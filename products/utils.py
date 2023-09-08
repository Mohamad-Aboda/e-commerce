import requests
from io import BytesIO
from django.core.files import File

def product_image_directory_path(inst, file_name):
    return f"product_images/{inst.product.name}/{file_name}"


def multiple_image_upload(request):
    if isinstance(request.FILES.getlist("image"), list) and len(request.FILES.getlist("image")) > 1:
        return True
    return False

test_image_cache = {}

def set_default_product_test_image() -> File:
    # Check if the image is already cached
    if 'default_product_image' in test_image_cache:
        return test_image_cache['default_product_image']
    test_img_url = "https://bit.ly/3vQgl0t"
    response = requests.get(test_img_url)
    
    if response.status_code == 200:
        img_stream = BytesIO(response.content)
        img_file = File(img_stream)
        # Cache the image for future use
        test_image_cache['default_product_image'] = img_file
        return img_file
    else:
        raise Exception("Failed to retrieve the test image.")


