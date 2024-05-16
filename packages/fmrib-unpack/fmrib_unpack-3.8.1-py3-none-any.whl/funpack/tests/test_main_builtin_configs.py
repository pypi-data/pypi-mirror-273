#!/usr/bin/env python
#
# test_main_builtin_configs.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import numpy  as np
import pandas as pd

import funpack.main as main

from . import tempdir, patch_logging


@patch_logging
def test_main_fmrib(cfg='fmrib_logs'):

    # Just checking one rule - categorical recoding
    # from datacodings_recoding.tsv for datacoding
    # 100002 / variable  100900: 555,1,2,300 -> 0.5,1,2,3
    # 111 is discarded
    mappings = {
        555 : 0.5,
        1   : 1,
        2   : 2,
        300 : 3,
        111 : np.nan
    }


    eids = np.arange(1, 101)
    vals = np.random.choice(list(mappings.keys()), 100)
    exp  = np.array([mappings[v] for v in vals])
    data = pd.DataFrame({'eid' : eids, '100900-0.0' : vals}).set_index('eid')
    exp  = pd.DataFrame({'eid' : eids, '100900-0.0' : exp}) .set_index('eid')

    with tempdir():
        data.to_csv('data.csv')

        main.main('-cfg {} out.tsv data.csv'.format(cfg).split())

        got = pd.read_csv('out.tsv', delimiter='\t', index_col=0)

        assert got.columns == ['100900-0.0']
        exp = exp['100900-0.0']
        got = got['100900-0.0']

        namask = got.isna()
        assert (got.isna()   == exp.isna())  .all()
        assert (got[~namask] == exp[~namask]).all()
