from dataclasses import dataclass, asdict
from enum import Enum


class state(Enum):
    INIT = 'init'
    RUN = 'run'
    PAUSE = 'pause'
    STOP = 'stop'


@dataclass
class Item:
    id: str
    description: str
    state: str


netflix = Item('Netflix', 'tv shows', state.INIT.value)
hbo = Item('hbo', 'documentary', state.RUN.value)
ps = Item('ps', 'ps games', state.PAUSE.value)
xbox = Item('xbox', 'xbox games', state.STOP.value)

subscriptions = [asdict(netflix), asdict(hbo), asdict(ps), asdict(xbox)]
