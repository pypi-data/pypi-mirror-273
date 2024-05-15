from typing import List
from loguru import logger
from tucan.unformat_common import strip_c_comment, clean_c_comments


def scan_ifdef_variables(lines: List[str]) -> list:
    """Detect ifdef variables

    cancels inner variables"""
    out = []
    inner_defined = []
    for line in lines:
        if (
            line.startswith("#ifdef")
            or line.startswith("#elif")
            or line.startswith("#if ")
        ):
            rhs = line.split()[1]

            rhs = rhs.replace("defined(", "")
            rhs = rhs.replace(")", "")

            rhs = rhs.replace("||", " ")
            rhs = rhs.replace("&&", " ")

            out.extend(rhs.split())
        if line.startswith("#define"):
            definition = line.split()
            inner_defined.append(definition[1])

        inner_def = sorted(set(inner_defined))
        global_def= sorted(set(out))
        global_def = [item for item in global_def if item not in inner_defined]
        
    return global_def,inner_def


            




def read_definition(line:str)->str:
    parts=strip_c_comment(line).split()
    out = None
    if len(parts)==2:
        out= parts[1]+"=True"
    elif len(parts)>=3:
        out=parts[1]+"="+" ".join(parts[2:])
    else:
        raise RuntimeError(f"CPP statement - definition not understood :  {line}")
    return out

def remove_ifdef_from_module(lines: List[str], definitions: List[str], verbose: bool=False, fortran:bool=False) -> List[str]:
    """Cleaned version of a code
    
    The output must be exactly as long a the input
    """

    uncommented_lines = clean_c_comments(lines,fortran=fortran) # we should all C comments, except // for fortran

    out = []
    context = []
    definitions_values=[ def_+"=True" for def_ in definitions]

    local_definitions=[]
    for i,line in enumerate(uncommented_lines):
        ifdef_line = line.lstrip()
        if not context:
            included = True
        # ============================== Ifdef logic =============================
        if ifdef_line.startswith((
                "#ifdef",
                "# ifdef",
                "#ifndef",
                "# ifndef",
                "#elif",
                "# elif", 
                "#if ", 
                "# if "   # ???? Is this really cpp ifdef grammar?
            )):
            
            status = str(interpret_ideflogic(ifdef_line, definitions_values+local_definitions))
            # increment context
            if ifdef_line.startswith(("#elif", "# elif")):
                context[-1].append(status)  # append to the sublist of the last element
            else:
                context.append([status])  
            
            included = evaluate_context(context)
            out.append("")
            if verbose:
                logger.warning(f"{i:04}|{line} |Context  :{str(context)} |Included :{str(included)}")

        elif ifdef_line.startswith((
                "#else",
                "# else"    # ???? Is this really cpp ifdef grammar?
            )):
            #  if  elif  else
            #  True False False
            #  False True False
            #  False False True
            # all of the previous if/eli in the context must be false for else to be true

            status = "True"
            for bool_ in context[-1]:
                if bool_ == "True":  # if any of previous is true, status is False.
                    status = "False"
            context[-1].append(status)
            included = evaluate_context(context)
            out.append("")
            if verbose:
                logger.warning(f"{i:04}|{line} |Context  :{str(context)} |Included :{str(included)}")
         
        elif ifdef_line.startswith("#endif"):
            if not context:
                logger.error(f"{i:04}|{line} : No context found")
                raise RuntimeError("IFdef cleaning failed")
            else:
                context.pop(-1)  

            included = evaluate_context(context)      
            out.append("")        
            if verbose:
                logger.warning(f"{i:04}|{line} |Context  :{str(context)} |Included :{str(included)}")
            

        # ======================================= Other cases ============================
        elif ifdef_line.startswith("#define"):  # variable definitions
            if included:
                local_definitions.append(read_definition(line))
            out.append("")

        elif ifdef_line.startswith("#undef"):  # variable definitions
            if included:
                def_=strip_c_comment(line).split()[1]
                local_definitions = [item for item in local_definitions
                    if not item.startswith(def_+"=")]
            out.append("")

        elif ifdef_line.startswith("#include"):  # commented code??
            if included:
                out.append(line)
            else:
                out.append("")

        elif ifdef_line.startswith("#"):  # commented code??
            if verbose:
                logger.critical(f"{i:04}|{line} : Pragma not recognised")
            if included:
                out.append(line)
            else:
                out.append("")
        else:  # Normal code
            
            if included:
                out.append(line)
                if verbose:
                    logger.success(f"{i:04}|{line}")
            else:
                out.append("")
                if verbose:
                    logger.error(f"{i:04}|{line}")
                
    try:       
        assert len(out)==len(lines)  # The output must match exactly the input
    except AssertionError:
        logger.critical(f"Cleaned version {len(out)}/{len(lines)}")
        raise RuntimeError("Ifdef cleaning failed")
    return out

def evaluate_context(context: list) -> bool:
    """Interpret the context to see if next lines will be included or not"""
    if context == []:
        return True 
    final_context = [bools_[-1] for bools_ in context]
    if eval(" and ".join(final_context)):
        included = True
    else:
        included = False
    return included


def replace_strings_by_proxies(line:str)-> (str, dict) :
    """Extreme measure to handle strings values in Ifdefs..."""
    proxies={}
    indexes = [i for i, char in enumerate(line) if char == '"']

    if not indexes:
        return line, proxies 
    
    #logger.critical("Replacing strings:"+line)
    last_char=0
    out_line = ""
    for i in range(0, len(indexes), 2):
        pair = indexes[i:i+2]
        key = f"#STR{i}#"
        try:
            value = line[pair[0]:pair[1]+1]
        except IndexError: # happen is " are not in even number 
            break          # well this should never happen but you never know
        proxies[key]=value
        out_line+=line[last_char:pair[0]-1] + " "+key
        last_char=pair[1]+1

    out_line+=line[last_char:]
    return out_line, proxies 


def interpret_ideflogic(line:str,definitions:list)->bool:
    """ Assume an #ifdef-like start:  interpret the content of the line 
    
    NB: no #else or #endif should be ever encountered here (no logic to solve)
    """
    def_dict = {}
    for def_ in definitions:
        key,value=def_.split("=", 1)
        def_dict[key]=value
    
    re_line = strip_c_comment(line)
    # clean right hand side
    
    
    #"not", "or", "and" unneeded to be spaced if other are correctly spaced
    # needed to avoid collision btw <= and = , resp >= and =

    re_line = re_line.replace("#ifndef", " not ")
    re_line = re_line.replace("# ifndef", " not ")
    re_line = re_line.replace("#ifdef", " ")
    re_line = re_line.replace("# ifdef", " ")
    re_line = re_line.replace("# if", " ")
    re_line = re_line.replace("#if", " ")
    re_line = re_line.replace("#elif", " ")
    re_line = re_line.replace("# elif", " ")
    re_line = re_line.replace("defined", " ")

    # protect double chars operators
    re_line = re_line.replace(">=", ".ge.")
    re_line = re_line.replace("<=", ".le.")
    re_line = re_line.replace("!=", ".ne.")
    re_line = re_line.replace("==", ".eq.")
    
    for ops in [ "(", ")", ">", "<"]:
        re_line = re_line.replace(ops, f" {ops} ")
    re_line = re_line.replace("!", " not ")
    re_line = re_line.replace("||", " or ")
    re_line = re_line.replace("&&", " and ")


    # revert double chars operators
    re_line = re_line.replace(".ge.", " >= ")
    re_line = re_line.replace(".le.", " <= ")
    re_line = re_line.replace(".ne.", " != ")
    re_line = re_line.replace(".eq.", " == ")
   
    # assemble expression as string
    re_line, proxies=replace_strings_by_proxies(re_line)
    expr = ""
    for item in re_line.split():
        expr+= " "
        if item in def_dict:
            expr += def_dict[item]
        elif item in proxies:
            expr += proxies[item]
        elif item in [ 
            "(", ")", ">", "<",       #simple chars operators
            "<=", ">=", "==", "!=",   #double chars operators
            "not", "or", "and"        #logical operators
        ]:
            expr += item
        
        elif item.isdigit():
            expr += item
        else:
            expr += "False"
        expr+= " "
    try:
        out = eval(expr)
        #logger.warning(f"Expr   :{expr}")
    except (SyntaxError, TypeError) :
        logger.warning(f"Origin :{line}")
        logger.warning(f"Clean  :{re_line}")
        logger.warning(f"Expr   :{expr}")
        #raise RuntimeError("IFDEF expression not understood")
        logger.critical("IFDEF expression not understood, fallback to false")
        return False
    
    return out


def run_ifdef_pkg_analysis(files: dict) -> dict:
    """
    Gather the data associated to the functions and the imports within a file

    Args:
        files (dict): key: short_name , value: absolute paths

    Returns:
        dict: _description_
    """

    ifdef_analysis = {
        "global": [],
        "local": {},

    }
    
    gvars = []
    for file ,path_ in files.items():
        with open(path_,"r") as fin:
            lines = fin.read().split("\n")
        
        gv_, lv_ = scan_ifdef_variables(lines)
        
        gvars.extend(gv_)
        ifdef_analysis["local"][file]=lv_

    ifdef_analysis["global"]=sorted(set(gvars))
    logger.success("Analysis completed.")
    return ifdef_analysis

# with open("templates_ifdef.f","r") as fin:
#     lines = fin.read().split("\n")

# vars = scan_ifdef_variables(lines)
# print("Found "+ ", ".join(vars))

# out =remove_ifdef_from_module(lines,["OUIPI1","MOREARG","LVL1"])

# print("\n".join(out))
