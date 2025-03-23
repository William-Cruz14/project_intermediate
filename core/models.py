from django.db import models
from stdimage import StdImageField
from django.db.models import signals
from django.template.defaultfilters import slugify

class Base(models.Model):
    created = models.DateTimeField('Created Date', auto_now_add=True)
    modified = models.DateTimeField('Modified Date', auto_now=True)
    active = models.BooleanField('Active', default=True)
    class Meta:
        abstract = True

class Product(Base):
    name = models.CharField('Product Name', max_length=100)
    cost = models.DecimalField('Product Cost', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Product Stock')
    image = StdImageField('Product Image', upload_to='product_images', variations={'thumbnail':(200, 200)})
    slug = models.SlugField('Product Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.name


def product_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)

signals.pre_save.connect(product_pre_save, sender=Product)