import argparse

from jinja2 import Environment, FileSystemLoader
from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

from MediaDownloader import MediaDownloader

env = Environment(loader=FileSystemLoader('templates'))

if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser(description='Scrape a PSN profile and create a PS5 like UI for it.')
    parser.add_argument('username', type=str, help='PSN username to scrape')
    # Read arguments from the command line
    args = parser.parse_args()

    scraper = PsnProfilesScraper()
    profile = scraper.get_profile(args.username, True)

    downloader = MediaDownloader(profile)
    downloader.download_game_media()
    downloader.download_trophy_media()

    # Write to file
    with open("web/index.html", 'w') as out:
        out.write(env.get_template("index.tpl.html").render(
            name=profile.get_name(),
            avatar=profile.get_avatar(),
            games=profile.get_games(),
            summary=profile.get_summary(),
            rarest_trophies=profile.get_rarest_trophies(),
            recent_trophies=profile.get_recent_trophies(),
            milestones=profile.get_milestones(),
            trophy_cabinet=profile.get_trophy_cabinet()
        ))
