#!/usr/bin/env python
#
# metaproc_functions.py - Functions for manipulating column metadata.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains ``metaproc`` functions - functions for manipulating
column metadata.

Some :class:`.Column` instances have a ``metadata`` attribute, containing some
additional information about the column. The functions in this module can be
used to modify these metadata values. Currently, column metadata is only used
to generate a description of each column (via the ``--description_file``
command-line option - see :func:`funpack.main.generateDescription`).

All ``metaproc`` functions must accept three arguments:

 - The :class:`.DataTable`

 - The variable ID associated with the column. This may be ``None``, if the
   column has been newly added, and is not associated with any other variable.

 - The metadata value.
"""


import           logging
import pandas as pd

import funpack.util             as util
import funpack.custom           as custom
import funpack.schema.coding    as coding
import funpack.schema.hierarchy as hierarchy


log = logging.getLogger(__name__)


@custom.metaproc('codingdesc')
def codingDescriptionFromValue(dtable, vid, val):
    """Generates a description for a value from a specific data coding. """

    log.debug('Generating coding description for [vid %s]: %s', vid, val)

    descs = coding.loadCodingFile(dtable, vid)

    # Reverse any categorical recoding
    # that may have been applied, so we
    # can get at the original value.
    # We make the assumption here that
    # metaproc functions are called
    # after categorical recoding.
    raw = dtable.vartable.at[vid, 'RawLevels']
    new = dtable.vartable.at[vid, 'NewLevels']

    if not pd.isna(new) and val in new:
        recoding = dict(zip(new, raw))
        val      = recoding[val]

    desc  = descs['meaning'][val]
    return '{} - {}'.format(val, desc)


@custom.metaproc('hierarchynumdesc')
def hierarchicalDescriptionFromNumeric(dtable, vid, val):
    """Generates a description for a hierarchical code which has been
    passed through the :func:`~.hierarchy.codeToNumeric` cleaning function.
    """
    val  = hierarchy.numericToCode(val, dtable=dtable, vid=vid)
    hier = hierarchy.loadHierarchyFile(dtable, vid)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)


@custom.metaproc('hierarchycodedesc')
def hierarchicalDescriptionFromCode(dtable, vid, val):
    """Generates a description for a hierarchical code (e.g. ICD10 code). """
    hier = hierarchy.loadHierarchyFile(dtable, vid)
    desc = hier.description(val)
    return '{} - {}'.format(val, desc)
