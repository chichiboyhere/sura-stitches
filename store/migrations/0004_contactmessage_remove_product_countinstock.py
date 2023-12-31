# Generated by Django 4.2.2 on 2023-07-21 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_size_orderitem_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, null=True)),
                ('email', models.CharField(max_length=88)),
                ('subject', models.CharField(max_length=64)),
                ('message', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='countInStock',
        ),
    ]
