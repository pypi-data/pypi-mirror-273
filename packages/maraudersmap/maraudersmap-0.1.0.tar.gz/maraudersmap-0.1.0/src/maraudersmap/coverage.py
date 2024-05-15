import json
import networkx as nx
from loguru import logger


def unroll_coverage_json(json_cov: str) -> dict:
    """
    Parser to access the test coverage data from the gcov file

    Args:
        json_cov (str): Path to the gcov file

    Returns:
        out (dict): Dictionnary with coverage rate for each functions
    """
    with open(json_cov, "r") as fin:
        ct = json.load(fin)
    return unroll_coverage(ct)


def unroll_coverage(cov: dict) -> dict:
    """
    Parser to access the test coverage data from the gcov file

    Args:
        json_cov (str): Path to the gcov file

    Returns:
        out (dict): Dictionnary with coverage rate for each functions
    """
   
    out = {}
    all_lines = 0
    all_lines_cov = 0

    for file in cov["files"]:
        name = file["file"]
        file_lines = 0
        file_lines_cov = 0
        nbranches = 0
        nbranch_cov = 0
        for line in file["lines"]:
            if line["gcovr/excluded"]:
                continue
            if line["gcovr/noncode"]:
                continue
            
            file_lines += 1
            if line["count"] >= 1:
                file_lines_cov += 1

            # nbranches += len(line["branches"])
            # for branch in line["branches"]:
            #     if branch["count"] >= 1:
            #         nbranch_cov += 1
                
        # Global cvg
        all_lines_cov += file_lines_cov
        all_lines += file_lines
        # Compute coverage
        try:
            cvg_lines = file_lines_cov * 1.0 / file_lines
        except ZeroDivisionError:
            cvg_lines = 0.0
        # try:
        #     cvg_branch = nbranch_cov * 1.0 / nbranches
        # except ZeroDivisionError:
        #     cvg_branch = 0.0

        # Storage of coverages
        out[name] = {
            "lines": (file_lines_cov, file_lines, cvg_lines),
            # "cvg_branch": (nbranch_cov, nbranches, cvg_branch),
        }

    global_cvg = all_lines_cov / all_lines

    logger.info(f"Global coverage {global_cvg*100:.2f}%")

    return out


def get_coverage_tree(graph: nx.DiGraph, json_cov: str) -> nx.DiGraph:
    """
    This will compute the pourcentage of tests coverage of each function
    of the tree graph based on the gocv file

    Args:
        graph (obj): Func tree graph of the repo
        json_cov (str): Path to the gcov file

    Returns:
        graph (obj): Update the func_tree_graph with the tests coverage parameter
    """
    json_cov = unroll_coverage_json(json_cov)
    for node_name in graph.nodes():
        graph.nodes[node_name]["coverage"] = 0
        for file_key in json_cov.keys():
            if file_key in node_name:
                graph.nodes[node_name]["coverage"] = json_cov[file_key]["lines"][2]
    logger.info("Coverage tree generated.")
    return graph
