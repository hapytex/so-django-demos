from django.db.models import QuerySet, Manager, Model
from sql_formatter.core import format_sql

def format_query(qs):
    if isinstance(qs, Model):
        qs = qs._base_manager
    if isinstance(qs, Manager):
        qs = qs.get_queryset()
    if isinstance(qs, QuerySet):
        qs = qs.query
    qs = format_sql(str(qs))
    print(qs)
    return qs

@property
def query_(self):
    return format_query(self)

QuerySet.query_ = query_