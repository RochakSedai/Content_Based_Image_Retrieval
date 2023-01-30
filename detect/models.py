from django.db import models
import os
from django.core.files.storage import FileSystemStorage
# Create your models here.

def rename_path(instance, filename):
    upload_to = 'photos/products/'
    ext = 'jpg'
    name = 'shoes'
    filename = '{}.{}'.format(name,ext)
    return os.path.join(upload_to, filename)
    
class OverwriteStorage(FileSystemStorage):
    
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


class Product(models.Model):
    image = models.ImageField(storage=OverwriteStorage(), upload_to=rename_path)
    

    def __str__(self):
        return self.image


