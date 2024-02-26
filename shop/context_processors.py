from .models import Category


def categories(request):
    """
    Retrieves the top-level categories from the database and returns them in a dictionary.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}