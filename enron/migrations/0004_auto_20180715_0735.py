# Generated by Django 2.0.7 on 2018-07-15 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enron', '0003_auto_20180715_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bccemail',
            name='fromAddress',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ccemail',
            name='fromAddress',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='email',
            name='emailId',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='toemail',
            name='fromAddress',
            field=models.CharField(max_length=200),
        ),
    ]
