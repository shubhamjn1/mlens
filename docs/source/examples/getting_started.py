# -*- coding: utf-8 -*-
"""

.. _getting-started:

Getting started
===============

This tutorial highlights the basics of the
high-level API for ensemble classes, the model selection suite and
features visualization.

============================  =================================================
                   Tutorials                                            Content
============================  =================================================
:ref:`ensemble-guide`         How to build, fit and predict with an ensemble
:ref:`model-selection-guide`  How to compare several estimators in one go
:ref:`visualization-guide`    Plotting functionality
============================  =================================================

The :ref:`advanced high-level API tutorials <ensemble-tutorial>` shows how to
leverage advanced features such as probabilistic layers, feature propagation
etc. For tutorials on low-level mechanics, see
:ref:`the mechanics guides <learner_tutorial>`.


Preliminaries
-------------

We use the following setup throughout:
"""
import numpy as np
from pandas import DataFrame
from sklearn.metrics import f1_score
from sklearn.datasets import load_iris

seed = 2017
np.random.seed(seed)

def f1(y, p): return f1_score(y, p, average='micro')

data = load_iris()
idx = np.random.permutation(150)
X = data.data[idx]
y = data.target[idx]
print(y)

##############################################################################
# .. _ensemble-guide:
#
# Ensemble guide
# --------------
# Building an ensemble
# ^^^^^^^^^^^^^^^^^^^^
# Instantiating a fully specified ensemble is straightforward and requires
# three steps: first create the instance, second add the intermediate layers, and
# finally the meta estimator.
from mlens.ensemble import SuperLearner
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# --- Build ---
# Passing a scoring function will create cv scores during fitting
# the scorer should be a simple function accepting to vectors and returning a scalar

ensemble = SuperLearner(scorer=f1, random_state=seed, verbose=1)

# Build the first layer
ensemble.add([RandomForestClassifier(random_state=seed), SVC()])

# Attach the final meta estimator
ensemble.add_meta(LogisticRegression())

# --- Use ---

# Fit ensemble
ensemble.fit(X[:75], y[:75])

# Predict
preds = ensemble.predict(X[75:])

##############################################################################
# To check the performance of estimator in the layers, call the ``data``
# attribute. The attribute can be wrapped in a :class:`pandas.DataFrame`,
# but prints in a tabular format as is.
print(ensemble.data)

##############################################################################
