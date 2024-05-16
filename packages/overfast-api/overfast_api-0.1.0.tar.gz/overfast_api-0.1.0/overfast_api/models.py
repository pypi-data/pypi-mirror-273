from typing import Dict, List


class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        self.status_code = status_code
        self.message = message
        self.data = data if data else []


class Hero:
    def __init__(self, data: dict):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.name = data.get("name", None)
        self.description = data.get("description", None)
        self.portrait_url = data.get("portrait", None)
        self.role = data.get("role", None)
        self.location = data.get("location", None)
        self.age = data.get("age", None)
        self.birthday = data.get("birthday", None)
        self.hitpoints = data.get("hitpoints", None)
        self.abilities = data.get("abilities", None)

    def to_dict(self):
        return self.__dict__


class HeroSearchResult:
    def __init__(self, data: dict):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.name = data.get("name", None)
        self.portrait_url = data.get("portrait", None)
        self.role = data.get("role", None)


class HeroCareerStats:
    def __init__(
            self,
            hero_name: str,
            data: Dict
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.hero_name = hero_name
        if type(data) is list:
            data = data[0]
        self.assists = data.get("assists", None)
        self.average = data.get("average", None)
        self.best = data.get("best", None)
        self.combat = data.get("combat", None)
        self.game = data.get("game", None)
        self.hero_specific = data.get("hero_specific", None)


class HeroStatSummary:
    def __init__(
            self,
            hero_name: str,
            data: Dict
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.hero_name = hero_name
        self.games_lost = data.get("games_lost", None)
        self.games_played = data.get("games_played", None)
        self.games_won = data.get("games_won", None)
        self.kda = data.get("kda", None)
        self.time_played = data.get("time_played", None)
        self.winrate = data.get("winrate", None)
        self.average_assists = data["average"].get("assists", None)
        self.average_damage = data["average"].get("damage", None)
        self.average_deaths = data["average"].get("deaths", None)
        self.average_eliminations = data["average"].get("eliminations", None)
        self.average_healing = data["average"].get("healing", None)
        self.total_assists = data["total"].get("assists", None)
        self.total_damage = data["total"].get("damage", None)
        self.total_deaths = data["total"].get("deaths", None)
        self.total_eliminations = data["total"].get("eliminations", None)
        self.total_healing = data["total"].get("healing", None)


class PlayerSearchResult:
    def __init__(
            self,
            data: Dict
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.player_id = data["player_id"]
        self.name = data["name"]
        self.avatar_url = data["avatar"]
        self.namecard_url = data["namecard"]
        self.title = data["title"]
        self.blizzard_id = data["blizzard_id"]


class PlayerStatSummary:
    def __init__(
            self,
            username: str,
            data: Dict,
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.username = username
        self.games_lost = data["general"].get("games_lost", None)
        self.games_won = data["general"].get("games_won", None)
        self.games_played = data["general"].get("games_played", None)
        self.winrate = data["general"].get("winrate", None)
        self.kda = data["general"].get("kda", None)
        self.averages = data["general"].get("averages", None)
        self.totals = data["general"].get("totals", None)
        self.hero_stats = {}
        for key, value in data["heroes"].items():
            self.hero_stats[key] = HeroStatSummary(key, value)


class PlayerCareerStats:
    def __init__(
            self,
            username: str,
            data: Dict,
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.username = username
        for key, value in data.items():
            setattr(self, key, HeroCareerStats(key, value))


class CompStats:
    def __init__(
            self,
            platform: str,
            data: Dict
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.platform = platform,
        self.season = data.get("season", None),
        if data['tank']:
            self.tank_division = data['tank'].get('division', None)
            self.tank_tier = data['tank'].get('tier', None)
        else:
            self.tank_division = None
            self.tank_tier = None
        if data["damage"]:
            self.damage_division = data["damage"].get('division', None)
            self.damage_tier = data["damage"].get('tier', None)
        else:
            self.damage_division = None
            self.damage_tier = None
        if data["support"]:
            self.support_division = data["support"].get('division', None)
            self.support_tier = data["support"].get('tier', None)
        else:
            self.support_division = None
            self.support_tier = None


class PlayerSummary:
    def __init__(
            self,
            data: Dict
    ):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.username = data.get("username", None)
        self.avatar_url = data.get("avatar", None)
        self.name_card_url = data.get("namecard", None)
        self.title = data.get("title", None)
        self.endorsement_level = data["endorsement"].get("level", None)
        if data["competitive"]["pc"]:
            self.pc_comp_stats = CompStats(platform="pc", data=data["competitive"]["pc"])
        else:
            self.pc_comp_stats = None
        if data["competitive"]["console"]:
            self.console_comp_stats = CompStats(platform="console", data=data["competitive"]["console"])
        else:
            self.console_comp_stats = None


class PlayerFullData:
    def __init__(self, data: Dict):
        if has_error(data) in data:
            self.error = data.get("error", "Unknown Error")
            return

        self.player_summary = PlayerSummary(data["summary"])
        pc_stats = data['stats'].get('pc', None)
        console_stats = data['stats'].get('console', None)
        self.stats = {
            'pc': {
                'quickplay': {
                    "heroes_comparisons": {},
                    "career_stats": {}
                },
                'competitive': {
                    "heroes_comparisons": {},
                    "career_stats": {}
                }
            },
            'console': {
                'quickplay': {
                    "heroes_comparisons": {},
                    "career_stats": {}
                },
                'competitive': {
                    "heroes_comparisons": {},
                    "career_stats": {}
                }
            }
        }
        if pc_stats is not None:
            self.stats['pc']['quickplay']["heroes_comparisons"] = {}
            for key, value in pc_stats['quickplay']["heroes_comparisons"].items():
                self.stats['pc']['quickplay']["heroes_comparisons"][key] = value
            for key, value in pc_stats['quickplay']['career_stats'].items():
                self.stats['pc']['quickplay']['career_stats'][key] = HeroCareerStats(key, value)
            self.stats['pc']['competitive']["heroes_comparisons"] = {}
            for key, value in pc_stats['competitive']["heroes_comparisons"].items():
                self.stats['pc']['competitive']["heroes_comparisons"][key] = value
            for key, value in pc_stats['competitive']['career_stats'].items():
                self.stats['pc']['competitive']['career_stats'][key] = HeroCareerStats(key, value)
        if console_stats is not None:
            self.stats['console']['quickplay']["heroes_comparisons"] = {}
            for key, value in console_stats['quickplay']["heroes_comparisons"].items():
                self.stats['console']['quickplay']["heroes_comparisons"][key] = value
            for key, value in console_stats['quickplay']['career_stats']:
                self.stats['console']['quickplay']['career_stats'][key] = HeroCareerStats(key, value)
            self.stats['console']['competitive']["heroes_comparisons"] = {}
            for key, value in console_stats['competitive']["heroes_comparisons"].items():
                self.stats['console']['competitive']["heroes_comparisons"][key] = value
            for key, value in console_stats['competitive']['career_stats'].items():
                self.stats['console']['competitive']['career_stats'][key] = HeroCareerStats(key, value)


class Gamemode:
    def __init__(self, data: Dict):
        self.key = data['key']
        self.name = data['name']
        self.icon_url = data['icon']
        self.description = data['description']
        self.screenshot_url = data['screenshot']


class Map:
    def __init__(self, data: Dict):
        self.name = data['name']
        self.screenshot_url = data['screenshot']
        self.gamemode = data['gamemodes']
        self.location = data['location']
        self.country_code = data['country_code']


def has_error(data: dict):
    return 'error' in data
