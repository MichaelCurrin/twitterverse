"""
Initialisation file for models directory.
"""
# Create an _`_all__` list here, using values set in other application files.
from .places import __all__ as placesModel
from .trends import __all__ as trendsModel
from .tweets import __all__ as tweetsModel
from .cronJobs import __all__ as cronJobsModel
__all__ = placesModel + trendsModel + tweetsModel + cronJobsModel

# Make table objects available on models module.
from .places import *
from .trends import *
from .tweets import *
from .cronJobs import *
