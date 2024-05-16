from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import HeroSearchResult, Hero
from typing import Dict, List


class Heroes:
    def __init__(self):
        self.adapter = RestAdapter()

    def get_all_heroes(self, role: str = None, locale: str = 'en-us') -> List[HeroSearchResult]:
        params = dict(locale=locale)
        if role:
            params["role"] = role
        result = self.adapter.get(endpoint="heroes", params=params)
        heroes = []
        for hero in result.data:
            heroes.append(HeroSearchResult(hero))
        return heroes

    def get_hero(self, hero_key: str, locale: str = 'en-us') -> Hero:
        params = dict(locale=locale)
        result = self.adapter.get(endpoint=f"heroes/{hero_key}", params=params)
        return Hero(result.data[0])

    def get_roles(self) -> List[Dict]:
        result = self.adapter.get(endpoint="roles")
        return result.data

