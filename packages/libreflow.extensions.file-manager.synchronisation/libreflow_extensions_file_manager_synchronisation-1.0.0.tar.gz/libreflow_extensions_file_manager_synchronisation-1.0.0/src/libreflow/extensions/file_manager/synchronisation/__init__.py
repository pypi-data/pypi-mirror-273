from kabaret import flow
from libreflow.baseflow import Synchronization
from .file import RequestRevisions, MultiRequestRevisions
from .shot import RequestShot, MultiRequestShot, RequestSequence, MultiRequestSequence
from .error import ShowSiteSyncErrors
from .sync_utils import resolve_pattern

from . import _version
__version__ = _version.get_versions()['version']

def request_revisions(parent):
    if type(parent) is Synchronization:
        r = flow.Child(MultiRequestRevisions).ui(label='Request Files')
        r.name = 'multi_request_revisions'
        r.index = None
        return r

def install_extensions(session): 
    return {
        "synchronization": [
            request_revisions,
        ],
    }
