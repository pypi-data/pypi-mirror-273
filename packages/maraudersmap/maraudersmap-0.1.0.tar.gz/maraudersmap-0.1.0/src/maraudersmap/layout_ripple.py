"""Custom RIPPLE layout for callgraphs, fair approximation of a force atlas layout"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.spatial import cKDTree

from loguru import logger

EPS=1e-12

def layout_ripple(
        ntx:nx.DiGraph,
        pos:dict,
        depth:dict,
        nit:int=10000,
        neighbors:int=4,
        relax_connexions:float=0.2,
        relax_repulsions:float=0.2,
        relax_gravity_level:float=0.0,
        relax_gravity_frontier:float=0.1,
        debug_show_graph:bool=False,
        debug_show_convergence:bool=True,
    )-> dict:
    """layout algorithm involving following attractions: 
    * links connexions (like spring layout)
    *repulsion (like in barnes hut) but limited to a small amount of neigbors (most import cost of the method)
    * and concentric gravity pits to attract the different levels of a callgraph 
    
    When the concentric gravity pit is strong, graph look like the ripple of a droplet in water, hence the name.
    """
    logger.info(f"Ripple layout pass.")
    logger.info(f"  - iterations {nit}")
    logger.info(f"  - neighbors {neighbors}")
    logger.info(f"  - relax_connexions {relax_connexions}")
    logger.info(f"  - relax_repulsions {relax_repulsions}")
    logger.info(f"  - relax_gravity_level {relax_gravity_level}")
    logger.info(f"  - relax_gravity_frontier {relax_gravity_frontier}")
    
    
    # Prepare arrays
    node_list = list(ntx.nodes.keys())
    nnodes = len(node_list)
    neighbors=min(neighbors,nnodes)
    conn=[]
    for edge in ntx.edges:
        conn.append([node_list.index(edge[0]),node_list.index(edge[1])])

    coords = [pos[node] for node in pos]
    depth_array = [depth[node] for node in pos]
    conn = np.array(conn)
    coords = np.array(coords)
    depth_array = np.array(depth_array)
    
    # Rescale coords to -1 1 -1 1 
    coords[:,0] = (coords[:,0]-coords[:,0].min())/(coords[:,0].max()-coords[:,0].min())
    coords[:,0] = -1+2*coords[:,0]
    coords[:,1] = (coords[:,1]-coords[:,1].min())/(coords[:,1].max()-coords[:,1].min())
    coords[:,1] = -1+2*coords[:,1]
    
    # Compute typical sizes
    area = 4. #drawing surface
    square_edge= np.sqrt(area)       # drawing suface width/height
    rim = 0.5*square_edge            # drawing radius
    pushlen = np.sqrt(area/nnodes)/2/6 # typical distance btwen equally spaces nodes
    if debug_show_graph:
        nx.draw(ntx, with_labels=False, node_color='grey', alpha=0.1, node_size=500, arrowstyle='->', arrowsize=10, pos=pos)

    list_rep=[]
    list_conn=[]
    list_grav_lvl=[]
    list_grav=[]
    
    last_completion= 0
 
    for iteration in range(nit):
        # level gravity: must be equal to 'pushlen' at distance 'square_edge'
        motion = _gravity_level_forces(coords,depth_array, pushlen, rim)
        coords += relax_gravity_level*motion
        residual_grav_lvl = np.sum(np.hypot(motion[:,0],motion[:,1])**2)/nnodes
        list_grav_lvl.append(residual_grav_lvl)
        
        # gravity: must be equal to 'pushlen' at distance 'rim'
        motion = _gravity_frontier(coords, pushlen, rim)
        coords += relax_gravity_frontier*motion
        residual_grav = np.sum(np.hypot(motion[:,0],motion[:,1])**2)/nnodes
        list_grav.append(residual_grav)

        # repulsion effect
        motion = _repulsion_forces(coords, neighbors,pushlen)
        coords += relax_repulsions*motion
        residual_rep = np.sum(np.hypot(motion[:,0],motion[:,1])**2)/nnodes
        list_rep.append(residual_rep)
    
        # spring effects
        motion = _connexion_forces_polar(coords, conn, pushlen)
        #motion = _connexion_forces(coords, conn, pushlen)
        coords += motion*relax_connexions
        residual_conn = np.sum(np.hypot(motion[:,0],motion[:,1])**2)/nnodes
        list_conn.append(residual_conn)

        # progress
        completion = int(iteration/(nit-1)*100)
        if completion>= last_completion+10:
            last_completion = completion
            logger.debug(f"[{int(iteration/(nit-1)*100)}%],Conn.:{residual_conn:.3g}, Rep.:{residual_rep:.3g}, Lvlgrav.:{residual_grav_lvl:.3g}, Frontier.:{residual_grav:.3g}")
            pos =  {
                node: coords[i,:] for i, node in enumerate(node_list)
            }
            if debug_show_graph:
                nx.draw(
                    ntx, 
                    with_labels=False, 
                    node_color='red', 
                    alpha=(iteration/(nit-1))**2,
                    node_size=50, 
                    arrowstyle='->', 
                    arrowsize=10, 
                    pos=pos
                )
    if debug_show_graph:
        plt.show()
        plt.clf()

    if debug_show_convergence:
        ax0 = plt.subplot(4, 1, 1)
        ax1 = plt.subplot(4, 1, 2)
        ax2 = plt.subplot(4, 1, 3)
        ax3 = plt.subplot(4, 1, 4)
        
        ax0.loglog(list_conn)
        ax1.loglog(list_rep)
        ax2.loglog(list_grav)
        ax3.loglog(list_grav_lvl)
        ax0.set_title("Connexion residual")
        ax1.set_title("Repulsion residual")
        ax2.set_title("Gravity frontier residual")
        ax3.set_title("Gravity level residual")
        plt.show()
    
    return pos


def _connexion_forces_polar(coords:np.array, conn: np.array, pushlen:float)->np.array:
    """Force to stabilize two neigbors to the distance PUSHLEN"""
    def spring_connexions(distances:np.array, pushlen:float)->np.array:
        spring = np.clip(distances-pushlen,-pushlen, 100*pushlen)
        # quadratic effort
        spring = np.where(spring>0,spring**3, -spring**3)
        return spring
    
    def boost_tangent(points, vectors,factor=3.):
        rad_pts=np.hypot(points[:,0],points[:,1])
        unit_vects=points/rad_pts[:,np.newaxis]
        rad_cpnt = np.sum(np.multiply(vectors, unit_vects), axis=-1)
        rad_vect =unit_vects* rad_cpnt[:, np.newaxis]
        tgt_vect=vectors-rad_vect
        return 1./factor*rad_vect+factor*tgt_vect

    pts_a = coords[conn[:,0]]
    pts_b = coords[conn[:,1]]
    edge_vectors = (pts_a-pts_b)

    distances=np.hypot(edge_vectors[:,0],edge_vectors[:,1])
    springs= spring_connexions(distances,pushlen)
    conn_motion = edge_vectors/(distances[:,np.newaxis]+EPS)*springs[:,np.newaxis]

    motion = np.zeros_like(coords)
    motion[conn[:,0],:] -= boost_tangent(pts_a,conn_motion)
    motion[conn[:,1],:] += boost_tangent(pts_b,conn_motion)
    return motion


def _connexion_forces(coords:np.array, conn: np.array, pushlen:float)->np.array:
    """Force to stabilize two neigbors to the distance PUSHLEN"""
    def spring_connexions(distances:np.array, pushlen:float)->np.array:
        spring = np.clip(distances-pushlen,-pushlen, 100*pushlen)
        # quadratic effort
        spring = np.where(spring>0,spring**3, -spring**3)
        return spring

    edge_vectors = (coords[conn[:,0]]-coords[conn[:,1]])                 
    distances=np.hypot(edge_vectors[:,0],edge_vectors[:,1])
    springs= spring_connexions(distances,pushlen)
    conn_motion = edge_vectors/(distances[:,np.newaxis]+EPS)*springs[:,np.newaxis]

    motion = np.zeros_like(coords)
    motion[conn[:,0],:] -= conn_motion
    motion[conn[:,1],:] += conn_motion
    return motion


def _gravity_level_forces(coords:np.array,depth_array:np.array,pushlen:float, rim:float,expnt=1.)->np.array:
    """Force to attract a node to its level gravity circle.
    The lower the node is in the callgraph, the outer circle it will be.

    Most external circle is at distance RIM.
    By lowering EXPNT, one can enlarge the inner circles.
    """
    rad=np.hypot(coords[:,0],coords[:,1])

    gravity_pits_radius = (depth_array / np.max(depth_array))**expnt * rim 
    
    radvec = coords/rad[:,np.newaxis]
    intensity = (rad-gravity_pits_radius)/pushlen
    motion = -pushlen*radvec *intensity[:,np.newaxis]
    return  motion


def _gravity_frontier(coords:np.array,pushlen:float, rim:float,expnt=1)->np.array:
    """Force to  limit nodes to a circular region of radius RIM
    """
    rad=np.hypot(coords[:,0],coords[:,1])
    radvec = coords/rad[:,np.newaxis]
    intensity = (rad/rim)**expnt
    motion = -pushlen*radvec * intensity[:,np.newaxis]
    return  motion






def _repulsion_forces(coords:np.array, neighbors:int,pushlen:float, expnt:int=2)->np.array:
    """Force to push away a node from its neigbors, vanishes at PUSHLEN distance"""
    def spring_repulsion(distances:np.array, pushlen:float, neighbors:int, factor:float=2)->np.array:
        z_pushlen= factor*pushlen
        spring = np.clip(1/(distances/z_pushlen+EPS), 0.5/neighbors,1)
        return (spring*z_pushlen)**expnt

    tree = cKDTree(coords)
    _,neighb  = tree.query(coords, k=neighbors)
    motion = np.zeros_like(coords)
    repulsion=0
    for nei in range(1,neighbors):
        edge_vectors = (coords[neighb[:,nei]]-coords[:,:])
        distances=np.hypot(edge_vectors[:,0],edge_vectors[:,1])
        springs= spring_repulsion(distances,pushlen,neighbors)
        repulsion+= springs.sum()
        motion += -edge_vectors/(distances[:,np.newaxis]+EPS)*springs[:,np.newaxis]
    return motion
        