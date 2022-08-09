import os
from .data_classes import VOICES_FOLDER, VoiceFile, Voice

__voices_folder = os.path.abspath(os.path.join(VOICES_FOLDER))

data_voices = Voice(
    user_name="spade",
    voices=[
        VoiceFile(name="对呀对呀", file_name="dydy.mp3", folder_path=__voices_folder),
    ],
)

__all__ = ["data_voices"]
