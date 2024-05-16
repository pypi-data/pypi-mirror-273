#!/usr/bin/env python
#
# value_expression.py - Logic for parsing value expressions used in categorical
#                       recoding/replacement rules.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""Logic for parsing categorical recoding/replacement values.

The ``--recoding`` command-line option, also specified via the ``RawLevels`` /
``NewLevels`` columns in the variable table, accepts both literal values, and
value expressions.

As an example of literal values, this option would cause FUNPACK to replace
values ``555`` and ``444`` with ``0.5``and ``4`` respectively, in the data field
123::

    --recoding 123 "555,444" "0.5,4"

As an example of value expressions, this option would cause FUNPACK to replace
the value "-818" with one plus the data maximum in data-field 123::

    --recoding 123 "-818" "1 + max()"

This module contains the logic used to parse and evaluate these value
expressions.

Value expressions can use the following functions and binary operators.
Both functions and operators accept numbers and other expressions as arguments:

 - ``min()``: If called without arguments (i.e. ``min()``), returns the minimum
              of the input data. Otherwise returns the minimum of the
              arguments, e.g. ``min(1,2,3,4)``

 - ``max()``: If called without arguments (i.e. ``max()``), returns the maximum
              of the input data. Otherwise returns the maximum of the
              arguments, e.g. ``max(1,2,3,4)``

 - ``+``:     Adds two operands, e.g. ``1 + 2``

 - ``-``:     Subtracts two operands, e.g. ``1 - 2``

 - ``*``:     Multiplies two operands, e.g. ``1 * 2``

 - ``/``:     Divides two operands, e.g. ``1 / 2``


The :func:`parseValueExpressions` function is the primary function provided
by this module. It accepts a string containing a comma-separated sequence of
literal values and value expressions, and will return a list containing those
literal values, and :class:`ValueExpression` objects for each expression.


A :class:`ValueExpression` object can be invoked on some data to evaluate
the expression on that data.
"""


import              enum
import functools as ft
import              logging

from typing import Any, List, Sequence, Union

import numpy     as np
import pandas    as pd
import pyparsing as pp

import funpack.util as util


log = logging.getLogger(__name__)


Literal = Union[float, int, str]
"""Type representing a literal primitive value. """


class ValueExpression:
    """Class which parses and evaluates a single value expression.

    ``ValueExpression`` objects are created by the :func:`parseValueExpression`
    function. A ``ValueExpression`` object can be called with some data to
    evaluate the expression against that data.
    """


    def __init__(self, expr : str):
        """Create a ``ValueExpression`` object.

        :arg expr: String containing the expression.
        """

        parser = makeValueExpressionParser(self)

        self.__data    = None
        self.__rawexpr = expr
        self.__expr    = parser.parseString(expr, parseAll=True)[0]


    @property
    def expression(self) -> str:
        """Return the expression string that this ``ValueExpression`` will
        evaluate.
        """
        return self.__rawexpr


    def __str__(self):
        """Return the expression string that this ``ValueExpression`` will
        evaluate.
        """
        return self.__rawexpr


    def __repr__(self):
        """Return the expression string that this ``ValueExpression`` will
        evaluate.
        """
        return self.__rawexpr


    def __call__(self, data : Sequence):
        """Evaluate the expression on some data. """
        self.__data = data

        try:
            # If the original expression was a literal,
            # e.g. "25", we can just return it as-is.
            # Otherwise it is evaluated.
            if callable(self.__expr): return self.__expr()
            else:                     return self.__expr
        except Exception as e:
            log.error(f'Error evaluating expression "{self.expression}" on '
                      f'data: {data}')
            raise e


    def __eval(self, value):
        """Evaluate a function/operator argument. Called by the functions/
        binary operators. If the value is a literal it is returned unchanged.
        Otherwise it is assumed to be another function/statement, in which
        case it is evaluated, and the result returned.
        """
        if np.issubdtype(type(value), np.number): return value
        else:                                     return value()


    def min(self, *vals):
        """Evaluates ``min([values])``. Return the minimum of vals. If no
        values are specified, returns the minimum of the data set.
        """
        vals = [self.__eval(v) for v in vals]
        if len(vals) == 0: return np.asanyarray(self.__data).min()
        else:              return np.array(vals).min()


    def max(self, *vals):
        """Evaluates ``max([values])``. Return the maximum of vals. If no
        values are specified, returns the maximum of the data set.
        """
        vals = [self.__eval(v) for v in vals]
        if len(vals) == 0: return np.asanyarray(self.__data).max()
        else:              return np.array(vals).max()


    def add(self, v1, v2):
        """Evaluates ``v1 + v2``. """
        return self.__eval(v1) + self.__eval(v2)


    def sub(self, v1, v2):
        """Evaluates ``v1 - v2``. """
        return self.__eval(v1) - self.__eval(v2)


    def mul(self, v1, v2):
        """Evaluates ``v1 * v2``. """
        return self.__eval(v1) * self.__eval(v2)


    def div(self, v1, v2):
        """Evaluates ``v1 / v2``. """
        return self.__eval(v1) / self.__eval(v2)


def parseValueExpressions(
        exprs : str,
        ctype : enum.Enum,
) -> List[Union[ValueExpression, Literal]]:
    """Parse a comma-separated sequence of value expressions/literal values.

    Returns a list containing literal values and :class:`ValueExpression`
    objects - these can be used to evaluate each expression against some
    data at a later point in time.

    :arg exprs: String containing a comma-separated sequence of
                value expressions/literal values

    :arg ctype: UKBiobank data type of the data-field against which the
                expressions will be applied. Used to infer a suitable
                data type into which any literal values will be coerced.
    """

    dtype = util.DATA_TYPES.get(ctype, np.float32)

    # Value expressions are not supported
    # for non-numeric/date types so
    # parsing is not necessary.
    if not (np.issubdtype(dtype, np.number) or
            np.issubdtype(dtype, np.datetime64)):
        return [w.strip() for w in exprs.split(',')]

    # We parse the string in two-passes. The
    # first pass is to split up the comma-
    # separated list. This can't be done
    # naively, as value expressions may
    # themselves contain commas.
    parser = pp.delimitedList(makeValueExpressionParser())
    try:
        exprs = parser.parseString(exprs, parseAll=True)
    except Exception as e:
        raise ValueError(f'Could not parse value expression {exprs}') from e

    # In the second pass, we re-parse each
    # expression invididually. We attempt to coerce
    # each item to its target data type and, failing
    # that, assume that it is a value expression.
    #
    # All numeric types are coerced to floating
    # point, as most data fields are stored as
    # floats anyway, and this allows for insertion
    # of non-integer values into otherwise integral
    # data fields (e.g. replacing "555" with "0.5")
    # in the categorical recoding step).
    for i, e in enumerate(exprs):
        try:
            if ctype in (util.CTYPES.date, util.CTYPES.time):
                exprs[i] = pd.to_datetime(e)
            else:
                exprs[i] = float(e)
        # Any values which cannot be coerced to the target
        # data type are assumed to be value expressions,
        # e.g. "max()+1".  They are parsed and replaced
        # with a ValueExpression object which can be used
        # to evaluate them later on.
        except Exception:
            exprs[i] = ValueExpression(e)

    return exprs


def makeValueExpressionParser(valexpr : ValueExpression = None) -> Any:
    """Create a ``pyparsing`` parser which can be used to evaluate a
    value expression.

    If ``valexpr is not None``, it must be a :class:`ValueExpression` instance.
    In this case, the parser will produce a callable object which can be
    evaluated by ``valexpr``. The callable is for the exclusive use of
    ``valexpr``, as the functions/expressions contained within will be bound to
    methods of ``valexpr``.

    If ``valexpr is None``, the returned parser can still be used, but will
    just re-construct the expression as a string. This sounds pointless, but it
    is used by the :func:`parseValueExpressions` function, to parse
    comma-separated sequences of expressions.
    """

    # Parses "func(*args)"
    def parseFunction(tkns):

        func = tkns[0]
        args = tkns[1:]

        if valexpr is None:
            args = ', '.join([str(a) for a in args])
            return f'{func}({args})'

        if   func == 'min': func = valexpr.min
        elif func == 'max': func = valexpr.max
        return ft.partial(func, *args)

    # Parses "a op b"
    def parseBinary(tkns):

        arg1, func, arg2 = tkns[0]

        if valexpr is None:
            return f'{arg1} {func} {arg2}'

        if   func == '+': func = valexpr.add
        elif func == '-': func = valexpr.sub
        elif func == '*': func = valexpr.mul
        elif func == '/': func = valexpr.div
        return ft.partial(func, arg1, arg2)

    # expr represents numbers, functions, and
    # binary expressions. Forward-define, as
    # expressions can be used as function
    # arguments and operands in binary
    # expressions.
    expr      =  pp.Forward()
    lparen    =  pp.Literal('(').suppress()
    rparen    =  pp.Literal(')').suppress()
    primitive = (pp.pyparsing_common.number      ^
                 pp.Word(pp.alphanums + '_-:+.') ^
                 pp.QuotedString('"')            ^
                 pp.QuotedString("'"))

    # Functions are of the form "func([arg, ...])",
    # where arg can be numbers, functions, or
    # binary expressions.
    funcName = pp.oneOf(('min', 'max'))
    funcArgs = pp.Optional(pp.delimitedList(expr))
    funcExpr = funcName + lparen - funcArgs + rparen
    funcExpr = funcExpr.setParseAction(parseFunction)

    # infixNotation handles all of the
    # grouping/precedence logic. We
    # don't need to handle non-numeric
    # literals, as value expressions are
    # only applicable to numeric/datetime
    # data.
    binary = pp.oneOf(('+', '-', '*', '/'))
    expr <<= pp.infixNotation(
        primitive ^ funcExpr,
        [(binary, 2, pp.opAssoc.LEFT, parseBinary)])

    return expr
