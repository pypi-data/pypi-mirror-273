from typing import List
from loguru import logger
from tucan.kw_lang import KEYWORDS_FTN

from tucan.unformat_common import (
    Statements,
    new_stmts,
    remove_strings,
    clean_blanks,
    clean_inline_comments,
    clean_pure_comments,
    align_multiline_blocks,
    split_multi_statement_lines,
    get_indent,
    eat_spaces,
)

def align_end_continuations(stmts: Statements) -> Statements:
    """Align continuation with amprsand
    
    For example

     FORMAT("Lorem ipsum &
     sic hamet") 
    
    """
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if last_line.strip().endswith("&"):
            new_stmt[-1] = last_line[:-1] + " " + line.strip().lstrip("&")
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)


def align_start_continuations(stmts: Statements) -> Statements:
    """Align continuation with amprsand
    
    For example

     FORMAT("Lorem ipsum
    & sic hamet") 
    
    """
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if line.lstrip().startswith("&"):
            new_stmt[-1] = last_line.rstrip("&") + " " + line.strip()[1:]
            new_lines[-1][1] = lend
        elif line.lstrip().startswith("$"):
            new_stmt[-1] = last_line.rstrip("$") + " " + line.strip()[1:]
            new_lines[-1][1] = lend
        elif line.startswith("     +"):
            new_stmt[-1] = last_line.rstrip("     +") + " " + line.strip()[1:]
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)


def ftn_align_labelled_continuations(stmts: Statements) -> Statements:
    """Align labelled continuations , very old style
   15 FORMAT(
     1/' TRANFT:  Transport property fitting,',
     2/'           CHEMKIN-II Version ',A,', August 1994',
C*****precision > double
     3/'           DOUBLE PRECISION')

     becomes
    15 FORMAT(' TRANFT:  Transport property fitting,',' CHEMKIN-II Version ',A,', August 1994','DOUBLE PRECISION') 
    
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if line[0:5]=="     " and (line[5] in "0123456789*"):
            new_stmt[-1]+=line[7:]
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

    return Statements(new_stmt, new_lines)



def ftn_make_oneliners_conditionals_multilines(stmts: Statements) -> Statements:
    """_summary_

    Args:
        stmts (Statements): _description_

    Returns:
        Statements: _description_
    """
    new_stmt = []
    new_lines = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if "do" in line.split():
            if ": do" in line.strip():
                new_stmt.append(
                    line.replace(" ".join(line.split()), "do " + " ".join(line.split()))
                )
            else:
                new_stmt.append(line)

        elif line.strip().startswith("if ") and " then" not in line:
            #logger.critical(line)
            splitted_parts = split_oneliner(line)
            #logger.critical(str(splitted_parts))
            indent = get_indent(line)
            new_stmt.append(splitted_parts[0]+ " then")
            new_lines.append([lstart, lend])
            new_stmt.append(indent + "   "+ splitted_parts[-1])
            new_lines.append([lstart, lend])
            new_stmt.append(indent + "end if")

        elif line.strip().startswith("where "):
            splitted_parts = split_oneliner(line)

            if not splitted_parts[-1]:
                new_stmt.append(line)
                new_lines.append([lstart, lend])
                continue

            indent = get_indent(line)
            new_stmt.append(splitted_parts[0])
            new_lines.append([lstart, lend])
            new_stmt.append(indent + splitted_parts[-1])
            new_lines.append([lstart, lend])
            new_stmt.append(indent + "end where")

        else:
            new_stmt.append(line)

        new_lines.append([lstart, lend])
    return Statements(new_stmt, new_lines)


def split_oneliner(line: str) -> list:
    """_summary_

    Args:
        line (str): _description_

    Returns:
        list: _description_
    """
    #logger.critical("Splitting line:"+line)
    path = []
    new_stmt = ""
    split_parts = []
    for idx, char in enumerate(line):
        if "(" in char:
            new_stmt += char
            path.append(char)
        elif ")" in char:
            new_stmt += char
            path.pop(-1)
            if not path:
                split_parts.append(new_stmt)
                split_parts.append(line[idx + 1 :])
                break
        else:
            new_stmt += char
    if not split_parts:
        split_parts=[new_stmt]
    return split_parts


def ftn_remove_space_in_front_of_variables(lines: List[str]) -> List[str]:
    """
    Detect keywords used as variables, and make sure it is without space:

    TYPE = 300 
    becomes
    TYPE= 300 
    
    This way, a true keyword is always followed by a space, and will be tetected,
    but false keywords wont
    """
    new_stmt = []
    for line in lines:
        stmt = line
        try:
            item0 = line.split()[0]
            item1 = line.split()[1]
        except IndexError:
            item1=None

        if item1 == "=" and item0 in KEYWORDS_FTN:
            stmt = line.replace(line.split()[0] + " =", line.split()[0] + "=")
            logger.warning(
                f"A Fortran Keywords {item0} is used as a variable in the code. Bad Practice Should Be Avoided"
            )
            
        new_stmt.append(stmt)
       
    return new_stmt



def ftn_clean_labelled_loops_oldftn(stmts: Statements) -> Statements:
    """Clean DO with labels instead of END DO

        Example in tranfit
        DO 600 K = 1, KK
            IF (NLIN(K) .EQ. NCHECK) THEN
                DO 750 J = K, KK
                    IF (NLIN(J) .EQ. NCHECK) WRITE (LOUT, 8010) KSYM(J)
                750  CONTINUE
                KERR = .TRUE.
            ENDIF
        600 CONTINUE

        to

        DO 600 K = 1, KK
            IF (NLIN(K) .EQ. NCHECK) THEN
                DO 750 J = K, KK
                    IF (NLIN(J) .EQ. NCHECK) WRITE (LOUT, 8010) KSYM(J)
                END DO !750 
                KERR = .TRUE.
            ENDIF
        END DO !600
    """
    new_stmt = []
    new_lines = []
    do_loop_lbl = []
    do_loop_indent = []
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        stmt = line

        try:
            item0=line.split()[0]
            item1=line.split()[1]
        except IndexError:
            new_stmt.append(stmt)
            new_lines.append([lstart, lend])
            continue
            
        if item0 == "do":
            if item1.isdigit():
                value = int(item1)
                do_loop_lbl.append(value)
                do_loop_indent.append(get_indent(line))
            

        if item0.isdigit() and do_loop_lbl:
            value = int(item0)
            while do_loop_lbl  and int(item0) == do_loop_lbl[-1]:
                stmt = do_loop_indent[-1]+f"end do ! {do_loop_lbl[-1]}"
                do_loop_indent.pop(-1)
                do_loop_lbl.pop(-1)
                new_stmt.append(stmt)
                new_lines.append([lstart, lend])
       
        else:     
            new_stmt.append(stmt)
            new_lines.append([lstart, lend])
       
    return Statements(new_stmt, new_lines)


def ftn_suppress_goto_references(lines: List[str]) -> List[str]:
    """Remove the GOTO references , put them at the end of the line
    
    """
    new_stmt = []
    for line in lines:
        stmt = line
        for keyword in KEYWORDS_FTN:
            if keyword in line.split() and line.split()[0].isdigit():
                stmt = line.replace(line.split()[0], len(line.split()[0]) * " ") + "  ! ("+  line.split()[0]+")"
        new_stmt.append(stmt)
    return new_stmt



def ftn_clean_labelled_loops_newftn(lines:List[str]) -> List[str]:
    """ Move modern labels at the end of the line 
    
     We keep label to show the name in struct
    """
    new_stmt = []
   
    def _move_labels(line:str, pattern:str="do", sep:str=":")->str:
        """
        eigenvalues: block

        becomes block ! NESTING_LABEL# eigenvalues
        """
        if pattern not in line or sep not in line:
            return line

        rhs = line.split(sep)[1].rstrip()
        rhs1=""
        for char in rhs:
            if char in " (":
                break
            rhs1+=char
        
        if rhs1==pattern:

            label = line.split(sep)[0].strip()
            index=line.find(sep)
            line = get_indent(line)+line[index+1:].rstrip()+ " ! NESTING_LABEL# "+label
        return line

    for line in lines:
        
        line = _move_labels(line, "block", ":")
        line = _move_labels(line, "do", ":")
        line = _move_labels(line, "if", ":")
        line = _move_labels(line, "entry", ":")
        line = _move_labels(line, "select_case", ":")
        new_stmt.append(line)
       
    return new_stmt

def ftn_clean_operators(lines:List[str]) -> List[str]:

    new_stmt = []
    for line in lines:
        line =line.replace("::", " :: ")
        line =line.replace("==", ".eq.")
        line =line.replace("/=", ".ne.")
        line =line.replace(">=", ".ge.")
        line =line.replace("<=", ".le.")
        #line =line.replace("=", " = ")
        new_stmt.append(line)
       
    return new_stmt

def ftn_clean_intrinsics_declarations(lines:List[str]) -> List[str]:
    """ clean oddities in fortran declarations"""
    new_stmt = []
   
    def _remove_decorators(line:str, keyword:str)->str:
        """usual cleanup before fortran structures:
        - check ends
        - put decorators at the back
        """
        if keyword not in line:
            return line
        
        if line.lstrip().startswith("end"):
            line.replace("end"+keyword,"end "+keyword )
            return line
        

        line_no_par = line.replace("("," ").replace(")"," ")+ " " # Here we add " " to make sure a keyword last on the line still trigger (" "+keyword+" ") for the replacement
        idx = line_no_par.find(" "+keyword+" ")
        if idx == -1:
            return line
        
        line = (get_indent(line) 
                + line[idx+1:]
                + " ! "+keyword.upper() +"# "+line[:idx+1].lstrip())
        return line
    for line in lines:

        # merge multiple words
        line =line.replace("double precision", "double_precision ")
        line =line.replace("module procedure", "module_procedure ")
        line =line.replace("type,public,abstract", "type_public_abstract ")
        line =line.replace("type,public", "type_public ")
        line =line.replace("type,private,abstract", "type_private_abstract ")
        line =line.replace("type,private", "type_private ")
        line =line.replace("type is", "type_is ")
        line =line.replace("selectcase", "select_case ")
        line =line.replace("select case", "select_case ")
        line =line.replace("select type", "select_type ")
        
        
        line = _remove_decorators(line, "function")
        line = _remove_decorators(line, "subroutine")
        line = _remove_decorators(line, "interface")


        line =line.replace("enddo", "end do ")
        line =line.replace("endif", "end if ")       # Important to add supp. spacing , incase of a following elmt.
        line =line.replace("endwhere", "end where ")
        line =line.replace("endmodule", "end module ")       # Important to add supp. spacing , incase of a following elmt.
        
        # slpit left parenthesis - and right ...
        for keyword in [
                "function",
                "subroutine",
                "interface",
                "if",
                "do",
                "type",
                "associate"
            ]:
            line=line.replace(f"{keyword}(",f"{keyword} (")

        line =line.replace(")then", ") then ")
        
        new_stmt.append(line)
       
    return new_stmt


def ftn_clean_type_keywords(lines:List[str]) -> List[str]:
    """ Replace  type( declarations by _type("""
    
    def _clean_type(line:str)-> str:
        if line.replace(" ","")[4]=="(":         #for type(bcdhjzks)
            return line.replace("type","_type",1)
        elif line.replace(" ","")[4:6]=="is":    #for select type ; type is
            return line.replace("type is","#typeis",1)
        elif line.replace(" ","")[4] in " azertyuiopqsdfghjklmwxcvbn":        #well formed keyword
            return line
        elif line.replace(" ","")[4]==",":  
            return line.replace("type","type ",1)   #for  type, extend (need the space to identify the end of keyword)
        else:
            return line
    new_stmt=[]
    for line in lines:
        if line.lstrip().startswith("type"):
            line = _clean_type(line)
            
        new_stmt.append(line)    
    return new_stmt


def unformat_ftn(code: List[str]) -> Statements:
    """
    Unformat Fortran code by stripping comments and moving leading '&' characters.

    Args:
        code (List[str]): List of Fortran code lines.

    Returns:
        List[Tuple[str, Tuple[int, int]]]: List of unformatted code statements along with line number ranges.
    """
    stmts = new_stmts(code)

    stmts = clean_pure_comments(stmts, "c")
    stmts = clean_pure_comments(stmts, "C")
    stmts = clean_pure_comments(stmts, "*")

    stmts.stmt = eat_spaces(stmts.stmt)
    stmts.stmt = remove_strings(stmts.stmt, '"')
    stmts.stmt = remove_strings(stmts.stmt, "'")

    stmts = clean_inline_comments(stmts, "!")
    
    stmts = clean_blanks(stmts)
    stmts = align_end_continuations(stmts)
    stmts = align_start_continuations(stmts)
    stmts = ftn_align_labelled_continuations(stmts)
    stmts = align_multiline_blocks(stmts, "(/", "/)")
    
    stmts.stmt = ftn_clean_operators(stmts.stmt) 
    stmts = split_multi_statement_lines(stmts)
    
    #stmts.stmt = ftn_clean_type_declarations(stmts.stmt) # not sure we need this now
    stmts.stmt = ftn_clean_type_keywords(stmts.stmt)
    stmts.stmt = ftn_clean_intrinsics_declarations(stmts.stmt)
    stmts = ftn_clean_labelled_loops_oldftn(stmts)
    stmts.stmt = ftn_clean_labelled_loops_newftn(stmts.stmt)

    stmts.stmt = ftn_suppress_goto_references(stmts.stmt)   # !!After ftn_clean_labelled_loops_oldftn, or you cannot end loops
    stmts = ftn_make_oneliners_conditionals_multilines(stmts)
    stmts.stmt = ftn_remove_space_in_front_of_variables(stmts.stmt)

    return stmts
