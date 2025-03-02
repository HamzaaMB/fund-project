import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('strategy', models.CharField(max_length=100)),
                ('aum', models.DecimalField(blank=True, decimal_places=0, max_digits=20, null=True)),
                ('inception_date', models.DateField(blank=True, null=True)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
