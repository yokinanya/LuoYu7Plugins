import os
import random
from dataclasses import dataclass
from typing import List, Optional

VOICES_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "voices"))
IMAGE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "images"))


@dataclass
class VoiceFile:
    name: str
    file_name: str
    folder_path: str


@dataclass
class Voice:
    user_name: str
    voices: List[VoiceFile]

    def get_voice(self, keyword: str) -> Optional[str]:
        result = [x for x in self.voices if x.name == keyword]
        if not result:
            result = self.voices
        voice = random.choice(result)
        return os.path.abspath(os.path.join(voice.folder_path, voice.file_name))


@dataclass
class ImageFile:
    name: str
    file_name: str
    folder_path: str


@dataclass
class Image:
    user_name: str
    images: List[ImageFile]

    def get_image(self, keyword: str) -> Optional[str]:
        result = [x for x in self.images if x.name == keyword]
        if not result:
            result = self.images
        image = random.choice(result)
        return os.path.abspath(os.path.join(image.folder_path, image.file_name))


__all__ = ["VOICES_FOLDER", "VoiceFile", "Voice", "IMAGE_FOLDER", "ImageFile", "Image"]
