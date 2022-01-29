# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

from __future__ import annotations

import os
import sys

on_rtd = os.environ.get("READTHEDOCS") == "True"

docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
project_dir = os.path.abspath(os.path.join(docs_dir, ".."))
package_dir = os.path.abspath(os.path.join(project_dir, "koapy"))

# -- Autodoc mocking configuration ---

from unittest.mock import MagicMock

autodoc_mock_imports = [
    "PyQt5",
    "PySide2",
    "sip",
    "qtpy",
    "pythoncom",
    "pywintypes",
    "win32com",
    "win32com.client",
]

for module in autodoc_mock_imports:
    sys.modules[module] = MagicMock()

if "qtpy" in autodoc_mock_imports:

    class QWidget:
        __module__ = "qtpy.QtWidgets"

    class QObject:
        __module__ = "qtpy.QtCore"

    qtpy = MagicMock()
    qtpy.QtWidgets.QWidget = QWidget
    qtpy.QtWidgets.QApplication = MagicMock()
    qtpy.QtWidgets.QSystemTrayIcon = MagicMock()
    qtpy.QtWidgets.QMenu = MagicMock()
    qtpy.QtWidgets.QStyle = MagicMock()
    qtpy.QtCore.QObject = QObject
    qtpy.QtCore.QEvent = MagicMock()
    qtpy.QtCore.Qt = MagicMock()
    qtpy.QtCore.QTimer = MagicMock()
    qtpy.QtCore.QUrl = MagicMock()
    qtpy.QtCore.Signal = MagicMock()
    qtpy.QtCore.SIGNAL = MagicMock()
    qtpy.QtAxContainer.QAxWidget = MagicMock()
    qtpy.QtGui.QDesktopServices = MagicMock()
    qtpy.QtNetwork.QAbstractSocket = MagicMock()

    sys.modules.update(
        {
            "qtpy": qtpy,
            "qtpy.QtWidgets": qtpy.QtWidgets,
            "qtpy.QtCore": qtpy.QtCore,
            "qtpy.QtAxContainer": qtpy.QtAxContainer,
            "qtpy.QtGui": qtpy.QtGui,
            "qtpy.QtNetwork": qtpy.QtNetwork,
        }
    )

if "PySide2" in autodoc_mock_imports:

    class QWidget:  # pylint: disable=function-redefined
        __module__ = "PySide2.QtWidgets"

    class QObject:  # pylint: disable=function-redefined
        __module__ = "PySide2.QtCore"

    PySide2 = MagicMock()
    PySide2.QtWidgets.QWidget = QWidget
    PySide2.QtCore.QObject = QObject
    PySide2.QtAxContainer.QAxWidget = MagicMock()
    PySide2.QtGui.QDesktopServices = MagicMock()
    PySide2.QtNetwork = MagicMock()

    sys.modules.update(
        {
            "PySide2": PySide2,
            "PySide2.QtWidgets": PySide2.QtWidgets,
            "PySide2.QtCore": PySide2.QtCore,
            "PySide2.QtAxContainer": PySide2.QtAxContainer,
            "PySide2.QtGui": PySide2.QtGui,
            "PySide2.QtNetwork": PySide2.QtNetwork,
        }
    )

if "PyQt5" in autodoc_mock_imports:

    class QWidget:  # pylint: disable=function-redefined
        __module__ = "PyQt5.QtWidgets"

    class QObject:  # pylint: disable=function-redefined
        __module__ = "PyQt5.QtCore"

    PyQt5 = MagicMock()
    PyQt5.QtWidgets.QWidget = QWidget
    PyQt5.QtCore.QObject = QObject
    PyQt5.QAxContainer.QAxWidget = MagicMock()
    PyQt5.QtGui.QDesktopServices = MagicMock()
    PyQt5.QtNetwork = MagicMock()

    sys.modules.update(
        {
            "PyQt5": PyQt5,
            "PyQt5.QtWidgets": PyQt5.QtWidgets,
            "PyQt5.QtCore": PyQt5.QtCore,
            "PyQt5.QAxContainer": PyQt5.QAxContainer,
            "PyQt5.QtGui": PyQt5.QtGui,
            "PyQt5.QtNetwork": PyQt5.QtNetwork,
        }
    )

# -- Import main package after mocking ---------------------------------------

sys.path.insert(0, project_dir)

import koapy  # noqa: E402

# -- Autodoc configuration ---

add_function_parentheses = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "PyQt5": ("https://www.riverbankcomputing.com/static/Docs/PyQt5/", None),
}

# -- Project information -----------------------------------------------------

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "KOAPY"
author = koapy.__author__
copyright = "2021, " + koapy.__author__  # pylint: disable=redefined-builtin

# The version info for the project you"re documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = koapy.__version__
# The full version, including alpha/beta/rc tags.
release = koapy.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.githubpages",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: list[str] = []

# -- Warnings related setting ---

suppress_warnings = ["autosectionlabel.*"]

if on_rtd:
    keep_warnings = False
    autodoc_warningiserror = False
else:
    keep_warnings = True
    autodoc_warningiserror = True

# -- Autoapi configuration ---------------------------------------------------

extensions.append("autoapi.extension")

autoapi_type = "python"
autoapi_file_patterns = [
    "*.pyi",
    "*.py",
]
autoapi_dirs = [package_dir]
autoapi_ignore = [
    "**/examples/*.py",
]
autoapi_keep_files = False
autoapi_options = [
    "members",
    # "inherited-members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

# -- Nbsphinx configuration --------------------------------------------------

if not on_rtd:
    extensions.append("nbsphinx")

html_sourcelink_suffix = ""

# -- Missing reference ---

from docutils import nodes

missing_reference_uris = {
    "PyQt5.QtWidgets.QWidget": "https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtwidgets/qwidget.html?highlight=qwidget",
    "PyQt5.QtCore.QObject": "https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtcore/qobject.html?highlight=qobject",
    "PySide2.QtWidgets.QWidget": "https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html",
    "PySide2.QtCore.QObject": "https://doc.qt.io/qtforpython/PySide2/QtCore/QObject.html",
}


def missing_reference(_app, _env, node, contnode):
    target = node["reftarget"]
    uri = missing_reference_uris.get(target)
    if uri:
        newnode = nodes.reference("", "", internal=False, refuri=uri)
        newnode.append(contnode)
        return newnode
    return None


# -- Setup event hooks ---


def setup(app):
    app.connect("missing-reference", missing_reference)


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
pygments_style = "sphinx"

# Theme options are theme-specific and customize the look and feel of a
# theme further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "description": "Kiwoom Open Api Plus Python",  # noqa: E501
    "fixed_sidebar": "true",
    "github_user": "elbakramer",
    "github_repo": "koapy",
    "github_banner": "true",
    "github_button": "true",
    "github_type": "star",
    "donate_url": "https://toon.at/donate/637521884081401532",
    "font_family": "'Noto Serif KR', Georgia, 'Times New Roman', Times, serif",
    "head_font_family": "'Noto Serif KR', Georgia, 'Times New Roman', Times, serif",
    "code_font_family": "'D2Coding', 'Consolas', 'Menlo', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', monospace",
}

if not on_rtd:
    html_theme_options["analytics_id"] = "UA-179490468-1"

html_context = {
    "google_site_verification": "true",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Edit this css file to override some existing styles.
html_css_files = [
    "css/style.css",
]

# -- Translation related configuration ---

gettext_uuid = True
gettext_compact = False

# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "preamble": r"""
    \usepackage{kotex}
    """,
    "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (master_doc, "koapy.tex", "KOAPY Documentation", "Yunseong Hwang", "manual"),
]


# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "koapy", "KOAPY Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "koapy",
        "KOAPY Documentation",
        author,
        "koapy",
        "One line description of project.",
        "Miscellaneous",
    ),
]
