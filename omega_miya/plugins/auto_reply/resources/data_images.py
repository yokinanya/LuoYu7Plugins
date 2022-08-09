import os
from .data_classes import IMAGE_FOLDER, Image, ImageFile

__images_folder = os.path.abspath(os.path.join(IMAGE_FOLDER))

data_images = Image(
    user_name="spade",
    images=[
        ImageFile(name="转圈圈", file_name="circle.gif", folder_path=__images_folder),
    ],
)

__all__ = ["data_images"]
