# Generated by Django 4.0.3 on 2022-03-12 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptkt', '0002_remove_tickets_interacao_interacoes_chamado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='anexo',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
