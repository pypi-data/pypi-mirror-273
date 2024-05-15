

import networkx as nx
import fnmatch
from copy import deepcopy
import numpy as np
from matplotlib import colors
from loguru import logger
from maraudersmap.nx_utils import (
    remove_by_patterns,
    remove_hyperconnect,
    remove_singles,
    soften_by_patterns,
    get_subgraph,
    crop_leafs,
)

from maraudersmap.colors_utils import colorscale,find_color

def clean_graph(
    nxdata: nx.DiGraph,
    remove_patterns: list = None,
    soften_patterns: list = None,
    hyperconnect: int = None,
    subgraph_roots:list =None,
    prune_lower_levels:int=None,
) -> nx.DiGraph:
    """
    Performs the diverse cleanings of the graph

    Args:
        ntx (obj): ntx (obj): networkX DiGraph
        remove_patterns (list): List of patterns to match in nodes name
        soften_patterns (list): List of patterns to match in nodes name
        hyperconnect (int): number of edges allowed for nodes

    Returns:
        ntx (obj): networkX DiGraph cleaned

    """

    def log_graph_size():
        logger.info(f"{nxdata.number_of_nodes()} nodes / {nxdata.number_of_edges()} edges")

    logger.info("Start filtering graph")

    log_graph_size()
    if subgraph_roots is not None:
        new_data = nx.DiGraph()
    
        for pattern in subgraph_roots:
            results =  fnmatch.filter(nxdata.nodes.keys(), pattern)
            if len(results)>1:
                logger.warning(f"subgraph_roots pattern {pattern} yielded several results")
                for res in results:
                    logger.warning(f" -{res}")
                logger.warning(f"Skipping...")
                
            elif len(results)==0:
                logger.warning(f"subgraph_roots pattern {pattern} yielded no results,{' '.join(results)} skipping...")
            else:
                new_data =nx.compose(new_data, get_subgraph(nxdata,results[0]))
        nxdata=new_data
        log_graph_size()
    
    if prune_lower_levels is not None:
        nxdata = crop_leafs(nxdata, levels=prune_lower_levels)
        log_graph_size()
    
    if hyperconnect is not None:
        nxdata = remove_hyperconnect(nxdata, hyperconnect)
        log_graph_size()
    
    #nxdata = remove_by_patterns(nxdata, ["<builtin>.*", "abc.*", "os.*", "shutil.*"])
    if remove_patterns is not None:
        nxdata = remove_by_patterns(nxdata, remove_patterns)
        log_graph_size()


    nxdata = remove_singles(nxdata)
    log_graph_size()

    
    
    if soften_patterns is not None:
        nxdata = soften_by_patterns(nxdata, soften_patterns)
        

    


    logger.info(
        "After cleaning :"
        + str(nxdata.number_of_nodes())
        + " nodes/"
        + str(nxdata.number_of_edges())
        + " edges"
    )
    if nxdata.number_of_nodes() == 0:
        msgerr = "Filtering removed all nodes, aborting"
        logger.critical(msgerr)
        raise RuntimeError( "Filtering removed all nodes, aborting")
    return nxdata


def color_nodes_by_quantity(
    graph: nx.DiGraph,
    min_lvl: int,
    max_lvl: int,
    color_by: str,
    color_map: str = "rainbow_PuRd",
    log_scale: bool = True,
) -> dict:
    """
    Add hexadecimal color to networkX graph according to a selected data

    Args:
        graph (obj): NetworkX graph
        min_lvl (int): Lower bound
        max_lvl (int): Upper bound
        color_by (str): Name of the data to look for in graph
        color_map (str): Name of the Paul Tol's color map desired
        log_scale (bool): switch to log_scale

    Returns:
        colored_graph (obj) : Update the color key in the graph nodes dict
        legend (dict): Name and color for legend
    """
    colored_graph = deepcopy(graph)
    for node in colored_graph.nodes:
        lvl = colored_graph.nodes[node].get(color_by, None)
        color = colorscale(
            lvl, min_lvl, max_lvl, color_map=color_map, log_scale=log_scale
        )
        color = colors.to_hex(color)
        colored_graph.nodes[node]["color"] = color

    legend = {}
    color_lvl = np.linspace(min_lvl, max_lvl, 5)

    for lvl in color_lvl:
        if min_lvl != 0 and max_lvl != 1:
            lvl = round(lvl)
        color_rgb = colorscale(
            lvl, min_lvl, max_lvl, color_map=color_map, log_scale=log_scale
        )
        color = colors.to_hex(color_rgb)
        legend[str(lvl)] = color

    return colored_graph, legend


def color_nodes_by_pattern(graph: nx.DiGraph, color_rules: dict):
    """
    Add hexadecimal color to networkX graph according to selected patterns

    Args:
        graph (obj): NetworkX graph
        color_rules (dict): Patterns as key, color as value

    Returns:
        colored_graph (obj) : Update the color key in the graph nodes dict
        legend (dict): Name and color for legend
    """

    colored_graph = deepcopy(graph)
    for node in colored_graph.nodes():
        color = colored_graph.nodes[node].get("color", None)
        if not color:
            color = find_color(node, color_rules)
            colored_graph.nodes[node]["color"] = color

    legend = {}
    for key, color in color_rules.items():
        legend[key] = colors.to_hex(color)

    return colored_graph, legend

