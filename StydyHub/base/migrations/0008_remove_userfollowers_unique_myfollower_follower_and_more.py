# Generated by Django 4.0.6 on 2023-08-07 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_userfollowers_unique_myfollower_follower_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userfollowers',
            name='unique_myFollower_follower',
        ),
        migrations.RemoveConstraint(
            model_name='userfollowing',
            name='unique_myFollowing_following',
        ),
    ]
