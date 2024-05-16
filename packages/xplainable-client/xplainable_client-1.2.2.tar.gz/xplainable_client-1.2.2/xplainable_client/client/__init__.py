from .datasets import *
from functools import cached_property

from ._models import *
from ._misc import *
from requests.packages.urllib3.util.retry import Retry
from ._session import Session
from ._misc import Misc
from ._models import Models
from ._preprocessing import Preprocessing
from ._deployments import Deployments
from ._gpt import GPT
from ._collections import Collections
from ._datasets import Datasets
from ._inference import Inference


class Client(Misc, Models, Preprocessing, GPT, Collections):

    def __init__(self, api_key=None, hostname='https://api.xplainable.io', silent_mode=False):
        self.session = Session(api_key=api_key, hostname=hostname, silent_mode=silent_mode)
        Misc.__init__(self, self.session)
        Models.__init__(self, self.session)
        Preprocessing.__init__(self, self.session)
        Deployments.__init__(self, self.session)
        GPT.__init__(self, self.session)
        Collections.__init__(self, self.session)
        Datasets.__init__(self, self.session)
        Inference.__init__(self, self.session)
        



