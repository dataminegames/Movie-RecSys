# Generated by Django 4.0.3 on 2022-11-12 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('genres', models.CharField(max_length=20)),
                ('nation', models.CharField(max_length=10)),
                ('open_date', models.PositiveSmallIntegerField()),
                ('companys', models.CharField(max_length=100)),
                ('actors', models.TextField()),
                ('directors', models.TextField()),
                ('poster', models.TextField()),
                ('link', models.TextField()),
                ('rating_audi', models.FloatField()),
                ('rating_critic', models.FloatField()),
                ('rating_netizen', models.FloatField()),
                ('audi_acc', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(max_length=2)),
                ('address', models.CharField(max_length=10)),
                ('mbti', models.CharField(max_length=4)),
                ('vote_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recsys.movieinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recsys.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='MovieChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recsys.movieinfo')),
            ],
        ),
    ]
