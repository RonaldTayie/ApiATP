import base64
import io
import os

from django.core.files.base import ContentFile
from PIL import Image

from ApiATP import settings
from parts.models import Part, Category, PartImage


def base64_to_contentfile(base64_data: str, filename: str) -> ContentFile:
    header, encoded = base64_data.split(",", 1)
    data = base64.b64decode(encoded)
    image_file = io.BytesIO(data)
    image = Image.open(image_file)
    image_io = io.BytesIO()
    image.save(image_io, format=image.format)
    image_content = ContentFile(image_io.getvalue(), filename)
    return image_content


def process_parts_data(data):
    for file_data in data:
        file_name = file_data.get('file')
        part_type = file_data.get('type')
        content = file_data.get('content', [])

        # Get or create the category
        category, created = Category.objects.get_or_create(name=part_type)

        for content_data in content:
            part_name = content_data.get('caption')
            caption = content_data.get('filename').split('.')[0]
            image_content = content_data.get('image')

            # Get or create the part
            part, created = Part.objects.get_or_create(
                category=category,
                part=part_name,
                defaults={'part_description': ''}
            )

            # If image content is provided, create the PartImage
            if image_content:
                # Decode base64 and save the image
                image_data = base64.b64decode(image_content)
                image_name = f"{part_name}---{caption}.png"
                image_name_db = f"part-images/{part_name}---{caption}.png"
                image_path = os.path.join(settings.MEDIA_ROOT, 'part-images', image_name)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(image_path), exist_ok=True)

                # Write the image to the file system
                with open(image_path, "wb") as img_file:
                    img_file.write(image_data)

                # Save the image path in the database
                PartImage.objects.create(part=part, image=image_name_db,)
