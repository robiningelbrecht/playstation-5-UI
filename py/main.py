from jinja2 import Environment, FileSystemLoader
from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

from MediaDownloader import MediaDownloader

env = Environment(loader=FileSystemLoader('templates'))

if __name__ == "__main__":
    scraper = PsnProfilesScraper()
    profile = scraper.get_profile("Fluttezuhher", True)

    downloader = MediaDownloader(profile)
    downloader.download_game_media()
    downloader.download_trophy_media()

    # Write to file
    with open("../index.html", 'w') as out:
        out.write(env.get_template("index.tpl.html").render(
            games=profile.get_games(),
            summary=profile.get_summary(),
            rarest_trophies=profile.get_rarest_trophies(),
            recent_trophies=profile.get_recent_trophies(),
            milestones=profile.get_milestones(),
            trophy_cabinet=profile.get_trophy_cabinet()
        ))
