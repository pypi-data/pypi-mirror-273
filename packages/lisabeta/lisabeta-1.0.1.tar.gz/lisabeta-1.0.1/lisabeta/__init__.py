#
# Copyright (C) 2019  Sylvain Marsat, John G. Baker
#
#

try:
    # This will fail when lisabeta is imported during the build process,
    # before version.py has been generated.
    from .version import git_hash
    from .version import version as lisabeta_version
except:
    git_hash = 'none'
    lisabeta_version = 'none'

__version__ = lisabeta_version
