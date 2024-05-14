import os
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.py'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '.secrets.py'),
    ],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
