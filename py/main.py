import shutil

import requests
from jinja2 import Environment, FileSystemLoader
from psnprofiles_scraper.src.PsnProfilesScraper import PsnProfilesScraper

env = Environment(loader=FileSystemLoader('templates'))

if __name__ == "__main__":
    scraper = PsnProfilesScraper()
    profile = scraper.get_profile("Fluttezuhher", True)

    r = requests.get('https://url/to/image.jpg', stream=True)
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    with open('FB_IMG_1490534565948.jpg', 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    # Write to file
    with open("index.html", 'w') as out:
        out.write(env.get_template("index.tpl.html").render(
            games=profile.get_games(),
            summary=profile.get_summary(),
            rarest_trophies=profile.get_rarest_trophies(),
            recent_trophies=profile.get_recent_trophies(),
            milestones=profile.get_milestones(),
            trophy_cabinet=profile.get_trophy_cabinet()
        ))
