# Generated by Django 4.0.6 on 2023-08-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_userfollowers_unique_myfollower_follower_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollowers',
            constraint=models.UniqueConstraint(fields=('myFollower', 'follower'), name='unique_followers_constraint'),
        ),
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('myFollowing', 'following'), name='unique_following_constraint'),
        ),
    ]
