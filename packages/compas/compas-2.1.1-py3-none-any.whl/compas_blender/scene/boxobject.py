from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.colors import Color
from compas.geometry import Box
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class BoxObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing box shapes in Blender.

    Parameters
    ----------
    box : :class:`compas.geometry.Box`
        A COMPAS box.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, box: Box, **kwargs: Any):
        super().__init__(geometry=box, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        show_wire: bool = True,
    ) -> list[bpy.types.Object]:
        """Draw the box associated with the scene object.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the box.
        collection : str | :blender:`bpy.types.Collection`, optional
            The name of the Blender scene collection containing the created object(s).
        show_wire : bool, optional
            Display the wireframe of the box.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The object(s) created in Blender to represent the box.

        """
        color = Color.coerce(color) or self.color
        name = self.geometry.name

        # add option for local coordinates
        vertices, faces = self.geometry.to_vertices_and_faces()
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=show_wire)

        self._guids = [obj]
        return self.guids
