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

netflix = Item('Netflix', 'tv shows', str(state.INIT))
hbo = Item('hbo', 'documentary', str(state.RUN))
ps = Item('ps', 'ps games', str(state.PAUSE))
xbox = Item('xbox', 'xbox games', str(state.STOP))


subscriptions = [asdict(netflix), asdict(hbo), asdict(ps), asdict(xbox)]
