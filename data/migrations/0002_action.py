# Generated by Django 2.2 on 2020-09-04 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(db_index=True)),
                ('end', models.DateTimeField(db_index=True)),
                ('duration', models.FloatField()),
            ],
            options={
                'db_table': 'tbl_action',
            },
        ),
    ]