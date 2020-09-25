import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

import django

django.setup()
from django.contrib.auth.models import Group


GROUPS = ['admin', 'anonymous']
MODELS = ['user']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)
