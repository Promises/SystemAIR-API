"""Configuration file for the Sphinx documentation builder."""

import os
import sys

# Add project root to the path so that autodoc can find it
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'SystemAIR-API'
copyright = '2025, Henning Berge'
author = 'Henning Berge'

# The full version, including alpha/beta/rc tags
import importlib.metadata
try:
    release = importlib.metadata.version('systemair_api')
except importlib.metadata.PackageNotFoundError:
    release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# -- autodoc settings --------------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__, __str__, __repr__',
}

# -- TypeHints settings ------------------------------------------------------
typehints_fully_qualified = False
always_document_param_types = True