# Generated by Django 4.1.3 on 2023-05-27 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_obtainedresultmachine_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obtainedresultmachine',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
