from jinja2 import Environment, FileSystemLoader
from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

env = Environment(loader=FileSystemLoader('templates'))

if __name__ == "__main__":
    scraper = PsnProfilesScraper()
    profile = scraper.get_profile("Fluttezuhher", False)

    games = ""
    for game in profile.get_games():
        template_slide_game = env.get_template("slide-game.html")
        games = games + template_slide_game.render(thumb=game.thumbnail_uri, title=game.title, platform=game.platform)

    index = env.get_template("index.html")

    print(index.render(games=games))
