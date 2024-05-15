import re
from typing import Tuple, List
from loguru import logger
from tucan.unformat_common import Statements
from tucan.struct_common import (
    find_words_before_left_parenthesis,
    new_buffer_item,
    new_stack_item,
    struct_from_stack,
    struct_augment,
)

from tucan.kw_lang import KEYWORDS_C

def extract_struct_c(stmts: Statements, verbose:bool) -> dict:
    """Main calls to build structure form statements

    statements is the output of tucan.unformat_c.unformat_c
    """
    
    clean_code = stmts.to_code()
    all_structs = _extract_on_cleaned_c(stmts, verbose=verbose)
    all_structs = struct_augment(all_structs, clean_code, find_callables_c, compute_ccn_approx_c)
    return all_structs


def _extract_on_cleaned_c(stmts: Statements, verbose:bool=False) -> dict:
    """Extract structure from cleaned statements."""
    buffer = []
    stack = []
    path = []

    stat_idx = 0

    level = 0
    stack_level=[None]

    for line, (line_idx1, line_idx2) in zip(stmts.stmt, stmts.lines):
        stat_idx += 1
        part=""
        #print(line)
        
        
        if "###===" in line:
                type_,name = _parse_type_name_c(line,line_idx1)
                stack_level.append(level)
                path.append(name)
                buffer.append(
                    new_buffer_item(
                        type_=type_,
                        path=path,
                        name=name,
                        first_line=line,
                        line_idx=line_idx1,
                        statement_idx=stat_idx,
                        verbose=verbose
                    )
                )
                part=""
        
        for char in line:
            part+=char
            if char=="{":
                level +=1
            if char=="}":
                level -=1
                if level == stack_level[-1]:  
                    if verbose:
                        logger.critical(f"Stop :{str(path)}")
                    last_buff = buffer[-1]
                    stack.append(
                        new_stack_item(last_buff,line_idx2,stat_idx,line)
                    )
                    path.pop(-1)
                    buffer.pop(-1)
                    stack_level.pop(-1)
                

    return struct_from_stack(stack, main_types=[
#        "program ",
#        "module ",
#        "interface ",
            "function ",
            "subroutine ",
            "derived_type ",
            "userdef_type ",
            "pointer "
        ])


def _parse_type_name_c(line: str, line_idx:int)->Tuple[str, str]:
    """expect a lowercase stripped line
    takes the second word as the name
    """
    if line.strip()=="":
        return None,None

    for kw in ["for", "if", "else", "switch"]:
        if line.strip().startswith(f"{kw} "):
            return kw, kw+str(line_idx+1)
    
    rtype,name = line.replace("(", " ").split()[0:2]
    if rtype in ["void"]:
        type_ = "subroutine "
    elif rtype in ["int", "double", "char","float"]:
        type_ = "function "
    elif rtype in ["struct","enum","class" ]:
        type_ = "userdef_type "
    elif rtype.endswith("*"):
        type_ = "pointer "
    else:
        type_ = "unknown "
    
    return type_,name.rstrip("{")


##### Main structs



def find_callables_c(code: list) -> list:
    """Find callables in c"""
    candidates = []
    for line in code:
        candidates.extend(find_words_before_left_parenthesis(line.strip()))

    # NB we expect lines like 'call mysubroutine()' to be caught by left parenthesis law

    matches = [cand.strip() for cand in set(candidates) if cand not in KEYWORDS_C]
    return sorted(matches)  # Must be sorted for testing


def compute_ccn_approx_c(code: list) -> int:
    """Count decision points (if, else if, do, select, etc.)"""
    decision_points = re.findall(
        r"(?i)(if |else |for |case |default )", "\n".join(code)
    )
    complexity = len(decision_points) + 1
    return complexity
