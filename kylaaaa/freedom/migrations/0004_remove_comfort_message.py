from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freedom', '0003_post_comfort_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comfort_message',
        ),
    ]
