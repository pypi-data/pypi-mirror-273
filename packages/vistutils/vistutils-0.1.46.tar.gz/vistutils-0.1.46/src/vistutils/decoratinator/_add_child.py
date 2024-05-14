"""AddChild replaces decorated class with class that inherits from the
decorated class and the class body from the class given in the decorator
constructor. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.decoratinator import AbstractDecorator
from vistutils.waitaminute import typeMsg


class AddChild(AbstractDecorator):
  """AddChild replaces decorated class with class that inherits from the
  decorated class and the class body from the class given in the decorator
  constructor. """

  def _apply(self, decoratedClass: type) -> type:
    """Apply the AddChild decorator to the decorated class."""
    child = self._getWrappedClass()
    if not isinstance(decoratedClass, type):
      e = typeMsg('decoratedClass', decoratedClass, type)
      raise TypeError(e)
    name = decoratedClass.__name__
    bases = (decoratedClass,)
    namespace = {**child.__dict__, }
    return type(name, bases, namespace)
