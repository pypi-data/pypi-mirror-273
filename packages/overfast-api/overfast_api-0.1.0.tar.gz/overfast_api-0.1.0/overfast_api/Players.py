from overfast_api.RestAdapter import RestAdapter
from overfast_api.models import PlayerSearchResult, PlayerSummary, PlayerStatSummary, PlayerCareerStats, PlayerFullData
from typing import List


class Players:
    def __init__(self):
        self.adapter = RestAdapter()

    def player_search(
            self,
            username: str,
            order_by: str = 'name:asc',
            offset: int = 0,
            limit: int = 20
    ) -> List[PlayerSearchResult]:

        params = {
            'name': username,
            'order_by': order_by,
            'offset': offset,
            'limit': limit,
        }
        result = self.adapter.get(endpoint='/players', params=params)
        players = []
        if "error" not in result.data[0]:
            for player in result.data[0]['results']:
                players.append(PlayerSearchResult(player))
        return players

    def get_player_summary(self, username: str) -> PlayerSummary:
        result = self.adapter.get(endpoint=f'/players/{username}/summary')
        return PlayerSummary(result.data[0])

    def get_player_stat_summary(self, username: str, gamemode: str = None, platform: str = None) -> PlayerStatSummary:
        params = {}
        if gamemode:
            params['gamemode'] = gamemode
        if platform:
            params['platform'] = platform
        result = self.adapter.get(endpoint=f'/players/{username}/stats/summary', params=params)
        return PlayerStatSummary(username, result.data[0])

    def get_player_career_stats(
            self,
            username: str,
            gamemode: str = "quickplay",
            platform: str = None,
            hero: str = None,
            with_labels: bool = False
    ) -> PlayerCareerStats:

        if with_labels:
            endpoint = f'/players/{username}/stats'
        else:
            endpoint = f'/players/{username}/stats/career'
        params = {"gamemode": gamemode}
        if platform:
            params['platform'] = platform
        if hero:
            params['hero'] = hero
        result = self.adapter.get(endpoint=endpoint, params=params)
        return PlayerCareerStats(username, result.data[0])

    def get_all_player_stats(self, username: str) -> PlayerFullData:
        result = self.adapter.get(endpoint=f'/players/{username}')
        return PlayerFullData(result.data[0])
