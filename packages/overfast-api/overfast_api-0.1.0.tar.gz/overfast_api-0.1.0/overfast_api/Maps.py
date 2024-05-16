from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import Map
from typing import List


class Maps:
    def __init__(self):
        self.adapter = RestAdapter()

    def get_maps(self, gamemode: str = None) -> List[Map]:
        if gamemode:
            params = {'gamemode': gamemode}
        results = self.adapter.get('/maps', params=params if gamemode else None)
        print(results.data)
        maps = []
        for map in results.data:
            maps.append(Map(map))
        return maps
