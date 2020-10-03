# Generated by Django 3.1.1 on 2020-09-21 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0026_auto_20200710_2250'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptionpart',
            options={'permissions': [('notified_on_subscriptionpart_creation', 'Wird bei Abo Bestandteil Erstellung informiert'), ('notified_on_subscriptionpart_cancellation', 'Wird bei Abo Bestandteil Kündigung informiert')], 'verbose_name': 'Abo Bestandteil', 'verbose_name_plural': 'Abo Bestandteile'},
        ),
        migrations.AddField(
            model_name='subscription',
            name='nickname',
            field=models.CharField(blank=True, help_text='Ersetzt die Mit-Abo-BezieherInnen auf der Depot-Liste.', max_length=30, verbose_name='Spitzname'),
        ),
        migrations.AlterField(
            model_name='job',
            name='multiplier',
            field=models.PositiveIntegerField(default=1, verbose_name='Arbeitseinsatz vielfaches'),
        ),
    ]