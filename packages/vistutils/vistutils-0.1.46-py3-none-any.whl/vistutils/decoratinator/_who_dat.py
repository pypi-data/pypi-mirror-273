"""WhoDat replaces"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Optional, Any

from icecream import ic

from vistutils.decoratinator import MidClass
from vistutils.waitaminute import typeMsg

ic.configureOutput(includeContext=True)


class WhoDat(MidClass):
  """WhoDat replaces"""

  @staticmethod
  def _newStrFactory() -> Callable:
    """Creates the new __str__ method for the decorated class."""

    def __str__(cls: type) -> str:
      """The new __str__ method for the decorated class."""
      for attrName in ['__qualname__', '__name__']:
        if hasattr(cls, attrName):
          name = getattr(cls, attrName)
          if isinstance(name, str):
            return name
          e = typeMsg('name', name, str)
          raise TypeError(e)
      else:
        return type.__str__(cls)

    def lmao(cls: type) -> str:
      return cls.__qualname__

    return lmao

  def __init__(self, *args, **kwargs) -> None:
    super().__init__()
    self._setAttributeName('__str__')
    self._setReplacementMethod(self._newStrFactory())

  def _apply(self, cls: type) -> type:
    """Apply the WhoDat decorator to the decorated class."""
    cls = super()._apply(cls)
    ic(cls.__str__)
    return cls
