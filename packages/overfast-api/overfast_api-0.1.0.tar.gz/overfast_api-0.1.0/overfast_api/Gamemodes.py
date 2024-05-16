from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import Gamemode
from typing import List


class Modes:
    def __init__(self):
        self.adapter = RestAdapter()

    def get_all_modes(self) -> List[Gamemode]:
        result = self.adapter.get(endpoint='gamemodes')
        modes = []
        for mode in result.data:
            modes.append(Gamemode(mode))
        return modes
