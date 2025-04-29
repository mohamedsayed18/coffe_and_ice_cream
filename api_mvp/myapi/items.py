from dataclasses import dataclass, asdict
from datetime import datetime, date
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
    created_at: str


netflix = Item('Netflix', 'tv shows', state.INIT.value, date(2025, 1 ,1).isoformat())
hbo = Item('hbo', 'documentary', state.RUN.value, date(2025, 2 ,1).isoformat())
ps = Item('ps', 'ps games', state.PAUSE.value, date(2025, 3 ,1).isoformat())
xbox = Item('xbox', 'xbox games', state.STOP.value, date(2025, 4 ,1).isoformat())

subscriptions = [asdict(netflix), asdict(hbo), asdict(ps), asdict(xbox)]
