from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля id, name, price, image, release_date, lte_exists и slug
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=250)
    release_date = models.DateField(auto_now=False)
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return (f'{self.name}, {self.price}')
