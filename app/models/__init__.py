"""
Initialisation file for models module.

Note that the model files cannot be be imported directly with
`python -m models/<MODEL>.py`, if they have been included here. Since
this __init__ file will add the table names to the name space before the
file is run, which causes a conflict.
"""
# Create an _`_all__` list here, using values set in other application files.
from .places import __all__ as places_model
from .trends import __all__ as trends_model
from .tweets import __all__ as tweets_model
from .cron_jobs import __all__ as cron_jobs_model
__all__ = places_model + trends_model + tweets_model + cron_jobs_model

# Make table objects available on models module.
from .places import *
from .trends import *
from .tweets import *
from .cron_jobs import *
