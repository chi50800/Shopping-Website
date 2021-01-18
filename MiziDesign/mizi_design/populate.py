import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mizi_design.settings')

import django
django.setup()

import random
from mizi_app.models import User
from faker import Faker

fakegen=Faker()

def populate(N=5):

    for entry in range(N):
        fake_name=fakegen.name()
        fake_email=fakegen.email()
        userpg=User.objects.get_or_create(name=fake_name,email=fake_email)

print('script')
populate(10)
print('populated')
