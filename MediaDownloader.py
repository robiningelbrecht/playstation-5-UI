import shutil
import os

import requests
from pathlib import Path
from psnprofiles_scraper.src.PsnProfiles.Profile import Profile
from psnprofiles_scraper.src.ProgressBar import ProgressBar


class MediaDownloader:

    def __init__(self, profile: Profile):
        self.profile = profile

    def download_game_media(self):
        games = self.profile.get_games()

        progress = ProgressBar()
        progress.max = len(games)

        for game in games:
            game_id = self.__extract_game_id_from_uri(game.uri.replace("https://psnprofiles.com", ""))

            # Update progress message.
            progress.update_message("Downloading " + game_id)

            files_to_download = {
                "thumbnail": game.thumbnail_uri,
                "cover": game.cover_uri,
                "background": game.background_uri
            }

            for style, uri in files_to_download.items():
                if not uri:
                    # Uri is empty for some reason. Cannot proceed to download file.
                    progress.next()
                    continue

                ext = uri.split(".")[-1]
                file_destination = 'assets/profile/' + game_id + '/' + style + '.' + ext

                if os.path.exists("web/" + file_destination):
                    # File already exists. Do not download again.
                    # Update game instance with new image location.
                    if style == "thumbnail":
                        game.thumbnail_uri = file_destination
                    elif style == "cover":
                        game.cover_uri = file_destination
                    elif style == "background":
                        game.background_uri = file_destination

                    progress.next()
                    continue

                r = requests.get(uri, stream=True)

                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
                    # Create directory if needed.
                    Path('web/assets/profile/' + game_id).mkdir(parents=True, exist_ok=True)
                    # Download image.
                    with open("web/" + file_destination, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)

                    # Update game instance with new image location.
                    if style == "thumbnail":
                        game.thumbnail_uri = file_destination
                    elif style == "cover":
                        game.cover_uri = file_destination
                    elif style == "background":
                        game.background_uri = file_destination

            progress.next()

        # Update progress message.
        progress.update_message("Complete")
        progress.finish()

    def download_trophy_media(self):
        rarest_trophies = self.profile.get_rarest_trophies()
        recent_trophies = self.profile.get_recent_trophies()
        trophy_milestones = self.profile.get_milestones()
        trophy_cabinet = self.profile.get_trophy_cabinet()

        progress = ProgressBar()
        progress.max = len(rarest_trophies) + len(recent_trophies) + len(trophy_milestones) + len(trophy_cabinet)

        for trophy in rarest_trophies:
            if not trophy.icon_uri:
                progress.next()
                continue

            # Update progress message.
            progress.update_message("Downloading " + trophy.icon_uri)
            trophy.icon_uri = self.__download_trophy_icon(trophy.icon_uri)
            progress.next()

        for trophy in recent_trophies:
            if not trophy.icon_uri:
                progress.next()
                continue

            # Update progress message.
            progress.update_message("Downloading " + trophy.icon_uri)
            trophy.icon_uri = self.__download_trophy_icon(trophy.icon_uri)
            progress.next()

        for trophy in trophy_cabinet:
            if not trophy.icon_uri:
                progress.next()
                continue

            # Update progress message.
            progress.update_message("Downloading " + trophy.icon_uri)
            trophy.icon_uri = self.__download_trophy_icon(trophy.icon_uri)
            progress.next()

        for milestone in trophy_milestones:
            if not milestone.trophy_icon:
                progress.next()
                continue
            # Update progress message.
            progress.update_message("Downloading " + milestone.trophy_icon)
            milestone.trophy_icon = self.__download_trophy_icon(milestone.trophy_icon)
            progress.next()

        # Update progress message.
        progress.update_message("Complete")
        progress.finish()

    def __download_trophy_icon(self, uri: str):
        filename = uri.split("/")[-1]
        file_destination = 'assets/profile/trophies/' + filename

        if os.path.exists("web/" + file_destination):
            # File already exists. Do not download again.
            # Update trophy instance with new image location.
            return file_destination

        r = requests.get(uri, stream=True)

        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Create directory if needed.
            Path('web/assets/profile/trophies').mkdir(parents=True, exist_ok=True)
            # Download image.
            with open("web/" + file_destination, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            # Update trophy instance with new icon location.
            return file_destination

    def __extract_game_id_from_uri(self, uri: str) -> str:
        # /trophies/10034-foxyland/PSNname
        return uri.split('/')[2]
