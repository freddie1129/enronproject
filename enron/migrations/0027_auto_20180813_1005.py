# Generated by Django 2.0.7 on 2018-08-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enron', '0026_auto_20180813_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawemailfrom',
            name='e_content',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='rawemailfrom',
            name='e_subject',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
