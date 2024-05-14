# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['derivative']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.3,<2.0.0', 'scikit-learn>=1,<2', 'scipy>=1.4.1,<2.0.0']

extras_require = \
{'dev': ['pytest>=7,<8'],
 'docs': ['sphinx>=5,<6',
          'nbsphinx>=0.6.1,<0.7.0',
          'ipykernel>=5.2.1,<6.0.0',
          'jupyter_client>=6.1.3,<7.0.0',
          'matplotlib>=3.2.1,<4.0.0']}

entry_points = \
{'derivative.hyperparam_opt': ['kalman.default = '
                               'derivative.utils:_default_kalman']}

setup_kwargs = {
    'name': 'derivative',
    'version': '0.6.1',
    'description': 'Numerical differentiation in python.',
    'long_description': '|RTD| |PyPI| |Zenodo| |GithubCI| |LIC|\n\nNumerical differentiation of noisy time series data in python\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n**derivative** is a Python package for differentiating noisy data. The package showcases a variety of improvements that can be made over finite differences when data is not clean.\n\nWant to see an example of how **derivative** can help? This package is part of **PySINDy** (`github.com/dynamicslab/pysindy <https://github.com/dynamicslab/pysindy/>`_), a sparse-regression framework for discovering nonlinear dynamical systems from data.\n\nThis package binds common differentiation methods to a single easily implemented differentiation interface to encourage user adaptation.\nNumerical differentiation methods for noisy time series data in python includes:\n\n1. Symmetric finite difference schemes using arbitrary window size.\n\n2. Savitzky-Galoy derivatives (aka polynomial-filtered derivatives) of any polynomial order with independent left and right window parameters.\n\n3. Spectral derivatives with optional filter.\n\n4. Spline derivatives of any order.\n\n5. Polynomial-trend-filtered derivatives generalizing methods like total variational derivatives.\n\n6. Kalman derivatives find the maximum likelihood estimator for a derivative described by a Brownian motion.\n\n7. Kernel derivatives smooth a random process defined by its kernel (covariance).\n\n.. code-block:: python\n\n    from derivative import dxdt\n    import numpy as np\n\n    t = np.linspace(0,2*np.pi,50)\n    x = np.sin(x)\n\n    # 1. Finite differences with central differencing using 3 points.\n    result1 = dxdt(x, t, kind="finite_difference", k=1)\n\n    # 2. Savitzky-Golay using cubic polynomials to fit in a centered window of length 1\n    result2 = dxdt(x, t, kind="savitzky_golay", left=.5, right=.5, order=3)\n\n    # 3. Spectral derivative\n    result3 = dxdt(x, t, kind="spectral")\n\n    # 4. Spline derivative with smoothing set to 0.01\n    result4 = dxdt(x, t, kind="spline", s=1e-2)\n\n    # 5. Total variational derivative with regularization set to 0.01\n    result5 = dxdt(x, t, kind="trend_filtered", order=0, alpha=1e-2)\n\n    # 6. Kalman derivative with smoothing set to 1\n    result6 = dxdt(x, t, kind="kalman", alpha=1)\n    \n    # 7. Kernel derivative with smoothing set to 1\n    result7 = dxdt(x, t, kind="kernel", sigma=1, lmbd=.1, kernel="rbf")\n\nContributors:\n-------------\nThanks to the members of the community who have contributed!\n\n+-----------------------------------------------------------------+-----------------------------------------------------------------------------------+\n|`Jacob Stevens-Haas <https://github.com/Jacob-Stevens-Haas>`_    | Kalman derivatives `#12 <https://github.com/andgoldschmidt/derivative/pull/12>`_, |\n|                                                                 | and more!                                                                         |\n+-----------------------------------------------------------------+-----------------------------------------------------------------------------------+\n\n\nReferences:\n-----------\n\n[1] Numerical differentiation of experimental data: local versus global methods- K. Ahnert and M. Abel\n\n[2] Numerical Differentiation of Noisy, Nonsmooth Data- Rick Chartrand\n\n[3] The Solution Path of the Generalized LASSO- R.J. Tibshirani and J. Taylor\n\n[4] A Kernel Approach for PDE Discovery and Operator Learning - D. Long et al.\n\n\nCiting derivative:\n------------------\nThe **derivative** package is a contribution to `PySINDy <https://github.com/dynamicslab/pysindy/>`_; this work has been published in the Journal of Open Source Software (JOSS). If you use **derivative** in your work, please cite it using the following reference:\n\nKaptanoglu et al., (2022). PySINDy: A comprehensive Python package for robust sparse system identification. Journal of Open Source Software, 7(69), 3994, https://doi.org/10.21105/joss.03994\n\n.. code-block:: text\n\n\t@article{kaptanoglu2022pysindy,\n\t\tdoi = {10.21105/joss.03994},\n\t\turl = {https://doi.org/10.21105/joss.03994},\n\t\tyear = {2022},\n\t\tpublisher = {The Open Journal},\n\t\tvolume = {7},\n\t\tnumber = {69},\n\t\tpages = {3994},\n\t\tauthor = {Alan A. Kaptanoglu and Brian M. de Silva and Urban Fasel and Kadierdan Kaheman and Andy J. Goldschmidt and Jared Callaham and Charles B. Delahunt and Zachary G. Nicolaou and Kathleen Champion and Jean-Christophe Loiseau and J. Nathan Kutz and Steven L. Brunton},\n\t\ttitle = {PySINDy: A comprehensive Python package for robust sparse system identification},\n\t\tjournal = {Journal of Open Source Software}\n\t\t}\n    \n\n.. |RTD| image:: https://readthedocs.org/projects/derivative/badge/?version=latest\n   :target: https://derivative.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n  \n.. |LIC| image:: https://img.shields.io/badge/License-MIT-blue.svg\n   :target: https://derivative.readthedocs.io/en/latest/license.html\n   :alt: MIT License\n\n.. |PyPI| image:: https://badge.fury.io/py/derivative.svg\n    :target: https://pypi.org/project/derivative/\n\n.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.6617446.svg\n   :target: https://doi.org/10.5281/zenodo.6617446\n\n.. |GithubCI| image:: https://github.com/andgoldschmidt/derivative/actions/workflows/push-test.yml/badge.svg\n    :target: https://github.com/andgoldschmidt/derivative/actions/workflows/push-test.yml\n\n',
    'author': 'Andy Goldschmidt',
    'author_email': 'andygold@uchicago.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/andgoldschmidt/derivative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
