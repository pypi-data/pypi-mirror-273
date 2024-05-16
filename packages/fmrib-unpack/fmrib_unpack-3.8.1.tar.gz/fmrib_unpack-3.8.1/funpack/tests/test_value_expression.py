#!/usr/bin/env python
#
# test_value_expression.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import functools       as ft
import itertools       as it
import multiprocessing as mp

import numpy  as np
import pandas as pd

import funpack.parsing as parsing
import funpack.util    as util


DATA = np.arange(-10, 11)
# expression[, data], result
TESTS = [
    ('max(1, 2, 3)',                3),
    ('min(1, 2, 3)',                1),
    ('max(min(1, 2, 3), 0)',        1),
    ('min(max(1, 2, 3), 0)',        0),
    ('min(max(1, 2, 3) + 5, 0)',    0),
    ('max(min(1, 2, 3) + 5, 0)',    6),
    ('max(1, 2, 3) + min(4, 5, 6)', 7),

    ('max()',               DATA, 10),
    ('max() + 1',           DATA, 11),
    ('min()',               DATA, -10),
    ('min() + 1',           DATA, -9),
    ('min(max() + 1, 15)',  DATA, 11),
    ('min(max() + 1, 5)',   DATA, 5),
    ('max(min() - 1, 0)',   DATA, 0),
    ('max(min() - 1, -20)', DATA, -11),

    ('1',   1),
    ('-1',  -1),
    ('10',  10),
    ('-10',  -10),
    ('0.5', 0.5),
    ('-0.5', -0.5),
]

def parse_test(test):
    if len(test) == 2:
        data = None
        expr, expect = test
    else:
        expr, data, expect = test

    return expr, data, expect


def test_ValueExpression():

    for test in TESTS:

        expr, data, expect = parse_test(test)

        assert parsing.ValueExpression(expr)(DATA) == expect

        # parsing expressions without a ValueExpression
        # object should result in the expression being
        # re-constructed
        parser = parsing.makeValueExpressionParser()
        parsed = parser.parseString(expr, parseAll=True)[0]

        # parsed may be a number for literals
        if isinstance(parsed, str): assert parsed == expr
        else:                       assert parsed == float(expr)



def test_parseValueExpressions():

    alltests = []
    allexprs = []

    for i in range(2, 6):

        perms = it.permutations(TESTS, i)

        for perm in perms:

            exprs = [t[0] for t in perm]
            exprs = ','.join(exprs)
            allexprs.append(exprs)
            alltests.append(perm)

    # randomly sample 1000 expression permutations
    sample   = np.random.choice(len(alltests), 1000)
    alltests = [alltests[i] for i in sample]
    allexprs = [allexprs[i] for i in sample]

    pool       = mp.Pool()
    allresults = pool.map(ft.partial(parsing.parseValueExpressions,
                                     ctype=util.CTYPES.continuous), allexprs)

    for exprs, tests, results in zip(allexprs, alltests, allresults):

        for test, result in zip(tests, results):

            expr, data, expect = parse_test(test)

            try:
                float(expr)
                literal = True
            except Exception:
                literal = False

            if literal: assert expect == result
            else:       assert expect == result(data)


def test_parseValueExpressions_types():

    datedata = pd.to_datetime(['1991-01-01',
                               '1992-01-01',
                               '1993-01-01'])
    textdata = ['X', 'Y', 'Z']

    # expr, data, type, expect
    tests = [
        ('1990-01-01,min()', datedata, util.CTYPES.date,
         pd.to_datetime(['1990-01-01', '1991-01-01'])),
        ('X,Y,17,max()',     textdata, util.CTYPES.text,
         ['X', 'Y', '17', 'max()']),
    ]

    for exprs, data, ctype, expect in tests:
        results = parsing.parseValueExpressions(exprs, ctype)

        for i, r in enumerate(results):
            if isinstance(r, parsing.ValueExpression):
                results[i] = r(data)

        for r, e in zip(results, expect):
            assert r == e
