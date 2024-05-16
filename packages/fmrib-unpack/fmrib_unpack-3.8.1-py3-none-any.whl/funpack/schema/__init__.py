#!/usr/bin/env python
#
# __init__.py - UKB showcase schema
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The ``funpack.schema`` package contains functions for retrieving UK BioBank
showcase schema files which contain metadata describing all UKB data fields
and encoding schemes.
"""


import                   logging
import os.path        as op
import functools      as ft
import urllib.request as urlrequest

import pandas         as pd

import funpack.util   as util

from typing import Any, Callable


log = logging.getLogger(__name__)


DOWNLOAD = True
"""Flag used to enable/disable schema file downloads."""


NEVER_DOWNLOAD = False
"""Global override which disables schema file downloads. If ``True``, files
are never downloaded. This flag takes precedence over the :attr:`DOWNLOAD`
flag - it is intended to be used for testing purposes.
"""


def shouldDownload():
    """Used by :func:`downloadFile`. Returns ``True`` if schema files should
    be downloaded, or ``False``if off-line copies should be used instead.
    """
    return (not NEVER_DOWNLOAD) and DOWNLOAD


def fieldUrl() -> str:
    """Return a URL to download a file containing UKB "Data field properties".
    This file contains meta data about all UKB data fields.
    """
    return  'https://biobank.ctsu.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=1'


def encodingUrl() -> str:
    """Return a URL to download a file containing UKB "Encoding dictionaries".
    This file contains meta data about the encoding schemes used by all UKB
    categorical variables.
    """
    return 'https://biobank.ctsu.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=2'


def codingFileUrl(coding : int) -> str:
    """Return a URL to download a file containing the data coding for the
    specified UKB encoding scheme.
    """
    return f'https://biobank.ctsu.ox.ac.uk/crystal/codown.cgi?id={coding}'


@ft.lru_cache
def loadFieldProperties(download : bool = True) -> pd.DataFrame:
    """Downloads and loads the UKB data field properties file, returning
    it as a ``pandas.DataFrame``.
    """
    url    = fieldUrl()
    backup = op.join(op.dirname(__file__), 'field.txt')
    load   = ft.partial(pd.read_csv, delimiter='\t')
    log.debug('Loading UKB data field properties (field.txt)...')
    return downloadFile(url, backup, load, download)


@ft.lru_cache
def loadEnodingDictionaries(download : bool = True) -> pd.DataFrame:
    """Downloads and loads the UKB encoding dictionaries file, returning
    it as a ``pandas.DataFrame``.
    """
    url    = encodingUrl()
    backup = op.join(op.dirname(__file__), 'encoding.txt')
    load   = ft.partial(pd.read_csv, delimiter='\t')
    log.debug('Loading UKB encoding dictionaries (encoding.txt)...')
    return downloadFile(url, backup, load, download)


def downloadFile(url        : str,
                 backupFile : str,
                 loadFunc   : Callable,
                 download   : bool = True) -> Any:
    """Download a file from url, loading it using ``loadFunc``.

    If the download fails, or if ``download is True``, the file is loaded from
    a local ``backupFile`` instead.
    """

    download = download and shouldDownload()

    # Path to local file
    if op.exists(url):
        url = 'file:' + urlrequest.pathname2url(op.abspath(url))

    with util.tempdir():
        try:
            if download:
                log.debug('Downloading %s ...', url)
                with urlrequest.urlopen(url)  as inf, \
                     open('file.txt', 'wb')  as outf:
                    outf.write(inf.read())
                fname = 'file.txt'
            else:
                raise Exception('Force-loading from backup')

        except Exception as e:
            fname = backupFile
            log.warning('Unable to download file from %s - attempting '
                        'to load back-up from %s (%s)', url, fname, e)

        return loadFunc(fname)
