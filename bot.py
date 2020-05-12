import requests
import json
from discord_webhooks import DiscordWebhooks
import os

__j__ = json.loads(open("settings.json", 'r').read())

apiKey = __j__['apikey'] # https://isthereanydeal.com API key
webhook = DiscordWebhooks(__j__['webhook'])


class Game:

    def __init__(self, title, shop_name, buy_url, added):
        self.title = title
        self.shop_name = shop_name
        self.buy_url = buy_url
        self.added = added
        self.announce_msg = "`{}` Is now on {} For Free!\nGet it now: {}".format(self.title, self.shop_name,
                                                                                 self.buy_url)
        if __j__['tag@everyone']:
            self.announce_msg = "@everyone " + self.announce_msg


def get_games():
    r = requests.get(
        'https://api.isthereanydeal.com/v01/deals/list/',
        params={
            'key': apiKey,
            'sort': 'price:asc'
        }
    ).content.decode()
    j = json.loads(r)
    games = []
    for item in j['data']['list']:
        if item['price_new'] == 0 and not(item['shop']['name'].lower()) in __j__['storefilter'].lower():
            game = Game(item['title'], item['shop']['name'], item['urls']['buy'], added=item['added'])
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
            webhook.set_content(content=game.announce_msg)
            webhook.send()


def first_time_send(games):
    webhook.set_content(content="Already-posted list not found, posting current free games & creating list.")
    webhook.send()
    for game in games:
        webhook.set_content(content=game.announce_msg)
        webhook.send()
    write_json(games)


if __name__ == "__main__":
    games = get_games()
    if os.path.isfile("yesterday_games.json"):
        read_json(games)
        write_json(games)
    else:
        first_time_send(games)
