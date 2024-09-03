import base64
import io
from django.core.files.base import ContentFile
from PIL import Image

def base64_to_contentfile(base64_data: str, filename: str) -> ContentFile:
    header, encoded = base64_data.split(",", 1)
    data = base64.b64decode(encoded)
    image_file = io.BytesIO(data)
    image = Image.open(image_file)
    image_io = io.BytesIO()
    image.save(image_io, format=image.format)
    image_content = ContentFile(image_io.getvalue(), filename)
    return image_content