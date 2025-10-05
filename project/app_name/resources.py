from import_export import resources

from app_name.models import Book


class BookResource(resources.ModelResource):

    class Meta:
        model = Book