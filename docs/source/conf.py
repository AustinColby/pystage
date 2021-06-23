# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from tempfile import TemporaryFile
from urllib.request import urlopen
from zipfile import ZipFile

sys.path.insert(0, os.path.abspath("../../src"))


# -- Project information -----------------------------------------------------

project = 'PyStage'
copyright = '2021, The Pystage Developing Team'
author = 'The Pystage Developing Team'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', "sphinx_rtd_theme", "m2r2"]
# 'sphinx.ext.coverage', 'sphinx.ext.napoleon'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# alabaster
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# doing this as example for en
PATH_BLOCK_IMAGES = "/".join([html_static_path[0], "images", "blocks"])
lang = "en"
BLOCK_IMG_URL = f"http://img.pystage.org/blocks/zip/png/300/{lang}_png300.zip"

# download block img
with urlopen(BLOCK_IMG_URL) as f:
    print(f"Downloading block imgs for {lang}.")
    html = f.read()
    with TemporaryFile() as tmp:
        tmp.write(html)
        with ZipFile(tmp) as f:
            f.extractall("/".join([PATH_BLOCK_IMAGES, lang]))


# insert rst block with correct image
def autodoc_process_docstring(app, what, name, obj, options, lines):
    def get_block_png(lang, opcode):
        return "/".join([PATH_BLOCK_IMAGES, lang, opcode + ".png"])

    if hasattr(obj, "opcode"):
        path = get_block_png(name.split(".")[1], obj.opcode)

        # insert rst figure block, care to put in empty lines above and below.
        for i in range(3):
            lines.insert(1, "")
        lines.insert(4, f".. figure:: {path}")
        lines.insert(5, "    :width: 150")
        for i in range(3):
            lines.insert(6, "")

    return lines


def setup(app):
    print("Setup")
    app.connect('autodoc-process-docstring', autodoc_process_docstring)
