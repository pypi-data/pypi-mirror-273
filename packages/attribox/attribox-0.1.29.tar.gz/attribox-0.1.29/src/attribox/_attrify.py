"""Attrify decorates a custom class leaving a new class subclassing the
decorated class, and with the AttriClass.__dict__ as the class body."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriClass
from vistutils.waitaminute import typeMsg


class Attrify:
  """Attrify decorates a custom class leaving a new class subclassing the
  decorated class, and with the AttriClass.__dict__ as the class body."""

  __decorated_class__ = None

  def __init__(self, cls: type) -> None:
    """Initialize the Attrify class."""
    self._setDecoratedClass(cls)

  def _setDecoratedClass(self, cls: type) -> None:
    """Sets the decorated class. """
    if not isinstance(cls, type):
      e = typeMsg('cls', cls, type)
      raise TypeError(e)
    self.__decorated_class__ = cls

  def _getDecoratedClass(self, ) -> type:
    """Returns the decorated class. """
    if self.__decorated_class__ is None:
      e = """The decorated class has not been assigned. """
      raise AttributeError(e)
    return self.__decorated_class__

  def __call__(self, cls: type) -> type:
    """Returns a new class subclassing"""
    name = cls.__name__
    bases = (cls,)
    namespace = {**AttriClass.__dict__, }
    return type(name, bases, namespace)
