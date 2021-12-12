# Generated by Django 3.2.9 on 2021-12-07 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_topic_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='access',
            field=models.CharField(choices=[(True, 'private'), (False, 'public')], default=True, max_length=10),
            preserve_default=False,
        ),
    ]