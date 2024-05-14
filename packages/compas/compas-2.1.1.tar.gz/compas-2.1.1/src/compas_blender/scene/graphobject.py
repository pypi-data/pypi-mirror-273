from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import bpy  # type: ignore

import compas_blender
from compas.colors import Color
from compas.datastructures import Graph
from compas.geometry import Line
from compas.scene import GraphObject as BaseSceneObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class GraphObject(BlenderSceneObject, BaseSceneObject):
    """Scene object for drawing graph data structures in Blender.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`
        A COMPAS graph.

    """

    def __init__(self, graph: Graph, **kwargs: Any):
        super().__init__(graph=graph, **kwargs)
        self.nodeobjects = []
        self.edgeobjects = []

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_nodes(self):
        """Clear all objects contained in the node collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.nodeobjects)

    def clear_edges(self):
        """Clear all objects contained in the edge collection.

        Returns
        -------
        None

        """
        compas_blender.delete_objects(self.edgeobjects)

    # def clear_nodelabels(self):
    #     """Clear all objects contained in the nodelabel collection.

    #     Returns
    #     -------
    #     None

    #     """
    #     compas_blender.delete_objects(self.nodelabelcollection.objects)

    # def clear_edgelabels(self):
    #     """Clear all objects contained in the edgelabel collection.

    #     Returns
    #     -------
    #     None

    #     """
    #     compas_blender.delete_objects(self.edgelabelcollection.objects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(
        self,
        nodes: Optional[List[int]] = None,
        edges: Optional[Tuple[int, int]] = None,
        nodecolor: Optional[Union[Color, Dict[int, Color]]] = None,
        edgecolor: Optional[Union[Color, Dict[Tuple[int, int], Color]]] = None,
    ) -> list[bpy.types.Object]:
        """Draw the graph.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        edges : list[tuple[hashable, hashable]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        nodecolor : :class:`compas.colors.Color` | dict[hashable, :class:`compas.colors.Color`], optional
            The color specification for the nodes.
        edgecolor : :class:`compas.colors.Color` | dict[tuple[hashable, hashable], :class:`compas.colors.Color`], optional
            The color specification for the edges.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        self._guids = self.draw_nodes(nodes=nodes, color=nodecolor) + self.draw_edges(edges=edges, color=edgecolor)
        return self.guids

    def draw_nodes(
        self,
        nodes: Optional[List[int]] = None,
        color: Optional[Union[Color, Dict[int, Color]]] = None,
        collection: Optional[str] = None,
        radius: float = 0.05,
        u: int = 16,
        v: int = 16,
    ) -> List[bpy.types.Object]:
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of node identifiers.
            Default is None, in which case all nodes are drawn.
        color : :class:`compas.colors.Color` | dict[hashable, :class:`compas.colors.Color`], optional
            The color specification for the nodes.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.nodecolor = color

        for node in nodes or self.graph.nodes():  # type: ignore
            name = f"{self.graph.name}.node.{node}"  # type: ignore
            color = self.nodecolor[node]  # type: ignore
            point = self.graph.nodes_attributes("xyz")[node]  # type: ignore

            # there is no such thing as a sphere data block
            bpy.ops.mesh.primitive_uv_sphere_add(location=point, radius=radius, segments=u, ring_count=v)
            obj = bpy.context.object
            self.objects.append(obj)
            self.update_object(obj, name=name, color=color, collection=collection)
            objects.append(obj)

        return objects

    def draw_edges(
        self,
        edges: Optional[Tuple[int, int]] = None,
        color: Optional[Union[Color, Dict[Tuple[int, int], Color]]] = None,
        collection: Optional[str] = None,
    ) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edge keys (as uv pairs) identifying which edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`compas.colors.Color` | dict[tuple[hashable, hashable], :class:`compas.colors.Color`], optional
            The color specification for the edges.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        self.edgecolor = color

        for u, v in edges or self.graph.edges():  # type: ignore
            name = f"{self.graph.name}.edge.{u}-{v}"  # type: ignore
            color = self.edgecolor[u, v]  # type: ignore
            curve = conversions.line_to_blender_curve(Line(self.graph.nodes_attributes("xyz")[u], self.graph.nodes_attributes("xyz")[v]))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=collection)
            objects.append(obj)

        return objects

    # =============================================================================
    # draw labels
    # =============================================================================

    # def draw_nodelabels(self, text: Optional[Dict[int, str]] = None) -> List[bpy.types.Object]:
    #     """Draw labels for a selection nodes.

    #     Parameters
    #     ----------
    #     text : dict[hashable, str], optional
    #         A dictionary of vertex labels as vertex-text pairs.
    #         The default value is None, in which case every vertex will be labeled with its key.

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     self.node_text = text
    #     labels = []
    #     for node in self.node_text:
    #         labels.append(
    #             {
    #                 "pos": self.graph.nodes_attributes("xyz")[node],
    #                 "name": f"{self.graph.name}.nodelabel.{node}",
    #                 "text": self.node_text[node],
    #                 "color": self.nodecolor[node],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.nodelabelcollection)

    # def draw_edgelabels(self, text: Optional[Dict[Tuple[int, int], str]] = None) -> List[bpy.types.Object]:
    #     """Draw labels for a selection of edges.

    #     Parameters
    #     ----------
    #     text : dict[tuple[hashable, hashable], str], optional
    #         A dictionary of edge labels as edge-text pairs.
    #         The default value is None, in which case every edge will be labeled with its key.

    #     Returns
    #     -------
    #     list[:blender:`bpy.types.Object`]

    #     """
    #     self.edge_text = text
    #     labels = []
    #     for edge in self.edge_text:
    #         u, v = edge
    #         labels.append(
    #             {
    #                 "pos": centroid_points([self.graph.nodes_attributes("xyz")[u], self.graph.nodes_attributes("xyz")[v]]),
    #                 "name": f"{self.graph.name}.edgelabel.{u}-{v}",
    #                 "text": self.edge_text[edge],
    #                 "color": self.edgecolor[edge],
    #             }
    #         )
    #     return compas_blender.draw_texts(labels, collection=self.edgelabelcollection)

    # =============================================================================
    # draw miscellaneous
    # =============================================================================
