# Generated by Django 2.0.9 on 2018-12-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PessoaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('usuario', models.CharField(max_length=255)),
                ('senha', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('disciplina', models.CharField(max_length=1000)),
                ('curso', models.CharField(max_length=1000)),
                ('turma', models.CharField(max_length=1000)),
            ],
        ),
    ]
