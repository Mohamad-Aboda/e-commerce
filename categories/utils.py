from .models import Category

def get_category(pk):
    try:
        return Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return None