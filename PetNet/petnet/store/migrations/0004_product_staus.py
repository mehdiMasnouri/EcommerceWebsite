# Generated by Django 4.1.7 on 2023-04-01 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_options_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='staus',
            field=models.CharField(choices=[('draft', 'draft'), ('watingapproval', 'watingapproval'), ('active', 'active'), ('deleted', 'deleted')], default='active', max_length=50),
        ),
    ]