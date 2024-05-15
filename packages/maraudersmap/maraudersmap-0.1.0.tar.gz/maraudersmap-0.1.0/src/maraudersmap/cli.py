#!/usr/bin/env python
"""
cli.py

Command line interface for tools in MaraudersMaps
"""
import click
from loguru import logger

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def add_version(f):
    """
    Add the version of the tool to the help heading.
    :param f: function to decorate
    :return: decorated function
    """
    import maraudersmap

    doc = f.__doc__
    f.__doc__ = (
        "Package "
        + maraudersmap.__name__
        + " v"
        + maraudersmap.__version__
        + "\n\n"
        + doc
    )

    return f


@click.group()
@add_version
def main_cli():
    """
        ---------------    Marauders map  --------------------

        You are now using the Command line interface of Marauders map package,
        a set of tools created at CERFACS (https://cerfacs.fr).
        It creates callgraphs for python and fortran projects.

        Use `mmap anew` to create your main control file `mmap_in.yml`.
        The other commands use this control file to locate your sources and extract data.
        Here follows the complete workflow of marauder's commands(boxed) and data (plain text).



        \b
                                mmap_in.yml
                                     |
                                     |
                                     |
                  +------------------+-----------+-----------+--------+
                  |                              |           |        |
                  |                         +----+---+       |        |
                  |                         |treefile|       |        |
                  |                         +----+---+       |    +---v---+
             +----+---+                          |           |    |imports|
             |treefunc|                          v           |    +---+---+
             +----+---+                    file_tree.json    |        |
                  |                              |           |        v
                  |                              |           |import_graphs.js
                  v                              |           |   |    |
           func_tree.json-------------------+---|||------+   |   |    |
                  |                         |    |       |   |   |    |
                  |                         |    |       |   |   |    |
                  |                         |    |      +v---v---v+   |
                  |          +------------+ |    |      |callgraph|   |
                  |          |regexp-input| |    |      +----+----+   |
                  |          +-------+----+ |    |           |        |
                  |                  |      |    |           |        |
    +------+      |        +-----+   v      |    |           |        |
    | grep <------+-------->score<-rules.yml|    |           |        |
    +---+--+               +--+--+          |    |           |        |
        |                     |             |    |           v        |
        |        score<-------+             |    |    callgraph.json  |
        v                     |             |    |              |     |
    graphical        stats<---+             |    |              |     |
     output                   |             |    |              |     |
                              v             |    |              |     |
                    func_tree_score.json    |    |              |     |
                              |      +------+    |              |     |
                              +---+  |           |            +-v-----v-+
                                  |  |  +--------+            |showgraph|
                                  |  |  |                     +----+----+
                                 +v--v--v-+                        |
                                 |showtree|                        v
                                 +---+----+                     graphical
                                     |                           output
                                     v
                                  graphical
                                   output

        The created data (trees of graphs) are shown graphically through command `mmap show`.

    """
    pass


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
def anew(file):
    """Create a default  MMAP control file."""
    from pkg_resources import resource_filename
    import os, shutil

    write = True
    if os.path.isfile(file):
        msg = f"File {file} already exists. Overwrite ? [y/N] "
        if input(msg).lower() == "n":
            write = False
    if write:
        logger.info(f"Generating template inputfile {file} for maraudersmap.")
        shutil.copy2(
            resource_filename(__name__, "./mmap_in.yml"),
            file,
        )
    logger.success(f"File {file} created. Edit this file to set up your project...")


main_cli.add_command(anew)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def treefunc(file, verbose):
    """Create the tree of functions from sourcecode.

    Output is (name-of-pkg)/func_tree.json

    Need the MMAP Control file to find the sources,
    and obviously the sources themselves...
    """
    from maraudersmap.tree import get_tree
    import networkx as nx
    from json import dump as jdump
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)
    tree_graph = get_tree(
        param["path"],
        param["package"],
    )
    outdir = ensure_dir(param["package"])
    with open(outdir / "func_tree.json", "w") as fout:
        jdump(nx.node_link_data(tree_graph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']} / func_tree.json.")


main_cli.add_command(treefunc)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def treefile(file, verbose):
    """Create the tree of files from sourcecode.

    Output is (name-of-pkg)/file_tree.json

    Need the MMAP Control file to find the sources,
    and obviously the sources themselves...
    """
    from maraudersmap.macro_tree import get_macro_tree
    from networkx import node_link_data
    from json import dump as jdump
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    param = prepare_cmd(file)
    macro_graph = get_macro_tree(
        param["path"],
        param["package"],
    )
    outdir = ensure_dir(param["package"])
    with open(outdir / "file_tree.json", "w") as fout:
        jdump(node_link_data(macro_graph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']} / file_tree.json.")


main_cli.add_command(treefile)


@click.command()
@click.argument(
    "rules",
    nargs=1,
    type=click.Choice(["python", "fortran"]),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def regexp_input(rules, verbose):
    """Create a score rules file"""
    from pkg_resources import resource_filename
    import os, shutil
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    write = True
    if rules == "python":
        file = "./python_rc_default.yml"
        if os.path.isfile(file):
            msg = f"File {file} already exists. Overwrite ? [y/N] "
            if input(msg).lower() == "n":
                write = False
    elif rules == "fortran":
        file = "./fortran_rc_default.yml"
        if os.path.isfile(file):
            msg = f"File {file} already exists. Overwrite ? [y/N] "
            if input(msg).lower() == "n":
                write = False
    if write:
        logger.info(f"Generating dummy regexp inputfile {file} for maraudersmap score.")
        shutil.copy2(
            resource_filename(__name__, f"{file}"),
            file,
        )
    logger.info(f"File {file} created. Edit this file to customize your own rules.")


main_cli.add_command(regexp_input)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.argument(
    "rules",
    type=str,
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def score(rules, file, verbose):
    """
    Add score to the MMAP tree of functions

    Need the MMAP Control file to find the sources,

    RULES is the regexp&structure set of rules.
    These rules can be generated through mmap regexp-input (can be edited)
    """
    import json, os
    from networkx import node_link_data, node_link_graph
    from json import dump as jdump
    from maraudersmap.score import get_score
    from pathlib import Path
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)

    func_tree = Path(param["package"]) / "func_tree.json"
    if not func_tree.exists():
        logger.warning(
            f"Function tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )

    with open(func_tree, "r") as fin:
        nld = json.load(fin)
    tree_graph = node_link_graph(nld)
    score_graph = get_score(param["path"], tree_graph, rules)
    with open(Path(param["package"]) / "func_tree_score.json", "w") as fout:
        jdump(node_link_data(score_graph), fout, indent=4, sort_keys=True)
    logger.success(f"Generating {param['package']}/func_tree_score.json with scores.")


main_cli.add_command(score)


@click.command()
@click.argument(
    "pattern",
    type=str,
)
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def grep(file, pattern, verbose):
    """

    JSON_DATA is the database of the tree graph generated through mmap tree
    """
    import json
    from pathlib import Path
    from networkx import node_link_data, node_link_graph
    import tkinter as tk
    from nobvisual.tkinter_circlify import tkcirclify
    from nobvisual.circlifast import circlifast
    from nobvisual.colorize import color_by_value
    from nobvisual.helpers import from_circlify_to_nobvisual
    from maraudersmap.grep import get_grep_coverage
    from maraudersmap.show_nobvisual import ntw_nobvisual
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)
    param = prepare_cmd(file)
    func_tree = Path(param["package"]) / "func_tree.json"
    print(func_tree)
    if not func_tree.exists():
        logger.warning(
            f"Function tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )
    with open(func_tree, "r") as fin:
        nld = json.load(fin)

    tree_graph = node_link_graph(nld)
    grep_cov_graph = get_grep_coverage(pattern, tree_graph)
    nobj = ntw_nobvisual(grep_cov_graph)
    legend = color_by_value(nobj, "grep", tolcmap="rainbow_WhRd")
    circles = circlifast(nobj, show_enclosure=False)
    draw_canvas = tkcirclify(from_circlify_to_nobvisual(circles), legend=legend)
    draw_canvas.show_names(level=2)
    tk.mainloop()


main_cli.add_command(grep)


@click.command()
@click.argument(
    "colorby",
    nargs=1,
    type=click.Choice(
        [
            "complexity",
            "score",
            "patterns",
            "size",
            "file_patterns",
            "file_complexity",
            "file_size",
        ]
    ),
)
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="MMAP Control file (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def showtree(colorby, file, verbose):
    """Visualize MMAP trees

    Need the MMAP Control file to find the sources
    """
    import json
    from pathlib import Path
    import networkx as nx
    import tkinter as tk
    from nobvisual.tkinter_circlify import tkcirclify
    from nobvisual.circlifast import circlifast
    from nobvisual.colorize import color_by_name_pattern, color_by_value
    from nobvisual.helpers import from_circlify_to_nobvisual
    from maraudersmap.show_nobvisual import ntw_nobvisual
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)
    # Select source
    if colorby in ["file_complexity", "file_size", "file_patterns"]:
        func_tree = Path(param["package"]) / "file_tree.json"
    elif colorby == "score":
        func_tree = Path(param["package"]) / "func_tree_score.json"
    else:
        func_tree = Path(param["package"]) / "func_tree.json"

    if not func_tree.exists():
        logger.warning(
            f"Tree {str(func_tree)} is missing. Use `mmap tree` to create it."
        )
    with open(func_tree, "r") as fin:
        nld = json.load(fin)
    cgs_nx = nx.node_link_graph(nld)
    nobj = ntw_nobvisual(cgs_nx)

    if colorby in ["patterns", "file_patterns"]:
        legend = [(f"*{key}*", value) for key, value in param["color_rules"].items()]
        color_by_name_pattern(nobj, legend)
    elif colorby in ["complexity", "file_complexity"]:
        legend = color_by_value(nobj, "ccn", tolcmap="BuRd", logarithmic=True)
    elif colorby == "score":
        legend = color_by_value(nobj, "score", tolcmap="YlOrBr")
    elif colorby in ["size", "file_size"]:
        legend = color_by_value(nobj, "size", tolcmap="rainbow_PuRd", logarithmic=False)
    else:
        logger.warning(f"color by {colorby} is not an option")

    circles = circlifast(nobj, show_enclosure=False)
    draw_canvas = tkcirclify(from_circlify_to_nobvisual(circles), legend=legend)
    draw_canvas.show_names(level=2)
    tk.mainloop()


main_cli.add_command(showtree)


# @click.command()
# @click.argument("macro_graph", type=str)
# @click.option(
#     "--file",
#     "-f",
#     type=str,
#     default="./coverage.json",
#     help="Coverage json file from gcov",
# )
# def coverage_tree(macro_graph, file):
#     """Dump .json of mmap coverage macro tree graph."""
#     import json
#     from networkx import node_link_data, node_link_graph
#     from json import dump as jdump
#     from maraudersmap.coverage import get_coverage_tree

#     with open(macro_graph, "r") as fin:
#         nld = json.load(fin)
#     macro_graph = node_link_graph(nld)

#     coverage_graph = get_coverage_tree(macro_graph, file)

#     with open(f"coverage_tree.json", "w") as fout:
#         jdump(node_link_data(coverage_graph), fout, indent=4, sort_keys=True)

#     logger.success(f"Generating coverage_tree.json, use show command to see your results.")


# main_cli.add_command(coverage_tree)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def imports(file, verbose):
    """Create the MMAP import graph of functions

    Need the MMAP Control file to find the sources,
    """
    import os
    from maraudersmap.imports import get_importsgraph
    from networkx import node_link_data
    from json import dump as jdump
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)

    wkdir = os.getcwd()

    imports_graph = get_importsgraph(
        os.path.join(wkdir, param["path"]),
        param["package"],
        # tree_graph
    )
    outdir = ensure_dir(param["package"])
    with open(outdir / "imports.json", "w") as fout:
        jdump(node_link_data(imports_graph), fout, indent=4, sort_keys=True)

    logger.success(f"Generating {param['package']}/imports.json.")


main_cli.add_command(imports)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
@click.option(
    "-p",
    "--parents",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include parents links",
)
@click.option(
    "-c",
    "--contains",
    is_flag=True,
    show_default=True,
    default=False,
    help="Include contains links",
)
@click.option(
    "-n",
    "--nocalls",
    is_flag=True,
    show_default=True,
    default=False,
    help="Exclude direct calls",
)
def callgraph(file, verbose,parents, contains,nocalls):
    """Visualize mmap callgraph

    Arguments are the repo path and the code name.
    Backend for visualization is nobvisual by default.
    if kill

    """
    from json import dump as jdump
    from maraudersmap.callgraph import get_callgraph
    from networkx import node_link_data
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)


    callgraph = get_callgraph(
        param["path"], 
        param["context"],
        include_contains=contains,
        include_parents=parents,
        include_callables= (not nocalls),
    )

    outdir = ensure_dir(param["package"])
    with open(outdir / "callgraph.json", "w") as fout:
        jdump(node_link_data(callgraph), fout, indent=4, sort_keys=True)

    logger.success(f"Generating {param['package']}/callgraph.json.")


main_cli.add_command(callgraph)


@click.command()
@click.option(
    "--file",
    "-f",
    type=str,
    default="./mmap_in.yml",
    help="Input file with a custom name (.yml)",
)
@click.option(
    "--backend",
    "-b",
    type=click.Choice(["pyplot", "pyvis"]),
    default="pyplot",
    help="Backend for rendering",
)
@click.argument(
    "graphs",
    nargs=1,
    type=click.Choice(["imports", "callgraph"]),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Verbose mode",
)
def showgraph(graphs, file, backend, verbose):
    """Visualize mmap callgraphs stored in a JSON_DATA file

    mmap_in.yml control file is still used for:
    1 ) Vizualization (colors, shading)
    2 ) Cleaning (removal by patterns)
    3 ) Augmentation (add missing parent nodes)
    """
    import shutil, os, json
    from pathlib import Path
    import networkx as nx

    from maraudersmap.full_graph_actions import (
        clean_graph,
        color_nodes_by_quantity,
        color_nodes_by_pattern,
    )
    from maraudersmap.show_pyvis import showgraph_pyvis
    from maraudersmap.show_pyplot import ntw_pyplot2d
    from maraudersmap.mmap_startlog import mmap_startlog

    mmap_startlog(verbose)

    param = prepare_cmd(file)

    if graphs in ["imports"]:
        graph_json = Path(param["package"]) / "imports.json"
    elif graphs in ["callgraph"]:
        graph_json = Path(param["package"]) / "callgraph.json"

    with open(graph_json, "r") as fin:
        nld = json.load(fin)

    cgs_nx = nx.node_link_graph(nld)

    # if colorby == "patterns":

    # Add a "guess rules" functionality

    cgs_nx, legend = color_nodes_by_pattern(cgs_nx, param["color_rules"])
    # elif colorby == "complexity":
    #     cgs_nx, legend = color_nodes_by_quantity(cgs_nx, 1, 80, "ccn")
    # else:
    #     raise RuntimeError(f"color by {colorby} not supported")

    cgs_nx = clean_graph(
        cgs_nx,
        remove_patterns=param["clean_graph"].get("remove_patterns", []),
        soften_patterns=param["clean_graph"].get("soften_patterns", []),
        hyperconnect=param["clean_graph"].get("remove_hyperconnect", 5),
        subgraph_roots=param["clean_graph"].get("subgraph_roots", []),
        prune_lower_levels=param["clean_graph"].get("prune_lower_levels", 0),
    )
    outdir = ensure_dir(param["package"])
    file_prefix = f"{param['package']}_{graphs}"

    if backend == "pyvis":
        showgraph_pyvis(cgs_nx, legend, file_prefix)
        pyvis_file = file_prefix + ".html"
        # if (outdir/pyvis_file).exists():
        #     os.remove(outdir/pyvis_file)
        # shutil.move(pyvis_file,outdir /pyvis_file)
        # shutil.rmtree(outdir /"lib")
        # shutil.move("lib",outdir /"lib") #lib is associated to callgraphs

    if backend == "pyplot":
        
        layout_args = param.get("pyplot_layout", {})

        ntw_pyplot2d(
            cgs_nx,
            param["color_rules"],
            file_prefix=file_prefix,
            **layout_args
            # nit=param["pyplot_layout"].get("nit", 10000),
            # neighbors=param["pyplot_layout"].get("neighbors", 4),
            # relax_connexions=param["pyplot_layout"].get("relax_connexions", 0.2),
            # relax_repulsions=param["pyplot_layout"].get("relax_repulsions", 0.2),
            # relax_gravity_level=param["pyplot_layout"].get("relax_gravity_level", 0.1),
            # relax_gravity_frontier=param["pyplot_layout"].get(
            #     "relax_gravity_frontier", 0.0
            # ),
        )


main_cli.add_command(showgraph)


########################################################
####################### UTILITIES ######################
########################################################


def dump_json(nx_data, type_):
    import json
    from networkx import node_link_data

    fname = f"mmap_{type_}_graph.json"
    with open(fname, "w") as fout:
        json.dump(node_link_data(nx_data), fout, indent=4, sort_keys=True)
    logger.info(f"Graph dumped as {fname}")


def prepare_cmd(file) -> dict:
    """Read and check the control file of MMAP."""
    from yaml import safe_load
    from pathlib import Path

    ctrl_file = Path(file)
    if not ctrl_file.exists():
        logger.warning(
            f"File {file} does not exist. Use  >mmap anew  to create a new one"
        )

    with open(file, "r") as fin:
        param = safe_load(fin)

    if param is None:
        raise RuntimeError(f"No parameters found in {file}")

    tgt = Path(param["path"])
    if not tgt.exists():
        raise RuntimeError(f"Path {param['path']} not found")
    
    if "context" not in param:
        param["context"]= param["path"]

    return param


def ensure_dir(dir):
    """As name says

    So short we could remove it."""
    from pathlib import Path

    outdir = Path.cwd().absolute() / dir
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir
