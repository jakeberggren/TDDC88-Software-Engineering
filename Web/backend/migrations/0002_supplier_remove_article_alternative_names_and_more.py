# Generated by Django 4.1.1 on 2022-11-02 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, null=True)),
                ('supplier_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='alternative_names',
        ),
        migrations.RemoveField(
            model_name='article',
            name='sanitation_level',
        ),
        migrations.AddField(
            model_name='article',
            name='Z41',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='article',
            name='refill_unit',
            field=models.IntegerField(choices=[(1, 'Millilitres'), (2, 'Centilitres'), (3, 'Decilitres'), (4, 'Litres'), (5, 'Millimetres'), (6, 'Centimetres'), (7, 'Metres'), (8, 'Pieces'), (9, 'Crates'), (10, 'Bottles')], default=1),
        ),
        migrations.AddField(
            model_name='article',
            name='takeout_unit',
            field=models.IntegerField(choices=[(1, 'Millilitres'), (2, 'Centilitres'), (3, 'Decilitres'), (4, 'Litres'), (5, 'Millimetres'), (6, 'Centimetres'), (7, 'Metres'), (8, 'Pieces'), (9, 'Crates'), (10, 'Bottles')], default=1),
        ),
        migrations.AddField(
            model_name='storagespace',
            name='placement',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='storageunit',
            name='cost_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.costcenter'),
        ),
        migrations.AlterField(
            model_name='storagespace',
            name='article',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.article'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='time_of_transaction',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='ArticleHasSupplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier_article_nr', models.CharField(max_length=15, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.article')),
                ('article_supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='AlternativeArticleName',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.article')),
            ],
        ),
    ]