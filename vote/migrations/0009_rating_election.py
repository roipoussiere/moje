# Generated by Django 2.0.3 on 2018-04-07 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0008_election_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='election',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vote.Election'),
        ),
    ]