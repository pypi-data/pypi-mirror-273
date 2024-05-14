from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GeometryObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class TorusObject(GHSceneObject, GeometryObject):
    """Scene object for drawing torus shapes.

    Parameters
    ----------
    torus : :class:`compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, torus, **kwargs):
        super(TorusObject, self).__init__(geometry=torus, **kwargs)

    def draw(self):
        """Draw the torus associated with the scene object.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]
            List of created Rhino torus.

        """
        brep = conversions.torus_to_rhino_brep(self.geometry)
        brep.Transform(conversions.transformation_to_rhino(self.worldtransformation))

        self._guids = [brep]
        return self.guids
