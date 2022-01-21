# Generated by Django 4.0.1 on 2022-01-21 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_article_voter_comment_voter_alter_article_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='board.article')),
            ],
        ),
    ]