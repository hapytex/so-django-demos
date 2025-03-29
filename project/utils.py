from django.db.models import Manager, Model, QuerySet
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


QuerySet.query_ = property(format_query)
