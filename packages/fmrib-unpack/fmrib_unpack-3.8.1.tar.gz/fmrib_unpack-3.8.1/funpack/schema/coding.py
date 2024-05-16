#!/usr/bin/env python
#
# coding.py - Loading files which contain descriptions for data coding values.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains the :func:`loadCodingFile` function, which can be used
to load descriptions of the values for a given data coding.


The data coding information for data codings in the UKBiobank is downloaded
from the UK Biobank showcase at
https://biobank.ctsu.ox.ac.uk/crystal/schema.cgi.  Some pre-downloaded backup
files are stored in in ``funpack/schema/coding/``.
"""


import                   logging
import functools      as ft
import os.path        as op
import pandas         as pd
import funpack.util   as util
import funpack.schema as schema


log = logging.getLogger(__name__)


def getCoding(dtable=None, vid=None, coding=None):
    """Return a data coding ID for the given ``vid`` or ``coding``. See the
    :func:`loadCodingFile` function for details.

    :arg dtable: The :class:`.DataTable`
    :arg vid:    The variable ID
    :arg coding: Data coding ID
    :return:     An integer ID for the corresponding data coding.
    """

    if (dtable is not None) and (vid is not None):
        coding = dtable.vartable.loc[vid, 'DataCoding']

    elif coding is None:
        raise ValueError('Either a datatable+vid, or a data '
                         'coding, must be specified')

    return int(coding)


def getCodingFilePath(coding):
    """Return a file path to a backup file for the given coding. The file
    is not guaranteed to exist.
    """
    return op.join(op.dirname(__file__), 'coding', f'coding{coding}.tsv')


@ft.lru_cache
def _loadCodingFile(coding, url, backupFile, download=True):
    """Called by :func:`loadCodingFile`. Downloads/loads a coding file.
    Results are cached via ``functools.lru_cache`` to prevent repeated
    downloading of the same files.
    """
    log.debug('Loading UKB coding scheme (%i)...', coding)
    loadFunc = ft.partial(pd.read_csv, delimiter='\t', index_col=0)
    return schema.downloadFile(url, backupFile, loadFunc, download)


def loadCodingFile(dtable=None, vid=None, coding=None, download=True):
    """Loads a UK Biobank data coding scheme.

    Coding files can be looked up with one of the following methods, in
    order of precedence:

     1. By specifying a data coding (``coding``). This takes precedence.
     2. By passing a :class:`.DataTable` (``dtable``) and variable ID (``vid``)

    The descriptions are returned in a ``pandas.DataFrame``, with the coding
    values as the index, and a single column called ``meaning``, containing
    the descriptions for each value.

    :arg dtable:   The :class:`.DataTable`
    :arg vid:      Variable ID
    :arg coding:   Data coding ID
    :arg download: Defaults to ``True`` - coding files are downloaded from
                   the UK Biobank showcase. Set to ``False`` to force loading
                   from the backup files in ``funpack/schema/coding/``.
    :return:       A ``DataFrame`` containing descriptions
    """
    coding = getCoding(dtable, vid, coding)
    url    = schema.codingFileUrl(coding)
    backup = getCodingFilePath(coding)
    return _loadCodingFile(coding, url, backup, download)
