# Generated by Django 4.1.3 on 2022-11-06 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0004_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='photos/products/shoes.jpg'),
        ),
    ]
