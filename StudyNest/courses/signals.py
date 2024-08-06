from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Course

@receiver(post_save, sender=Course)
def update_course_count_on_save(sender, instance, created, **kwargs):
    if created:
        instance.category.course_count += 1
        instance.category.save()

@receiver(post_delete, sender=Course)
def update_course_count_on_delete(sender, instance, **kwargs):
    instance.category.course_count -= 1
    instance.category.save()