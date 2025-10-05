import uuid
from functools import cached_property

import tablib
from django.conf import settings
from django.db import models
from import_export.formats.base_formats import DEFAULT_FORMATS


class Topping(models.Model):
    name = models.CharField(max_length=30)


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )


class City(models.Model):
    # ...
    pass


class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


class Chapter(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=256)
    chapters = models.ManyToManyField(Chapter)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)


class Restaurant(models.Model):
    pizzas = models.ManyToManyField(Pizza, related_name="restaurants")
    best_pizza = models.ForeignKey(
        Pizza, related_name="championed_by", on_delete=models.CASCADE
    )

class Mining(models.Model):
    mining_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True,null=True)
    profile_pic = models.ImageField(upload_to='UploadedProfilePicture/', default="ProfileAvatar/avatar.png", blank=True)
    following = models.ManyToManyField(
        'Profile',  # Refers to the User model itself
        symmetrical=False,  # If A follows B, B doesn't automatically follow A
        related_name='followers',  # Reverse relationship: get followers of a user
        blank=True,
    )


FORMAT_DICT = {x.CONTENT_TYPE: x() for x in DEFAULT_FORMATS if x().can_import()}

class ImportedFile(models.Model):
    file = models.FileField(upload_to='tmp/')
    file_format = models.CharField(
        choices=[(x.CONTENT_TYPE, x.CONTENT_TYPE) for x in DEFAULT_FORMATS if x().can_import()],
        max_length=255,
    )
    matching = models.JSONField(default=dict)

    @property
    def file_format_obj(self):
        return FORMAT_DICT.get(self.file_format)

    @cached_property
    def dataset(self):
        file_data = b''
        for chunk in self.file.chunks():
            file_data += chunk
        return self.file_format_obj.create_dataset(file_data.decode('utf-8'))

    def mapped_dataset_with(self, matching=None):
        if matching is None:
            matching = self.matching
        dataset = self.dataset
        headers = ['a']
        target = None
        n = len(dataset)
        empty = (None,)*n
        for tar, (src1, src2) in matching.items():
            src = empty
            if src1 is not None:
                src = dataset[src1]
            elif src2:
                src = (src2,)*n
            if target:
                target.append_col(src, header=tar)
            else:
                target = tablib.Dataset(*[(x,) for x in src], headers=[tar])
        return target

    @cached_property
    def mapped_dataset(self):
        return self.mapped_dataset_with()

    def import_with(self, resource, matching=None, dry_run=True):
        dataset = self.mapped_dataset_with(matching)
        return resource.import_data(dataset, dry_run=dry_run)

    @cached_property
    def headers(self):
        return self.dataset.headers