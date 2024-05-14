from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import SceneObject


class GHSceneObject(SceneObject):
    """Base class for all GH scene objects."""

    def __init__(self, **kwargs):
        super(GHSceneObject, self).__init__(**kwargs)
