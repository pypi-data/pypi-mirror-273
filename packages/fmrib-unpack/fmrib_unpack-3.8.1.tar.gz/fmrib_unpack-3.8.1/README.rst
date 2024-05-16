**FUNPACK** - the FMRIB UKBioBank Normalisation, Parsing And Cleaning Kit
=========================================================================


.. image:: https://img.shields.io/pypi/v/fmrib-unpack.svg
   :target: https://pypi.python.org/pypi/fmrib-unpack/

.. image:: https://anaconda.org/conda-forge/fmrib-unpack/badges/version.svg
   :target: https://anaconda.org/conda-forge/fmrib-unpack


.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1997626.svg
   :target: https://doi.org/10.5281/zenodo.1997626

.. image:: https://git.fmrib.ox.ac.uk/fsl/funpack/badges/master/coverage.svg
   :target: https://git.fmrib.ox.ac.uk/fsl/funpack/commits/master/


**FUNPACK** is a Python library for pre-processing of UK BioBank data.


    FUNPACK is developed at the Wellcome Centre for Integrative Neuroimaging
    (WIN@FMRIB), University of Oxford. FUNPACK is in no way endorsed,
    sanctioned, or validated by the `UK BioBank
    <https://www.ukbiobank.ac.uk/>`_.

    FUNPACK comes bundled with metadata about the variables present in UK
    BioBank data sets. This metadata can be obtained from the `UK BioBank
    online data showcase <https://biobank.ctsu.ox.ac.uk/showcase/index.cgi>`_


Installation
------------


Install FUNPACK from ``conda-forge``::

    conda install -c conda-forge fmrib-unpack


Or using ``pip``::

    pip install fmrib-unpack



The FUNPACK source code can be found at
https://git.fmrib.ox.ac.uk/fsl/funpack/.


Introductory notebook
---------------------


The ``funpack_demo`` command will start a Jupyter Notebook which introduces
the main features provided by FUNPACK. A non-interactive version of this
notebook can be found at
https://open.win.ox.ac.uk/pages/fsl/funpack/demo.html.

If you are using ``pip``, you need to install a few additional dependencies::

    pip install fmrib-unpack[demo]


You can then start the demo by running ``fmrib_unpack_demo``.


.. note:: The introductory notebook uses ``bash``, so is unlikely to work on
          Windows.


Usage
-----


General usage is as follows::

    fmrib_unpack [options] output.tsv input1.tsv input2.tsv


You can get information on all of the options by typing ``fmrib_unpack --help``.

    The `fmrib_unpack` command was called `funpack` in older versions of
    FUNPACK, but was changed to `fmrib_unpack` in 3.0.0 to avoid a naming
    conflict with an `unrelated software package
    <https://heasarc.gsfc.nasa.gov/fitsio/>`_.


Options can be specified on the command line, and/or stored in a configuration
file. For example, the options in the following command line::

    fmrib_unpack \
      --overwrite \
      --write_log \
      --icd10_map_file icd_codes.tsv \
      --category 10 \
      --category 11 \
      output.tsv input1.tsv input2.tsv


Could be stored in a configuration file ``config.txt``::

    overwrite
    write_log
    icd10_map_file icd_codes.tsv
    category       10
    category       11


And then executed as follows::

    fmrib_unpack -cfg config.txt output.tsv input1.tsv input2.tsv


Features
--------


FUNPACK allows you to perform various data sanitisation and processing steps
on your data, such as:

 * **NA value replacement**: Specific values for some columns can be replaced
   with NA, for example, variables where a value of -1 indicates *Do not know*.

 * **Categorical recoding**: Certain categorical columns can re-coded. For
   example, variables where a value of 555 represents *half* can be recoded
   so that 555 is replaced with 0.5.

 * **Child value replacement**: NA values within some columns which are
   dependent upon other columns may have values inserted based on the values
   of their parent columns.

See the introductory notebook for a more comprehensive overview of the features
available in FUNPACK.


Built-in rules
--------------


FUNPACK contains a large number of built-in rules which have been specifically
written to pre-process UK BioBank data variables. These rules are stored in
the following files [*]_:

 * ``funpack/configs/fmrib/datacodings_*.tsv``: Cleaning rules for data
   codings
 * ``funpack/configs/fmrib/variables_*.tsv``: Cleaning rules for individual
   variables
 * ``funpack/configs/fmrib/processing.tsv``: Processing steps
 * ``funpack/configs/fmrib/categories.tsv``: Variable categories

.. [*] The ``funpack/`` directory is located in
        ``<python-env>/lib/python<X.Y>/site-packages/funpack/``, where
        ``<python-env>`` is the location of your Python environment directory,
        and ``<X.Y>`` is the Python version you are using.


You can use these rules by using the FMRIB configuration profile::

    fmrib_unpack -cfg fmrib output.tsv input.tsv


You can customise or replace these files as you see fit. You can also pass
your own versions of these files to FUNPACK via the ``--variable_file``,
``--datacoding_file``, ``--type_file``, ``--processing_file``, and
``--category_file`` command-line options respectively. FUNPACK will load all
variable and datacoding files, and merge them into a single table which
contains the cleaning rules for each variable.


.. note:: The ``fmrib`` configuration profile is managed and released
          separately from FUNPACK at
          https://git.fmrib.ox.ac.uk/fsl/funpack-fmrib-config/. However, it is
          automatically installed alongside FUNPACK, so if you have FUNPACK,
          you can use the ``fmrib`` profile. If you are using FUNPACK from a
          source checkout, you may need to manually install the
          ``fmrib-unpack-fmrib-config`` package from `PyPi
          <https://pypi.org/project/fmrib-unpack-fmrib-config/>`_ or
          `conda-forge
          <https://anaconda.org/conda-forge/fmrib-unpack-fmrib-config>`_.


Creating your own rule files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


To define rules at the *data-coding* level, create one or more ``.tsv`` files
with an ``ID`` column containing the data-coding ID, and any of the following
columns:


  - ``NAValues``: A comma-separated list of values to replace with NA
  - ``RawLevels`` A comma-separated list of values to be replaced with
    corresponding values in ``NewLevels``.
  - ``NewLevels`` A comma-separated list of replacement values for each
    of the values listed in ``RawLevels``.

To apply these rules, pass your ``.tsv`` file(s) to ``funpack`` with the
``--datacoding_file`` option. They will be applied to all variables which
use the data-coding(s) listed in the file(s).


To define rules at the *variable* level, create one or more ``.tsv`` files
with an ``ID`` column containing the variable ID, and any of the following
columns:


  - ``NAValues``: As above
  - ``RawLevels`` As above
  - ``NewLevels`` As above
  - ``ParentValues``: A comma-separated list of expressions on parent
    variables, defining conditions which should trigger child-value
    replacement.
  - ``ChildValues``: A comma-separated list of values to insert into the
    variable when the corresponding expression in ``ParentValues`` evaluates
    to true.
  - ``Clean``: A comma-separated list of cleaning functions to apply to the
    variable.


Output
------


The main output of FUNPACK is a plain-text file [*]_ which contains the input
data, after cleaning and processing, potentially with some columns removed,
and new columns added.


If you used the ``--suppress_non_numerics`` option, the main output file will
only contain the numeric columns. You can combine this with the
``--write_non_numerics`` option to save non-numeric columns to a separate
file.


You can use any tool of your choice to load this output file, such as Python,
MATLAB, or Excel. It is also possible to pass the output back into
FUNPACK.


.. [*] If your output file name ends with ``.csv``, the file will be
       comma-separated, and if your output file name ends with ``.tsv``, the
       file will be tab-separated.


Loading output into MATLAB
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. |readtable| replace:: ``readtable``
.. _readtable: https://uk.mathworks.com/help/matlab/ref/readtable.html

.. |table| replace:: ``table``
.. _table: https://uk.mathworks.com/help/matlab/ref/table.html


If you are using MATLAB, you have several options for loading the FUNPACK
output. The best option is |readtable|_, which will load column names, and
will handle both non-numeric data and missing values.  Use ``readtable`` like
so (assuming that you generated a tab-separated file)::

    data = readtable('out.tsv', 'FileType', 'text');


The ``readtable`` function returns a |table|_ object, which stores each column
as a separate vector (or cell-array for non-numeric columns). If you are only
interested in numeric columns, you can retrieve them as an array like this::

    data    = data(:, vartype('numeric'));
    rawdata = data.Variables;


The ``readtable`` function will potentially rename the column names to ensure
that they are are valid MATLAB identifiers. You can retrieve the original
names from the ``table`` object like so::

    colnames = data.Properties.VariableDescriptions';


If you have used the ``--write_description`` or ``--description_file``
options, you can load in the descriptions for each column as follows::

    descs = readtable('out_descriptions.tsv', ...
                      'FileType', 'text', ...
                      'Delimiter', '\t',  ...
                      'ReadVariableNames',false);
    descs = [descs; {'eid', 'ID'}];
    idxs  = cellfun(@(x) find(strcmp(descs.Var1, x)), colnames, ...
                    'UniformOutput', false);
    idxs  = cell2mat(idxs);
    descs = descs.Var2(idxs);


Tests
-----


To run the test suite, you need to install some additional dependencies::

    pip install fmrib-unpack[test]


Then you can run the test suite using ``pytest``::

    pytest


macOS issues
------------


FUNPACK makes extensive use of the Python `multiprocessing
<https://docs.python.org/3/library/multiprocessing.html>`_ module to speed up
certain steps in its processing pipeline.  FUNPACK relies on the POSIX `fork()
<https://www.man7.org/linux/man-pages/man2/fork.2.html>`_ mechanism, so that
worker processes may inexpensively inherit the memory space of the main
process (often referred to as *copy-on-write*).  This is to avoid having to
serialise the data set being processed (stored internally as a
``pandas.DataFrame``).


In python 3.8 on macOS, the default method used by the ``multiprocessing``
module was changed from ``fork`` to ``spawn``, due to changes in macOS 10.13
restricting the use of ``fork()`` for safety reasons. Some background
information on this change can be found at https://bugs.python.org/issue33725,
and at `this blog post
<https://wefearchange.org/2018/11/forkmacos.rst.html>`_.


FUNPACK therefore explicitly sets the method used by the ``multiprocessing``
to ``fork``, to take advantage of copy-on-write semantics.  Using ``fork()``
on macOS *should* be safe for single-threaded parent processes, but as FUNPACK
calls ``fork()`` numerous times (by creating and discarding
``multiprocessing.Pool()`` objects on an as-needed basis), this assumption may
not be valid, and FUNPACK may crash with an error message resembling the
following::


    +[SomeClass initialize] may have been in progress in another thread
    when fork() was called. We cannot safely call it or ignore it in the
    fork() child process. Crashing instead.


You might be able to work around this error by setting an environment variable
before calling FUNPACK, like so::


    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
    fmrib_unpack ...


Citing
------


If you would like to cite FUNPACK, please refer to its `Zenodo page
<https://doi.org/10.5281/zenodo.1997626>`_.
