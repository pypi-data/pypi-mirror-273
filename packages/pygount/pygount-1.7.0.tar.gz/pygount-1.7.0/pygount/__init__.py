"""
Pygount counts lines of source code using pygments lexers.
"""

# Copyright (c) 2016-2023, Thomas Aglassinger.
# All rights reserved. Distributed under the BSD License.
from importlib.metadata import version

from .analysis import DuplicatePool, SourceAnalysis, SourceScanner, SourceState, encoding_for, source_analysis
from .common import Error, OptionError
from .summary import LanguageSummary, ProjectSummary

__version__ = version(__name__)

__all__ = [
    "__version__",
    "encoding_for",
    "DuplicatePool",
    "Error",
    "LanguageSummary",
    "OptionError",
    "ProjectSummary",
    "SourceAnalysis",
    "SourceScanner",
    "SourceState",
    "source_analysis",
]
