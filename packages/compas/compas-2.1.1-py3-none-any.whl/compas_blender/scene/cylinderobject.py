from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.geometry import Cylinder
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class CylinderObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing cylinder shapes in Blender.

    Parameters
    ----------
    cylinder : :class:`compas.geometry.Cylinder`
        A COMPAS cylinder.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, cylinder: Cylinder, **kwargs: Any):
        super().__init__(geometry=cylinder, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        u: int = 16,
        show_wire: bool = False,
        shade_smooth: bool = False,
    ) -> list[bpy.types.Object]:
        """Draw the cylinder associated with the scene object.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The RGB color of the cylinder.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        u : int, optional
            Number of faces in the "u" direction.
        show_wire : bool, optional
            Display the wireframe of the cylinder.
        shade_smooth : bool, optional
            Display smooth shading on the cylinder.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u)
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)
        if shade_smooth:
            mesh.shade_smooth()

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=show_wire)

        self._guids = [obj]
        return self.guids
