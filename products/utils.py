def product_image_directory_path(inst, file_name):
    return f"product_images/{inst.product.name}/{file_name}"


def multiple_image_upload(request):
    if isinstance(request.FILES.getlist("image"), list) and len(request.FILES.getlist("image")) > 1:
        return True
    return False


