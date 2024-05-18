import sys

from funcy import lcat

from .reader import *
from .tmx_reader import *

modules = ("reader","tmx_reader")
__all__ = lcat(sys.modules["translation_readers." + m].__all__ for m in modules)

