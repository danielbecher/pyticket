# Generated by Django 4.0.3 on 2022-03-16 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptkt', '0004_alter_interacoes_anexo_alter_tickets_prioridade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=250)),
                ('porta', models.CharField(max_length=5)),
                ('usuario', models.CharField(max_length=100)),
                ('senha', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='tickets',
            name='prioridade',
            field=models.CharField(max_length=20),
        ),
    ]
