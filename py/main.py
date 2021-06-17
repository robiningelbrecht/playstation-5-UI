from jinja2 import Environment, FileSystemLoader
from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

env = Environment(loader=FileSystemLoader('templates'))

if __name__ == "__main__":
    scraper = PsnProfilesScraper()
    profile = scraper.get_profile("Fluttezuhher", False)

    print(env.get_template("index.tpl.html").render(
        games=profile.get_games(),
        summary=profile.get_summary(),
        rarest_trophies=profile.get_rarest_trophies(),
    ))
