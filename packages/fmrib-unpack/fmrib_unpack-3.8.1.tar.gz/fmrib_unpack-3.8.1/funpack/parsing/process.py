#!/usr/bin/env python
#
# process.py - The Process class, and functions for parsing processing steps.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The :class:`Process` class, and functions for parsing processing steps.

This module defines the :class:`Process` class which is used by the
:mod:`funpack.processing` module to run FUNPACK processing steps.
"""


import functools       as ft
import itertools       as it
import                    logging
import                    warnings
import                    collections
import collections.abc as abc

import pyparsing as pp

from funpack import custom


log = logging.getLogger(__name__)


class NoSuchProcessError(Exception):
    """Exception raised by the :class:`Process` class when an unknown
    process name is specified.
    """


class Process:
    """Simple class which represents a single processing step. The :meth:`run`
    method can be used to run the process on the data for one or more
    variables.
    """


    def __init__(self, ptype, name, args, kwargs, procstr):
        """Create a ``Process``.

        :arg ptype:   Process type - either ``cleaner`` or ``processor``
                      (see the :mod:`.custom` module).
        :arg name:    Process name
        :arg args:    Positional arguments to pass to the process function.
        :arg kwargs:  Keyword arguments to pass to the process function.
        :arg procstr: Input string containing the process specification.

        Any keyword arguments which begin with ``'broadcast_'`` are separated
        out the other keyword arguments, although note that broadcasting is
        deprecated and will be removed in FUNPACK 4.0.0. See the :meth:`run`
        method for more details.
        """

        bcastKwargs  = collections.OrderedDict()
        normalKwargs = collections.OrderedDict()

        for k, v in kwargs.items():
            if k.startswith('broadcast_'):
                warnings.warn(f'[{k}]: Broadcasting is deprecated, and '
                              'will be removed in FUNPACK 4.0.0 ',
                              DeprecationWarning)
                k              = '_'.join(k.split('_')[1:])
                bcastKwargs[k] = v
            else:
                normalKwargs[k] = v

        # cleaner functions are not
        # defined in processing_functions,
        # so in this case func will be None.
        self.__ptype         = ptype
        self.__name          = name
        self.__args          = args
        self.__kwargs        = normalKwargs
        self.__procstr       = procstr
        self.__bcastKwargs   = bcastKwargs
        self.__metaproc      = normalKwargs.pop('metaproc', None)


    def __repr__(self):
        """Return a string representation of this ``Process``."""
        args    = ','.join([str(v) for v in self.__args])
        kwargs  = ','.join([f'{k}={v}' for k, v in
                           it.chain(self.__kwargs.items(),
                                    self.__bcastKwargs.items())])

        allargs = [args, kwargs]
        allargs = [a for a in allargs if a != '']
        allargs = ', '.join(allargs)
        return f'{self.__name}[{self.__ptype}]({allargs})'


    @property
    def name(self):
        """Returns the name of this ``Process``. """
        return self.__name


    @property
    def args(self):
        """Returns the positional arguments for this ``Process``. """
        return self.__args


    @property
    def kwargs(self):
        """Returns the keyword arguments for this ``Process``. """
        return self.__kwargs


    @property
    def processString(self):
        """Returns the original string, from the processing table/
        command-line, which defines this ``Process``.
        """
        return self.__procstr


    @property
    def broadcastKwargs(self):
        """Returns the keyword arguments for this ``Process`` which
        will broadcasted across all variable IDs that are passed to
        an invocation of :meth:`run`.
        """
        return self.__bcastKwargs


    @property
    def filterMissing(self):
        """Return ``True`` if this processing function expects that the list of
        variable IDs which it is given will not contain the IDs of variables
        which are not present in the data.

        This property is set via a ``filterMissing`` argument passed to the
        processor decorator function. Its default value is ``True``.
        """
        return custom.args(self.__ptype, self.__name).get('filterMissing',
                                                          True)


    def auxillaryVariables(self, broadcastIndex=None):
        """Returns a list of "auxillary" variables for this process. Auxillary
        variables are variables which a process is not being applied to, but
        which is needed by the process. These variables are passed in as
        arguments to the process.

        The names of any arguments which contain auxillary variables are
        specified via the ``auxvids`` argument to the processor decorator
        function.
        """

        auxargs = custom.args(self.__ptype, self.__name).get('auxvids', [])
        auxvids = []

        for arg in auxargs:
            if arg in self.kwargs:
                val = self.kwargs[arg]
            elif ((broadcastIndex is not None) and
                  (arg in self.broadcastKwargs)):
                val = self.broadcastKwargs[arg][broadcastIndex]
            else:
                continue

            if isinstance(val, abc.Sequence): auxvids.extend(val)
            else:                             auxvids.append(val)

        return auxvids


    def run(self, *args, broadcastIndex=None):
        """Run the process on the data, passing it the given arguments,
        and any arguments that were passed to :meth:`__init__`.

        :arg broadcastIndex: Deprecated. If provided, and if any broadcast
                             arguments were specified for this process, this
                             index is used to retrieve one value each
                             broadcast argument list - this value is then
                             passed to the process function.
        """

        kwargs = self.__kwargs.copy()
        bcast  = self.__bcastKwargs

        # retrieve the value for each broadcast argument,
        # and pass them in as regular keyword arguments
        if broadcastIndex is not None and len(bcast) > 0:
            for k, v in bcast.items():
                kwargs[k] = v[broadcastIndex]

        result = custom.run(self.__ptype,
                            self.__name,
                            *args,
                            *self.__args,
                            **kwargs)

        if self.__metaproc is not None and \
           isinstance(result, tuple)   and \
           len(result) == 4:

            # The first argument to a process
            # should be the data table
            dtable = args[0]

            # The 3rd/4th args returned from a
            # process should be a list of vids,
            # and a list of Column kwargs for
            # each of them
            vids      = result[2]
            kwargs    = result[3]
            mproc     = self.__metaproc
            newkwargs = []

            for vid, vkwargs in zip(vids, kwargs):

                if vkwargs is None or 'metadata' not in vkwargs:
                    newkwargs.append(vkwargs)
                    continue

                try:
                    vkwargs['metadata'] = custom.runMetaproc(
                        mproc, dtable, vid, vkwargs['metadata'])
                    newkwargs.append(vkwargs)

                except Exception as e:
                    log.warning('Metadata processing function '
                                'failed (vid %u): %s', vid, e)
                    newkwargs.append(vkwargs)

            result = tuple(list(result[:3]) + [newkwargs])

        return result


def parseProcesses(procs, ptype):
    """Parses the given string containing one or more comma-separated process
    calls, as defined in the processing table. Returns a list of
    :class:`Process` objects.

    :arg procs: String containing one or more comma-separated (pre-)processing
                steps.

    :arg ptype: either ``cleaner`` or ``processor``

    :returns:   A list of :class:`Process` objects.

    """

    def makeProcess(toks):
        name = toks[0]

        args   = ()
        kwargs = {}

        if len(toks) == 2:
            if isinstance(toks[1], tuple):
                args   = toks[1]
            elif isinstance(toks[1], dict):
                kwargs = toks[1]
        elif len(toks) == 3:
            args, kwargs = toks[1:]

        if not custom.exists(ptype, name):
            raise NoSuchProcessError(name)

        return Process(ptype, name, args, kwargs, procs)

    parser = pp.delimitedList(makeProcessParser().setParseAction(makeProcess))

    try:
        parsed = parser.parseString(procs, parseAll=True)
    except Exception as e:
        log.error('Error parsing process list "%s": %s', procs, e)
        raise e

    return list(parsed)


@ft.lru_cache()
def makeProcessParser():
    """Generate a ``pyparsing`` parser which can be used to parse a single
    process call in the processing table.
    """

    lparen   = pp.Literal('(').suppress()
    rparen   = pp.Literal(')').suppress()
    lbracket = pp.Literal('[').suppress()
    rbracket = pp.Literal(']').suppress()

    def convertBoolean(tok):
        tok = tok[0]
        if   tok == 'True':  return True
        elif tok == 'False': return False
        else:                return tok

    def parseValList(toks):
        return [list(toks)]

    def parseArgs(toks):
        return [tuple(toks)]

    def parseKwargs(toks):
        kwargs = collections.OrderedDict()
        for i in range(0, len(toks), 2):
            kwargs[toks[i]] = toks[i + 1]
        return kwargs

    funcName = pp.pyparsing_common.identifier
    argval   = (pp.QuotedString('"')                                       ^
                pp.QuotedString("'")                                       ^
                pp.pyparsing_common.number                                 ^
                pp.oneOf(['True', 'False']).setParseAction(convertBoolean) ^
                pp.Literal('None').setParseAction(pp.replaceWith(None)))

    # argument values are either a
    # scalar, or a list of scalars
    # within square brackets
    vallist  = (lbracket + pp.delimitedList(argval) + rbracket)
    vallist  = vallist.setParseAction(parseValList)
    argval   = argval ^ vallist

    # arguments are either
    # positional or keyword
    kwargs   = (pp.pyparsing_common.identifier +
                pp.Literal('=').suppress() +
                argval)
    posargs  = pp.delimitedList(argval).setParseAction(parseArgs)
    kwargs   = pp.delimitedList(kwargs).setParseAction(parseKwargs)
    allargs  = pp.delimitedList(pp.Optional(posargs) + pp.Optional(kwargs))

    # function can be called as:
    #   function
    #   function()
    #   function(args)
    allargs  = lparen   + pp.Optional(allargs) + rparen
    function = funcName + pp.Optional(allargs)

    return function
