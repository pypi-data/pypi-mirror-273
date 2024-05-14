"""AbstractDecorator provides an abstract baseclass for decorators
instantiated on a wrapped class. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Optional

from vistutils.waitaminute import typeMsg


class AbstractDecorator:
  """AbstractDecorator provides an abstract baseclass for decorators
  instantiated on a wrapped class. """

  __wrapped_class__ = None

  def __init__(self, cls: Optional[type] = None, **kwargs) -> None:
    """Initialize the AbstractDecorator with the wrapped class."""
    if cls is not None:
      if not isinstance(cls, type):
        e = typeMsg('cls', cls, type)
        raise TypeError(e)
      self._setWrappedClass(cls)

  def _setWrappedClass(self, cls) -> None:
    """Setter-function for the wrapped class."""
    if self.__wrapped_class__ is not None:
      e = """The wrapped class has already been assigned!"""
      raise AttributeError(e)
    if not isinstance(cls, type):
      e = typeMsg('cls', cls, type)
      raise TypeError(e)
    self.__wrapped_class__ = cls

  def _getWrappedClass(self) -> type:
    """Getter-function for the wrapped class."""
    if self.__wrapped_class__ is None:
      e = """The wrapped class has not been assigned!"""
      raise AttributeError(e)
    return self.__wrapped_class__

  @abstractmethod
  def _apply(self, decoratedClass: type) -> type:
    """Decorates should implement this method to define the actual
    decoration. The object returned will take the place of the decorated
    class in the namespace. Typically, the return value is a new class,
    the same class having been augmented, but could also be a function. """

  def __call__(self, decoratedClass: type, ) -> type:
    """Alias for the _apply method"""
    return self._apply(decoratedClass)
