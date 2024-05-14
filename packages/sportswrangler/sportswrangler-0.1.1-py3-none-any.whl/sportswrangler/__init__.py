from .odds import *
from .sports import *
from .utils import enums
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
