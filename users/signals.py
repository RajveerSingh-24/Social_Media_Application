from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Follow, User


# =========================
# FOLLOW CREATED
# =========================
@receiver(post_save, sender=Follow)
def increase_follow_counts(sender, instance, created, **kwargs):
    if created:
        User.objects.filter(id=instance.follower.id).update(
            following_count=F('following_count') + 1
        )

        User.objects.filter(id=instance.following.id).update(
            followers_count=F('followers_count') + 1
        )


# =========================
# FOLLOW REMOVED
# =========================
@receiver(post_delete, sender=Follow)
def decrease_follow_counts(sender, instance, **kwargs):
    User.objects.filter(id=instance.follower.id).update(
        following_count=F('following_count') - 1
    )

    User.objects.filter(id=instance.following.id).update(
        followers_count=F('followers_count') - 1
    )
