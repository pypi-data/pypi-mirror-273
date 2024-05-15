"""AttriVault implements an alternative to AttriBox without automatic
instantiating. Instead, __get__ returns the class itself. The owning class
is expected to instantiate the class. To aid the owning class, AttriVault
allows for arguments to be passed to the owning class as well as arguments
to the class instantiation process.

For example:


class OwnedClass:
  # just any custom class


class Owner:

  name = AttriVault[OwnedClass](*args, **kwargs)

  @name.CREATE(*args2, **kwargs2)
  def createName(self, *args, **kwargs) -> Any:  # instance of OwnedClass
    # args and kwargs are passed to the OwnedClass constructor
    # args2 and kwargs2 are passed to the CREATE method
    # The Owner class is free to specify the creation process. By having
    # separate sets of arguments, the OwnedClass may require specific
    # instantiation arguments, while different owners may require
    # different arguments. The owner class is required to specific a
    ¤ CREATE method with the convenient decorator.
"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from vistutils.metas import AbstractMetaclass
from vistutils.waitaminute import typeMsg


class MetaVault(AbstractMetaclass):
  """MetaVault is a metaclass for AttriVault. """

  __owned_class__ = None
  __pos_args__ = None
  __kw_args__ = None

  def _setOwnedClass(cls, owned: type) -> None:
    """Sets the owned class. """
    if cls.__owned_class__ is not None:
      e = """The owned class has already been assigned. """
      raise AttributeError(e)
    if not isinstance(owned, type):
      e = typeMsg('owned', owned, type)
      raise TypeError(e)
    cls.__owned_class__ = owned

  def _setPosArgs(cls, *args) -> None:
    """Sets the positional arguments. """
    if cls.__pos_args__ is not None:
      e = """The positional arguments have already been assigned. """
      raise AttributeError(e)
    cls.__pos_args__ = args

  def _setKwArgs(cls, **kwargs) -> None:
    """Sets the keyword arguments. """
    if cls.__kw_args__ is not None:
      e = """The keyword arguments have already been assigned. """
      raise AttributeError(e)
    cls.__kw_args__ = kwargs

  def __getitem__(cls, owned: type) -> Any:
    """Returns a new AttriVault class. """

  def __call__(cls, *args, **kwargs) -> type:
    """Calling the class returns the AttriVault class itself"""
    cls._setPosArgs(*args)
    cls._setKwArgs(**kwargs)
    return cls
