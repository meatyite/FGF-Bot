import requests
import json
from discord_webhooks import DiscordWebhooks
import os

__j__ = json.loads(open("settings.json", 'r').read())

api_key = __j__['api_key']
web_hook = DiscordWebhooks(__j__['web_hook'])


class Game:

    def __init__(self, title, shop_name, buy_url, price, currecny, added):
        self.title = title
        self.shop_name = shop_name
        self.buy_url = buy_url
        self.price = price
        self.currency = currecny
        self.added = added
        price_str = str(price) + " " + currecny
        if price == 0.00:
            price_str = "Free"
        self.announce_msg = "`{}` Is now on {} For {}!\nGet it now: {}".format(self.title, self.shop_name, price_str,
                                                                                 self.buy_url)
        if __j__['tag@everyone']:
            self.announce_msg = "@everyone " + self.announce_msg


class BothFilterTypesError(Exception):
    pass


def get_games():
    params = {
        'key': api_key,
    }
    if __j__['min_price'] <= 4.99:
        params['sort'] = 'price:asc'
    if __j__['country'] != 'default':
        params['country'] = __j__['country']
    r = requests.get(
        'https://api.isthereanydeal.com/v01/deals/list/',
        params=params
    ).content.decode()
    j = json.loads(r)
    games = []
    for item in j['data']['list']:
        game = Game(item['title'], item['shop']['name'], item['urls']['buy'], price=float(item['price_new']),
                    currecny=j['.meta']['currency'], added=item['added'])
        if game.price <= __j__['min_price']:
            if __j__['show_only'] and __j__['dont_show_only']:
                raise BothFilterTypesError("You need to enable only one of the two store filter types."
                                           " Please edit settings.json.")
            elif __j__['show_only'] and game.shop_name.lower() in __j__['show_only_list'].lower():
                   games.append(game)
            elif __j__['dont_show_only'] and not(game.shop_name.lower() in __j__['dont_show_only_list'].lower()):
                    games.append(game)
    return games


def write_json(games):
    f = open("yesterday_games.json", 'w')
    j = []
    for game in games:
        j.append({'title': game.title, 'shop_name': game.shop_name, 'buy_url': game.buy_url, 'added': game.added})
    f.write(json.dumps(j, indent=4))


def read_json(games):
    j = json.loads(open("yesterday_games.json", "r").read())
    for game in games:
        isAlreadyPosted = False
        for game_j in j:
            if game_j['buy_url'] == game.buy_url and game_j['added'] == game.added:
                isAlreadyPosted = True
        if isAlreadyPosted:
            print("{} Already posted.".format(game.title))
        else:
            print("Posting {}.".format(game.title))
            web_hook.set_content(content=game.announce_msg)
            web_hook.send()


def first_time_send(games):
    web_hook.set_content(content="Already-posted list not found, posting current free games & creating list.")
    web_hook.send()
    for game in games:
        web_hook.set_content(content=game.announce_msg)
        web_hook.send()
    write_json(games)


if __name__ == "__main__":
    games = get_games()
    if os.path.isfile("yesterday_games.json"):
        read_json(games)
        write_json(games)
    else:
        first_time_send(games)
