from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class CapsuleObject(GHSceneObject, GeometryObject):
    """Scene object for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, capsule, **kwargs):
        super(CapsuleObject, self).__init__(geometry=capsule, **kwargs)

    def draw(self):
        """Draw the capsule associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino breps.

        """
        breps = conversions.capsule_to_rhino_brep(self.geometry)
        transformation = conversions.transformation_to_rhino(self.transformation)
        for geometry in breps:
            geometry.Transform(transformation)

        self._guids = breps
        return self.guids
