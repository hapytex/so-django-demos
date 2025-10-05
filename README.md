# [Question](https://stackoverflow.com/questions/79783053/)


I have a Django model with a custom save() method:

```
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        print(&#39;Saving...&#39;)
        super().save(*args, **kwargs)
```

When I create a new object through the Django admin, I see &quot;Saving...&quot; printed twice in the console.
# Answer


