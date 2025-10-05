import uuid

from django.conf import settings
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping, blank=True)

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