from __future__ import absolute_import, unicode_literals
from secret.models import Secret
from celery import shared_task
from .models import Secret


@shared_task
def kill_secret():
    try:
        objects = Secret.objects.all()
        for obj in objects:
            if obj.time_to_live > 0:
                obj.time_to_live -= 1
            elif obj.time_to_live == 0:
                obj.delete()
            obj.save()
    except Exception as e:
        print(e)
