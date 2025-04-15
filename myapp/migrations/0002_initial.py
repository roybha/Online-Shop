import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('laptop', 'Laptop'), ('smartphone', 'Smartphone')], max_length=20, unique=True)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=False)),
                ('order_date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('screen_size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('screen_resolution', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='Формат має бути як 1920x1080', regex='^\\d{3,4}x\\d{3,4}$')])),
                ('screen_ref_rate', models.IntegerField(default=60)),
                ('sim_quantity', models.IntegerField(default=1)),
                ('network_generations', models.CharField(max_length=20)),
                ('cpu_model', models.CharField(max_length=15)),
                ('cpu_cores_num', models.IntegerField(default=8)),
                ('ram', models.IntegerField(default=4)),
                ('storage', models.IntegerField(default=120)),
                ('main_camera', models.CharField(max_length=30)),
                ('max_video_resolution', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Формат має бути як "7680 x 4320" або "7680 x 4320 8K UHD"', regex='^\\d{3,5}\\sx\\s\\d{3,5}(?:\\s[\\w\\s]{2,15})?$')])),
                ('frontal_camera', models.CharField(max_length=30)),
                ('nfc', models.BooleanField(default=False)),
                ('connector_type', models.CharField(max_length=10)),
                ('battery', models.IntegerField(default=2000)),
                ('weight', models.IntegerField(default=200)),
            ],
            options={
                'db_table': 'smartphones',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], max_length=10)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('screen_size', models.DecimalField(decimal_places=2, max_digits=10)),
                ('scree_resolution', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='Формат має бути як 1920x1080', regex='^\\d{3,4}x\\d{3,4}$')])),
                ('screen_ref_rate', models.IntegerField(default=60)),
                ('cpu_model', models.CharField(max_length=15)),
                ('cpu_cores_num', models.IntegerField(default=4)),
                ('cpu_frequency', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ram', models.IntegerField(default=4)),
                ('ram_type', models.CharField(max_length=5)),
                ('storage', models.IntegerField(default=120)),
                ('storage_type', models.CharField(max_length=5)),
                ('gpu_model', models.CharField(max_length=15)),
                ('cpu_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpu_brand', to='myapp.brand')),
                ('gpu_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gpu_brand', to='myapp.brand')),
            ],
            options={
                'db_table': 'laptops',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model_name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('category_prod_id', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.product')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user'),
        ),
    ]
