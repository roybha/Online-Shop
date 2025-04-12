from django.db import migrations, connection


def drop_all_tables(apps, schema_editor):
    """
    Method that drops all tables in the database
    :param apps: param that django is need to get access to the models
    :param schema_editor: param that django is need to change database schema
    :return: None
    """
    with connection.cursor() as cursor:
        # Array that consists of names of tables that app must drop
        tables = [
            'order_items',
            'products',
            'brands',
            'categories',
            'orders',
            'users'
        ]
        for table in tables:
            # Making an SQL query to drop the specific table
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(drop_all_tables),
    ]
