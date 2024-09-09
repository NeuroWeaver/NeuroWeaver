from collections import defaultdict
from systolic_sim.utils import *

class Genesys_Stats:
    def __init__(self) -> None:
        self.genesys_stats = defaultdict(lambda: 'NA')