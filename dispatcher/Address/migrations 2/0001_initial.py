# Generated by Django 3.0.5 on 2020-04-16 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30, null=True)),
                ('lastname', models.CharField(max_length=30, null=True)),
                ('street', models.CharField(max_length=30, null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('state', models.CharField(max_length=30, null=True)),
                ('zipcode', models.IntegerField(default=0, null=True)),
                ('phone', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
