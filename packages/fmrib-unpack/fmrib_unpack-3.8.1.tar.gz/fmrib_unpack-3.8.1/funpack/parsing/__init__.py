#!/usr/bin/env python
#
# __init__.py - Logic for parsing expressions.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""Logic for parsing expressions.

The ``funpack.parsing`` package contains logic for parsing different types
of expressions that are used throughout FUNPACK. This includes:

  - Subject inclusion expressions (see the ``--subject`` command-line option,
    and the :func:`funpack.importing.filter.filterSubjects` function).

  - Parent value expressions (see the ``--child_values`` command-line option,
    and the :func:`funpack.cleaning.applyChildValues` function).

  - Processing functions (see the :mod:`funpack.processing` module).

  - Recoding valu expressions (see the ``--recoding`` command-line option,
    and the :func:`funpack.cleaning.applyNewLevels` function).
"""


from funpack.parsing.variable_expression import (
    VariableExpression,
    parseVariableExpression,
    variablesInExpression,
    calculateVariableExpressionEvaluationOrder)


from funpack.parsing.value_expression import (
    parseValueExpressions,
    ValueExpression,
    makeValueExpressionParser)


from funpack.parsing.process import (
    NoSuchProcessError,
    Process,
    parseProcesses,
    makeProcessParser)
