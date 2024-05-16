#!/usr/bin/env python
#
# test_coding.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import textwrap as     tw
import os.path  as     op
from   unittest import mock

import numpy as np

import funpack.schema.coding as coding

from funpack.util import tempdir
from .            import gen_DataTable


def test_getCoding():
    dt = gen_DataTable([np.random.randint(1, 10, 10)])
    dt.vartable.loc[1, 'DataCoding'] = 4
    assert coding.getCoding(dt, 1)    == 4
    assert coding.getCoding(coding=4) == 4


def test_getCodingFilePath():
    exp = op.join(op.dirname(coding.__file__), 'coding', 'coding1.tsv')
    assert coding.getCodingFilePath(1)  == exp


def test_loadCodingFile():
    descs = tw.dedent("""
    coding	meaning
    30	meaning 30
    40	meaning 40
    50	meaning 50
    20	meaning 20
    60	meaning 60
    10	meaning 10
    """).strip()

    with tempdir():
        with open('descs.txt', 'wt') as f:
            f.write(descs)
        with mock.patch('funpack.schema.coding.getCodingFilePath',
                        return_value=op.abspath('descs.txt')):
            d = coding.loadCodingFile(coding=10, download=False)
        assert d.loc[30, 'meaning'] == 'meaning 30'
