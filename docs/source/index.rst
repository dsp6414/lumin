:github_url: https://github.com/GilesStrong/lumin

LUMIN
===================================================

Lumin Unifies Many Improvements for Networks

LUMIN aims to become a deep-learning and data-analysis ecosystem for
High-Energy Physics, and perhaps other scientific domains in the future.
Similar to `Keras`_ and `fastai`_ it is a wrapper framework for a graph
computation library (PyTorch), but includes many useful functions to
handle domain-specific requirements and problems. It also intends to
provide easy access to to state-of-the-art methods, but still be
flexible enough for users to inherit from base classes and override
methods to meet their own demands.

.. toctree::
   :maxdepth: 1
   :caption: Package Reference

   lumin.data_processing
   lumin.evaluation
   lumin.inference
   lumin.nn
   lumin.optimisation
   lumin.plotting
   lumin.utils

Package Description
===================================================

For an introduction and motivation for LUMIN, checkout this talk from
IML-2019 at CERN: `video`_, `slides`_.

Distinguishing Characteristics
------------------------------

Data objects
~~~~~~~~~~~~

-  Use with large datasets: HEP data can become quite large, making
   training difficult:

   -  The ``FoldYielder`` class provides on-demand access to data stored
      in HDF5 format, only loading into memory what is required.
   -  Conversion from ROOT and CSV to HDF5 is easy to achieve using (see
      examples)
   -  ``FoldYielder`` provides conversion methods to Pandas
      ``DataFrame`` for use with other internal methods and external
      packages

-  Non-network-specific methods expect Pandas ``DataFrame`` allowing
   their use without having to convert to ``FoldYielder``.

Deep learning
~~~~~~~~~~~~~

-  PyTorch > 1.0
-  Inclusion of recent deep learning techniques and practices,
   including:

   -  Dynamic learning rate, momentum, beta_1:

      -  Cyclical, `Smith, 2015`_
      -  Cosine annealed `Loschilov & Hutter, 2016`_
      -  1-cycle, `Smith, 2018`_

   -  HEP-specific data augmentation during training and inference
   -  Advanced ensembling methods:

      -  Snapshot ensembles `Huang et al., 2017`_
      -  Fast geometric ensembles `Garipov et al., 2018`_
      -  Stochastic Weight Averaging `Izmailov et al., 2018`_

   -  Learning Rate Finders, `Smith, 2015`_
   -  Entity embedding of categorical features, `Guo & Berkhahn, 2016`_
   -  Label smoothing `Szegedy et al., 2015`_

-  Flexible architecture construction:

   -  ``ModelBuilder`` takes parameters and modules to yield networks
      on-demand
   -  Networks constructed from modular blocks:

      -  Head - Takes input features
      -  Body - Contains most of the hidden layers
      -  Tail - Scales down the body to the desired number of outputs
      -  Endcap - Optional layer for use post-training to provide
         further computation on model outputs; useful when training on a
         proxy objective

   -  Easy loading and saving of pre-trained embedding weights
   -  Modern architectures like residual and dense(-like) networks (`He
      et al. 2015`_ & `Huang et al. 2016`_)

-  HEP-specific losses, e.g. Asimov loss `Elwood & Krücker, 2018`_
-  Easy training and inference of ensembles of models:

   -  Default training method ``fold_train_ensemble``, trains a
      specified number of models as well as just a single model
   -  ``Ensemble`` class handles the (metric-weighted) construction of
      an ensemble, its inference, saving and loading, and interpretation

-  Easy exporting of models to other libraries via Onnx
-  Use with CPU and NVidia GPU
-  Evaluation on domain-specific metrics such as Approximate Median
   Significance via ``EvalMetric`` class
-  Keras-style callbacks

Feature selection methods
~~~~~~~~~~~~~~~~~~~~~~~~~

-  Dendrograms
-  Feature importance via auto-optimised SK-Learn random forests

Interpretation
~~~~~~~~~~~~~~

-  Feature importance for models and ensembles
-  Embedding visualisation
-  1D & 2D partial dependency plots (via PDPbox)

Plotting
~~~~~~~~

-  Variety of domain-specific plotting functions
-  Unified appearance via ``PlotSettings`` class - class accepted by
   every plot function providing control of plot appearance, titles,
   colour schemes, et cetera

Universal handling of sample weights
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  HEP events are normally accompanied by weight characterising the
   acceptance and production cross-section of that particular event, or
   to flatten some distribution.
-  Relevant methods and classes can take account of these weights.
-  This includes training, interpretation, and plotting
-  Expansion of PyTorch losses to better handle weights

Parameter optimisation
~~~~~~~~~~~~~~~~~~~~~~

-  Optimal learning rate via cross-validated range tests `Smith, 2015`_
-  Quick, rough optimisation of random forest hyper parameters
-  Generalisable Cut & Count thresholds
-  1D discriminant binning with respect to bin-fill uncertainty

Statistics and uncertainties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Integral to experimental science
-  Quantitative results are accompanied by uncertainties
-  Use of bootstrapping to improve precision of statistics estimated
   from small samples

Look and feel
~~~~~~~~~~~~~

-  LUMIN aims to feel fast to use - liberal use of progress bars mean
   you’re able to always know when tasks will finish, and get live
   updates of training
-  Guaranteed to spark joy (in its current beta state, LUMIN may instead
   ignite rage, despair, and frustration - *dev.*)

Installation
------------

Due to some strict version requirements on packages, it is recommended
to install LUMIN in its own Python environment, e.g
``conda create -n lumin python=3.6``

From PyPI
~~~~~~~~~

The main package can be installed via: ``pip install lumin``

Full functionality requires two additional packages as described below.

From source
~~~~~~~~~~~
::

   git clone git@github.com:GilesStrong/lumin.git
   cd lumin
   pip install .

Optionally, run pip install with ``-e`` flag for development
installation. Full functionality requires an additional package as
described below.

Additional modules
~~~~~~~~~~~~~~~~~~

Full use of LUMIN requires the latest version of PDPbox, but this is not
released yet on PyPI, so you’ll need to install it from source, too:

-  ``git clone https://github.com/SauceCat/PDPbox.git && cd PDPbox && pip install -e .``
   note the ``-e`` flag to make sure the version number gets set
   properly.

Notes
-----

Why use LUMIN
~~~~~~~~~~~~~

TMVA contained in CERN’s ROOT system, has been the default choice for
BDT training for analysis and reconstruction algorithms due to never
having to leave ROOT format. With the gradual move to DNN approaches,
more scientists are looking to move their data out of ROOT to use the
wider selection of tools which are available. Keras appears to be the
first stop due to its ease of use, however implementing recent methods
in Keras can be difficult, and sometimes requires dropping back to the
tensor library that it aims to abstract. Indeed, the prequel to LUMIN
was a similar wrapper for Keras (`HEPML_Tools`_) which involved some
pretty ugly hacks. The fastai framework provides access to these recent
methods, however doesn’t yet support sample weights to the extent that
HEP requires. LUMIN aims to provides the best of both, Keras-style
sample weighting and fastai training methods, while focussing on
columnar data and providing domain-specific metrics, plotting, and
statistical treatment of results and uncertainties.

Data types
~~~~~~~~~~

LUMIN is primarily designed for use on columnar data. With some extra
work it can be used on other data formats, but at the moment it has
nothing special to offer. Whilst recent work in HEP has made use of jet
images and GANs, these normally hijack existing ideas and models.
Perhaps once we get established, domain specific approaches which
necessitate the use of a specialised framework, then LUMIN could grow to
meet those demands, but for now I’d recommend checking out the fastai
library, especially for image data.

With just one main developer, I’m simply focussing on the data types and
applications I need for my own research and common use cases in HEP. If,
however you would like to use LUMIN’s other methods for your own work on
other data formats, then you are most welcome to contribute and help to
grow LUMIN to better meet the needs of the scientific community.

Future
~~~~~~

The current priority is to imporve the documentation, add unit tests, and
expand the examples.

The next step will be to try and increase the user base and number of
contributors. I’m aiming to achieve this through presentations,
tutorials, blog posts, and papers.

Further improvments will be in the direction of implementing new methods
and (HEP-specific) architectures, as well as providing helper functions
and data exporters to statistical analysis packages like Combine and
PYHF.

Contributing & feedback
~~~~~~~~~~~~~~~~~~~~~~~

Contributions, suggestions, and feedback are most welcome! The issue
tracker on this repo is probably the best place to report bugs et
cetera.

Code style
~~~~~~~~~~

Nope, the majority of the codebase does not conform to PEP8. PEP8 has
its uses, but my understanding is that it primarily written for
developers and maintainers of software whose users never need to read
the source code. As a maths-heavy research framework which users are
expected to interact with, PEP8 isn’t the best style. Instead I’m aiming
to follow more `the style of fastai`_, which emphasises, in particular,
reducing vertical space (useful for reading source code in a notebook)
naming and abbreviating variables according to their importance and
lifetime (easier to recognise which variables have a larger scope and
permits easier writing of mathematical operations). A full list of the
abbreviations used may be found in `abbr.md`_

Why is LUMIN called LUMIN?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Aside from being a recursive accronym (and therefore the best kind of
accronym) lumin is short for ‘luminosity’. In high-energy physics, the
integrated luminosity of the data collected by an experiment is the main
driver in the results that analyses obtain. With the paradigm shift
towards multivariate analyses, however, improved methods can be seen as
providing ‘artificial luminosity’; e.g. the gain offered by some DNN
could be measured in terms of the amount of extra data that would have
to be collected to achieve the same result with a more traditional
analysis. Luminosity can also be connected to the fact that LUMIN is
built around the python version of Torch.

Who develops LUMIN
~~~~~~~~~~~~~~~~~~

Currently just me - Giles Strong; a British-born, Lisbon-based, PhD
student in particle physics at IST, researcher at LIP-Lisbon, member of
Marie Curie ITN `AMVA4NewPhysics`_ and the CMS collaboration.

Certainly more developers and contributors are welcome to join and help
out!

Reference
~~~~~~~~~

If you have used LUMIN in your analysis work and wish to cite it, the
preferred reference is: *Giles C. Strong, LUMIN, Zenodo (Mar. 2019),
https://doi.org/10.5281/zenodo.2601857, Note: Please check
https://github.com/GilesStrong/lumin/graphs/contributors for the full
list of contributors*

| @misc{giles_chatham_strong_2019_2601857,
|   author = {Giles Chatham Strong},
|   title = {LUMIN},
|   month = mar,
|   year = 2019,
|   note = {{Please check
  https://github.com/GilesStrong/lumin/graphs/contributors for the full
  list of contributors}},
|   doi = {10.5281/zenodo.2601857},
|   url = {https://doi.org/10.5281/zenodo.2601857}
| }


.. _Keras: https://keras.io/
.. _fastai: https://github.com/fastai/fastai
.. _video: https://cds.cern.ch/record/2672119
.. _slides: https://indico.cern.ch/event/766872/timetable/?view=standard#29-lumin-a-deep-learning-and-d
.. _Smith, 2015: https://arxiv.org/abs/1506.01186
.. _Loschilov & Hutter, 2016: https://arxiv.org/abs/1608.03983
.. _Smith, 2018: https://arxiv.org/abs/1803.09820
.. _Huang et al., 2017: https://arxiv.org/abs/1704.00109
.. _Garipov et al., 2018: https://arxiv.org/abs/1802.10026
.. _Izmailov et al., 2018: https://arxiv.org/abs/1803.05407
.. _Guo & Berkhahn, 2016: https://arxiv.org/abs/1604.06737
.. _Szegedy et al., 2015: https://arxiv.org/abs/1512.00567
.. _He et al. 2015: https://arxiv.org/abs/1512.03385
.. _Huang et al. 2016: https://arxiv.org/abs/1608.06993
.. _Elwood & Krücker, 2018: https://arxiv.org/abs/1806.00322
.. _HEPML_Tools: https://github.com/GilesStrong/hepml_tools
.. _AMVA4NewPhysics: https://amva4newphysics.wordpress.com/
.. _the style of fastai: https://docs.fast.ai/dev/style.html
.. _abbr.md: https://github.com/GilesStrong/lumin/blob/master/abbr.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
