# Generated by Django 4.0 on 2022-01-12 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses_app', '0002_alter_apartment_options_alter_city_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='city',
            field=models.ForeignKey(db_column='city', on_delete=django.db.models.deletion.DO_NOTHING, to='houses_app.city'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='floor',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='id_house',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='laitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='rooms',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='sq',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='year',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='city',
            name='voivodeship',
            field=models.ForeignKey(db_column='voivodeship', on_delete=django.db.models.deletion.DO_NOTHING, to='houses_app.voivodeship'),
        ),
    ]