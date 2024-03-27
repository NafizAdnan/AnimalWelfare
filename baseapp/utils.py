import requests
from django.conf import settings

def upload_image_to_imagga(image_path):
    response = requests.post(
        'https://api.imagga.com/v2/uploads',
        auth=(settings.IMAGGA_API_KEY, settings.IMAGGA_API_SECRET),
        files={'image': open(image_path, 'rb')}
    )
    return response.json()

def get_image_categories(image_id):
    response = requests.get(
        f'https://api.imagga.com/v2/categories/personal_photos?image_upload_id={image_id}',
        auth=(settings.IMAGGA_API_KEY, settings.IMAGGA_API_SECRET)
    )
    return response.json()
