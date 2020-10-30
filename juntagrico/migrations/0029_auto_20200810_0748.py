# Generated by Django 3.0.8 on 2020-08-10 05:48
from datetime import timedelta

from django.db import migrations, transaction
from django.utils import timezone


def migrate_memberships(apps, schema_editor):
    Member = apps.get_model('juntagrico', 'Member')
    SubscriptionMembership = apps.get_model('juntagrico', 'SubscriptionMembership')
    for member in Member.objects.all():
        if member.future_subscription is not None:
            try:
                with transaction.atomic():
                    SubscriptionMembership.objects.create(member=member,
                                                          subscription=member.future_subscription,
                                                          join_date=member.future_subscription.creation_date)
            except Exception:
                pass
        if member.subscription is not None:
            try:
                with transaction.atomic():
                    SubscriptionMembership.objects.create(member=member,
                                                          subscription=member.subscription,
                                                          join_date=member.subscription.creation_date)
            except Exception:
                pass
        yesterday = timezone.now().date() - timedelta(days=1)
        print(yesterday)
        for sub in member.old_subscriptions.all():
            try:
                with transaction.atomic():
                    SubscriptionMembership.objects.create(member=member,
                                                          subscription=sub,
                                                          join_date=sub.creation_date,
                                                          leave_date=sub.deactivation_date or yesterday)
            except Exception:
                pass


class Migration(migrations.Migration):
    dependencies = [
        ('juntagrico', '0028_subscriptionmembership'),
    ]

    operations = [
        migrations.RunPython(migrate_memberships),
    ]
