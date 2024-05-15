import networkx as nx
from loguru import logger
from pathlib import Path
import json
from tucan.package_analysis import (
    run_struct,
    rec_travel_through_package,
    clean_extensions_in_paths,
)


def get_callgraph(
        path: str,
        context: str,
        include_contains:bool=False,
        include_parents:bool=False,
        include_callables:bool=True,
    ) -> nx.DiGraph:
    """Get the  structure (what), and the context structure (with respect to what) to build the calgraph"""

    if Path(path).is_file():
        tgt_code_db = run_struct([path])
    else:
        tgt_paths_list = rec_travel_through_package(path)
        tgt_paths_list = clean_extensions_in_paths(tgt_paths_list)
        tgt_code_db = run_struct(tgt_paths_list)
    

    if context == path:  # often the case so it avoid recomputation
        context_code_db = tgt_code_db
    else:
        if Path(context).is_file():
            context_code_db = run_struct([context])
        else:
            context_paths_list = rec_travel_through_package(context)
            context_paths_list = clean_extensions_in_paths(context_paths_list)
            context_code_db = run_struct(context_paths_list)


    with open("debug_struct.json","w") as fout:
        json.dump(context_code_db,fout,indent=4)


    callgraph = build_callgraph(
            tgt_code_db,
            context_code_db,
            include_contains=include_contains,
            include_parents=include_parents,
            include_callables=include_callables
        )

    return callgraph

def build_callgraph(
    tgt_code_db: dict,
    context_code_db: dict,
    include_contains:bool=False,
    include_parents:bool=False,
    include_callables:bool=True,
) -> nx.DiGraph:
    """
    Build the callgraph.

    """
    logger.info("Computing callgraph, this can take a while...")

    
    callgraph = nx.DiGraph()
    for file_orig, file_db in tgt_code_db.items():
        for func_orig, func_db in file_db.items():
            if f"{file_orig}:{func_orig}" not in callgraph.nodes:
                callgraph.add_node(f"{file_orig}:{func_orig}", **func_db)

            if include_contains:  # add links to contained functions
                for contained_name in func_db["contains"]:
                    match_ddb,match_name = _fetch_function_in_file_ddb(context_code_db[file_orig],contained_name)
                    if match_ddb is not None:
                        _add_link(
                            callgraph,
                            match_ddb,
                            file_orig,
                            file_orig,
                            func_orig,
                            match_name,
                            weight=2
                        )
            
            if include_parents: # add links to parents
                for parent_name in func_db["parents"]:
                    #logger.warning("Trying to find "+_parent_name)
                    match_ddb, match_name, match_file = _fetch_function_in_all_ddb(context_code_db, parent_name)
                    if match_ddb is not None:
                        _add_link(
                            callgraph,
                            match_ddb,
                            file_orig,
                            match_file,
                            func_orig,
                            match_name,
                            weight=2
                        )
                    
                    
                    # for _func_par in parent_db_file[parent_name]["contains"]:
                    #     pure_inherit=True
                    #     for func_ in func_db["contains"]:
                    #         if _func_par.split(".")[-1] == func_.split(".")[-1] :
                    #             pure_inherit=False
                    #     if pure_inherit:
                    #         callgraph.add_edge(
                    #             f"{file_orig}:{func_orig}",
                    #             f"{parent_file}:{_func_par}",
                    #             weight=8
                    #         )

            if include_callables:
                for called_name in func_db["callables"]:
                    match_ddb,match_name,match_file = _fetch_function_in_all_ddb(context_code_db, called_name)
                    if match_ddb is not None:
                        _add_link(
                            callgraph,
                            match_ddb,
                            file_orig,
                            match_file,
                            func_orig,
                            match_name,
                            weight=2
                        )
 
    logger.info("Callgraph generated")
    return callgraph

def _fetch_function_in_all_ddb(allfiles_ddb, func_name) -> (dict, str, str):
    for _file, db_by_file in allfiles_ddb.items(): # search parent anywhere in the code
        match_ddb, match_name = _fetch_function_in_file_ddb(db_by_file, func_name)
        if match_name is not None:
            match_file=_file
            return match_ddb, match_name, match_file
    logger.warning(f"Ref. to {func_name} not found")
    return None,None,None

def _fetch_function_in_file_ddb(file_ddb, func_name) -> (dict, str):
    for _func,_db_func in file_ddb.items():
        if _longest_match(_func,func_name) :
            match_name=_func
            match_ddb=_db_func
            logger.success(f"Parent {match_name}  found")
            return match_ddb, match_name
                
    #logger.warning(f"Parent {func_name} not found")
    return None,None



def _add_link(
        callgraph:nx.DiGraph, # the callgraph
        db_by_file:dict, # the func tree ddb for one file
        file_orig:str,  # the origin func filename
        file_target:str, # the target func filename
        func_orig:str,  # the origin func name
        func_target:str,  # the target func
        weight: int= 1
    ):
    """Add a link in the graph"""
    
    # for func_target_full, func_db in db_by_file.items():
    #     # test if a fiunc_name matches the call. if yes add the node and the edge
    #     #if _longest_match(func_target_full, func_target):  # pas necessaire
    if f"{file_target}:{func_target}" not in callgraph.nodes:
        callgraph.add_node(
            f"{file_target}:{func_target}", **db_by_file
        )

    callgraph.add_edge(
        f"{file_orig}:{func_orig}",
        f"{file_target}:{func_target}",
        weight=weight
    )
    return

# def _try_add_callable_all(
#         callgraph:nx.DiGraph,
#         full_context_code_db:dict,# the func tree ddb for all files
#         file_orig:str,
#         func_orig:str,
#         func_target:str 
#     )-> bool:
#     """Try to add a callable if it is in the context of the same file"""
#     added = False
#     for file_target, db_by_file in full_context_code_db.items():

#         # for ctxt_func_name, func_db in ctxt_file_db.items():
#         #     if  _longest_match(ctxt_func_name, call):
#         #         if (f"{ctxt_filename}:{ctxt_func_name}"not in callgraph.nodes):
#         #             callgraph.add_node(
#         #                 f"{ctxt_filename}:{ctxt_func_name}",**func_db,
#         #             )
#         #         callgraph.add_edge(
#         #             f"{filename}:{func_name}",
#         #             f"{ctxt_filename}:{ctxt_func_name}",
#         #         )
#         #         break
#         added = _add_link(
#             callgraph ,
#             db_by_file,
#             file_orig,
#             file_target,
#             func_orig,
#             func_target
#         )
#         if added:
#             break    
       
#     return added




def _longest_match(ctxt_func_name:str,call_func:str)->bool:
    """Search for the longest match in the functions"""

    try:
        if ctxt_func_name.split(".")[-4:] == call_func.split(".") :
            return True
    except IndexError:
        pass

    try:
        if ctxt_func_name.split(".")[-3:] == call_func.split(".") :
            return True
    except IndexError:
        pass

    try:
        if ctxt_func_name.split(".")[-2:] == call_func.split(".") :
            return True
    except IndexError:
        pass

    if ctxt_func_name.split(".")[-1] == call_func :
        return True


    return False


    

    