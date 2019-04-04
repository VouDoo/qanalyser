#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Qanalyser
    ~~~~~~~~~

    Qanalyser analyzes queries in databases.

    :copyright: (c) 2019 by Maxence Grymonprez.
    :license: GNU General Public License v3.0, see LICENSE for more details.
"""

from .utils.version import get_version

VERSION = {
    'major': 0,
    'minor': 3,
    'micro': 0,
    'release': 'alpha',  # "alpha", "beta", "release-candidate" or "final"
    'relnum': 0,
    'post': False,  # True if in post-release, else False
    'postnum': 0,
    'dev': True,  # True if in development, else False
    'devnum': 0
}

__version__ = get_version()
__author__ = 'Maxence Grymonprez <maxgrymonprez@live.fr>'
__copyright__ = 'Copyright (c) 2019 by Maxence Grymonprez'
__license__ = 'GPLv3'
