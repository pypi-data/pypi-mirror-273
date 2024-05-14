from .rsam import RsamEW

from pkg_resources import get_distribution

__version__ = get_distribution("rsam-ew").version
__author__ = "Martanto"
__author_email__ = "martanto@live.com"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024"
__url__ = "https://github.com/martanto/rsam-ew"

__all__ = [
    'RsamEW'
]