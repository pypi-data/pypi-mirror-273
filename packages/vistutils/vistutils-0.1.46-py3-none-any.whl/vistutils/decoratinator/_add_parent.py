"""AddParent replaces decorated  class with class that inherits from the
class given in the decorator constructor.

For example:
@AddParent(Parent)
class Child:
  pass

"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.decoratinator import AbstractDecorator
from vistutils.waitaminute import typeMsg


class AddParent(AbstractDecorator):
  """AddParent replaces decorated  class with class that inherits from the
  class given in the decorator constructor.

  For example:
  @AddParent(Parent)
  class Child:
    pass"""

  def _apply(self, decoratedClass: type) -> type:
    """Apply the AddParent decorator to the decorated class."""
    parent = self._getWrappedClass()
    if not isinstance(decoratedClass, type):
      e = typeMsg('decoratedClass', decoratedClass, type)
      raise TypeError(e)
    name = decoratedClass.__name__
    bases = (*decoratedClass.__bases__, parent)
    namespace = {**decoratedClass.__dict__, }
    return type(name, bases, namespace)
