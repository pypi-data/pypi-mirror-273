"""The 'decoratinator' package provides decorators for use with custom
classes primarily aimed at providing functionalities that otherwise would
require custom metaclass implementations. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._abstract_decorator import AbstractDecorator
from ._add_parent import AddParent
from ._add_child import AddChild
from ._mid_class import MidClass
from ._who_dat import WhoDat
