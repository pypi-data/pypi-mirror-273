"""MidClass provides a class decorator implementing functionality
otherwise requiring custom metaclass implementations.

Instantiate the MidClass with a name and a callable. The given name will
then point to the callable as if the callable was a method of the metaclass.
It is possible to use the MidClass with custom class derived from a custom
metaclass. However, if a custom metaclass is already in use, placing the
method directly on the metaclass provides the same functionality in a much
better way.

Example use case: Improvement on __str__ as it applies to a custom class
itself.

The 'correct' solution would be to implement a custom metaclass that
reimplements the type.__str__ method. While powerful, when dealing with
external packages that make use of custom metaclass implementations
themselves, the resulting multiple metaclass conflicts introduce
significant complexities. Further, despite the improved error handling in
recent python edition, these have yet to reach metaclass implementations.

The MidClass decorator allows for inserting methods into the class that
function as though they were bound methods on the class. Let 'newStr' be
a callable receiving a type as the only argument, for example:

def newStr(cls: type) -> str:
  if hasattr(cls, '__qualname__'):
    return cls.__qualname__
  if hasattr(cls, '__name__'):
    return cls.__qualname__
  return type.__str__(cls)  # fallback to parent method

@MidClass('__str__', newStr)
class SomeClass(metaclass=type):
  ...

The above code will bring significant improvements to the way classes
represents themselves as strings.


"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import MethodType
from typing import Callable

from vistutils.decoratinator import AbstractDecorator
from vistutils.waitaminute import typeMsg


class MidClass(AbstractDecorator):
  """MidClass provides a class decorator implementing functionality
  otherwise requiring custom metaclass implementations. """

  __attribute_name__ = None
  __replacement_method__ = None

  def __init__(self, *args) -> None:
    """Initialize the MidClass with the attribute name and the replacement
    method."""
    AbstractDecorator.__init__(self, )
    for arg in args:
      if isinstance(arg, str) and self.__attribute_name__ is None:
        self._setAttributeName(arg)
      elif callable(arg) and self.__replacement_method__ is None:
        self._setReplacementMethod(arg)

  def _setAttributeName(self, attributeName: str) -> None:
    """Set the attribute name of the MidClass object."""
    if self.__attribute_name__ is not None:
      e = """The attribute name has already been assigned!"""
      raise AttributeError(e)
    self.__attribute_name__ = attributeName

  def _getAttributeName(self) -> str:
    """Getter-function for the attribute name."""
    if self.__attribute_name__ is None:
      e = """The attribute name has not been assigned!"""
      raise AttributeError(e)
    return self.__attribute_name__

  def _setReplacementMethod(self, callMeMaybe: callable) -> None:
    """Set the replacement method of the MidClass object."""
    if self.__replacement_method__ is not None:
      e = """The replacement method has already been assigned!"""
      raise AttributeError(e)
    if callable(callMeMaybe):
      self.__replacement_method__ = callMeMaybe
    else:
      e = typeMsg('callMeMaybe', callMeMaybe, Callable)
      raise TypeError(e)

  def _getReplacementMethod(self, ) -> callable:
    """Getter-function for the replacement method."""
    if self.__replacement_method__ is None:
      e = """The replacement method has not been assigned!"""
      raise AttributeError(e)
    return self.__replacement_method__

  def _apply(self, decoratedClass: type) -> type:
    """Apply the MidClass decorator to the decorated class."""
    if not isinstance(decoratedClass, type):
      e = typeMsg('decoratedClass', decoratedClass, type)
      raise TypeError(e)
    name = self._getAttributeName()
    repFunc = self._getReplacementMethod()
    if repFunc is None:
      e = """The replacement method has not been assigned!"""
      raise AttributeError(e)
    if not callable(repFunc):
      e = typeMsg('replacement', repFunc, Callable)
      raise TypeError(e)
    replacement = MethodType(repFunc, decoratedClass)
    setattr(decoratedClass, name, replacement)
    return decoratedClass
