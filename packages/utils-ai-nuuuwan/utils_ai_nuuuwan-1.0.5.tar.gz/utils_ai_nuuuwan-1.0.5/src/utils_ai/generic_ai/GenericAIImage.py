import os
import tempfile

from utils_base import Hash, Log
from utils_www import WWW

log = Log('GenericAIImage')


class GenericAIImage:
    def get_image_url(self, prompt: str) -> str:
        raise NotImplementedError

    def draw(self, prompt: str):
        dir_desktop = os.environ.get('DIR_DESKTOP') or tempfile.gettempdir()
        h = Hash.md5(prompt)[:8]
        image_path = os.path.join(dir_desktop, f'dalle-{h}.png')
        if os.path.exists(image_path):
            log.warn(f'Image already exists.')
            return image_path

        try:
            image_url = self.get_image_url(prompt)
            WWW.download_binary(image_url, image_path)
            return image_path
        except Exception as e:
            log.error(str(e))
            return None
