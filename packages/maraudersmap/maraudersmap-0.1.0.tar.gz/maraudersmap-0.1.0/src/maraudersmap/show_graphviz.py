"""Module to show a a networkX directed graph with pyvis"""

import graphviz
import networkx as nx

from maraudersmap.colors_utils import find_color,darken_color,brighten_color

def ntw_graphiz(
    ntx: nx.DiGraph,
    refsize: int = 3,
    color_filter: dict = None,
    prefix: str = "nodes",
    graph_engine: str = "dot",
    view: bool = True,
):
    """
    Convert a networkx to a pyvis html File

    ntx: a Network X directed Graph
    size: reference size in pixel, use this to scale up everything
    loosen: [-] mass divided:
        if increased, makes nodes more losely coupled during interactions
    title: used to create the file
    physics_panel: if true add physic panel to the HTML
    """

    if color_filter is None:
        color_filter = {}

    gfz = graphviz.Digraph("dummy", engine=graph_engine)

    for node in ntx.nodes:

        label = node
        color = find_color(node, color_filter)
        node_size = ntx.nodes[node].get("size", refsize)
        node_soften = ntx.nodes[node].get("soften", False)
        size = 0.5 * refsize * (node_size / refsize) ** 0.5
        pencolor = darken_color(color)

        # if color == "#ffffff":
        #    pencolor="#000000"
        if node_soften:
            color = brighten_color(color)

        gfz.node(
            label,
            style="filled",
            fillcolor=color,
            color=pencolor,
            # color=txt_color(color), #Find the parameter for the text
            shape="record",
            penwidth=str(size),
        )

    for link in ntx.edges:
        style = "solid"
        edge_size = ntx.edges[link].get("size", refsize)
        edge_soften = ntx.edges[link].get("soften", False)

        color = find_color(link[0], color_filter)
        if color == "#ffffff":
            color = "#000000"

        size = 0.5 * refsize * (edge_size / refsize) ** 0.5
        if edge_soften:
            size = 1
            style = "dashed"

        gfz.edge(link[0], link[1], style=style, color=color, penwidth=str(size))

    gfz.render(prefix, format="svg", cleanup=True, view=view)
    print("Rendered with graphvis in your browser")
    print(f"Output written to {prefix}.svg")
