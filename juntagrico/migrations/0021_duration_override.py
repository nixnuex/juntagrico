# Generated by Django 3.0.3 on 2020-03-29 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('juntagrico', '0021_auto_20200329_2059'), ('juntagrico', '0022_auto_20200329_2114')]

    dependencies = [
        ('juntagrico', '0020_auto_20200123_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='recuringjob',
            name='duration_override',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='Wenn nicht angegeben, wird die Dauer von der Jobart übernommen.', null=True, verbose_name='Besondere Dauer in Stunden'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='coordinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member', verbose_name='KoordinatorIn'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='email',
            field=models.EmailField(blank=True, help_text='Wenn leer wird E-Mail-Adresse von KoordinatorIn angezeigt', max_length=254, null=True, verbose_name='E-Mail'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='hidden',
            field=models.BooleanField(default=False, help_text='Nicht auf der "Tätigkeitsbereiche"-Seite anzeigen. Einsätze bleiben sichtbar.', verbose_name='versteckt'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='areas', to='juntagrico.Member', verbose_name='Mitglieder'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='show_coordinator_phonenumber',
            field=models.BooleanField(default=False, verbose_name='Telefonnummer von KoordinatorIn anzeigen'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='job_extras',
            field=models.ManyToManyField(blank=True, related_name='assignments', to='juntagrico.JobExtra', verbose_name='Job Extras'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member', verbose_name='Mitglied'),
        ),
        migrations.AlterField(
            model_name='extrasubscriptiontype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='types', to='juntagrico.ExtraSubscriptionCategory'),
        ),
        migrations.AlterField(
            model_name='job',
            name='infinite_slots',
            field=models.BooleanField(default=False, verbose_name='Unendlich Plätze'),
        ),
        migrations.AlterField(
            model_name='job',
            name='slots',
            field=models.PositiveIntegerField(default=0, verbose_name='Plätze'),
        ),
        migrations.AlterField(
            model_name='job',
            name='time',
            field=models.DateTimeField(verbose_name='Zeitpunkt'),
        ),
        migrations.AlterField(
            model_name='jobtype',
            name='activityarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea', verbose_name='Tätigkeitsbereich'),
        ),
        migrations.AlterField(
            model_name='member',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='E-Mail-Adresse bestätigt'),
        ),
        migrations.AlterField(
            model_name='member',
            name='inactive',
            field=models.BooleanField(default=False, help_text='Sperrt Login und entfernt von E-Mail-Listen', verbose_name='inaktiv'),
        ),
        migrations.AlterField(
            model_name='member',
            name='notes',
            field=models.TextField(blank=True, help_text='Notizen für Administration. Nicht sichtbar für Mitglied', max_length=1000, verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='onetimejob',
            name='activityarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea', verbose_name='Tätigkeitsbereich'),
        ),
        migrations.AlterField(
            model_name='recuringjob',
            name='additional_description',
            field=models.TextField(blank=True, default='', max_length=1000, verbose_name='Zusätzliche Beschreibung'),
        ),
        migrations.AlterField(
            model_name='recuringjob',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.JobType', verbose_name='Jobart'),
        ),
        migrations.AlterField(
            model_name='share',
            name='notes',
            field=models.TextField(blank=True, default='', help_text='Notizen für Administration. Nicht sichtbar für Mitglied', max_length=1000, verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Aktiv'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='future_depot',
            field=models.ForeignKey(blank=True, help_text='Nur setzen, wenn Depot geändert werden soll', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='future_subscription_set', to='juntagrico.Depot', verbose_name='Zukünftiges Depot'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='notes',
            field=models.TextField(blank=True, help_text='Notizen für Administration. Nicht sichtbar für Mitglied', max_length=1000, verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='primary_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subscription_primary', to='juntagrico.Member', verbose_name='Haupt-Abo-BezieherIn'),
        ),
        migrations.AlterField(
            model_name='subscriptionsize',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sizes', to='juntagrico.SubscriptionProduct', verbose_name='Produkt'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='types', to='juntagrico.SubscriptionSize', verbose_name='Grösse'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='trial',
            field=models.BooleanField(default=False, verbose_name='Probe-Abo'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='trial_days',
            field=models.IntegerField(default=0, verbose_name='Probe-Abo Dauer in Tagen'),
        ),
        migrations.AlterField(
            model_name='tfsst',
            name='type',
            field=models.ForeignKey(help_text='Muss gleich eingestellt sein wie Abo-Typen oben, wenn keine Änderung ansteht', on_delete=django.db.models.deletion.PROTECT, related_name='TTFSST', to='juntagrico.SubscriptionType'),
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='duration',
            new_name='default_duration',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='duration',
            new_name='default_duration',
        ),
    ]
