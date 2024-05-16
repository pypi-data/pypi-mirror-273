#!/usr/bin/env python
#
# test_metaproc.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import random
import textwrap as tw
from unittest import mock

import pandas as pd
import numpy  as np

import funpack.metaproc_functions as metaproc
import funpack.schema.hierarchy as hierarchy
import funpack.custom as custom

from funpack.util import tempdir

from . import clear_plugins, gen_DataTable, patch_logging


@clear_plugins
@patch_logging
def test_codingDescriptionFromValue():

    custom.registerBuiltIns()

    codings      = [30, 40, 50, 20, 60, 10]
    meanings     = [f'meaning {c}' for c in codings]
    meanings[-1] = f'{meanings[-1]} hah'
    coding = pd.DataFrame(
       {'coding'  : codings,
        'meaning' : meanings}).set_index('coding')

    dt = gen_DataTable([np.random.randint(1, 10, 10)])

    dt.vartable.loc[1, 'DataCoding'] = 123

    func = custom.get('metaproc', 'codingdesc')

    with mock.patch('funpack.schema.coding.loadCodingFile',
                    return_value=coding):
        assert func(dt, 1, 30) == '30 - meaning 30'
        assert func(dt, 1, 10) == '10 - meaning 10 hah'


@clear_plugins
@patch_logging
def test_hierarchicalDescriptionFromX():

    custom.registerBuiltIns()

    codings    = ['a', 'b', 'c', 'd', 'e']
    meanings   = [f'{c} desc' for c in codings]
    node_ids   = [5, 1, 3, 4, 2]
    parent_ids = [0, 5, 5, 3, 1]
    hier       = hierarchy.Hierarchy(node_ids, parent_ids, codings, meanings)

    dt = gen_DataTable([np.random.randint(1, 10, 10)])

    dt.vartable.loc[1, 'DataCoding'] = 123

    numfunc  = custom.get('metaproc', 'hierarchynumdesc')
    codefunc = custom.get('metaproc', 'hierarchycodedesc')

    with mock.patch('funpack.schema.hierarchy.loadHierarchyFile',
                    return_value=hier):
        assert codefunc(dt, 1, 'a') == 'a - a desc'
        assert codefunc(dt, 1, 'c') == 'c - c desc'
        assert numfunc( dt, 1,  5)  == 'a - a desc'
        assert numfunc( dt, 1,  3)  == 'c - c desc'
