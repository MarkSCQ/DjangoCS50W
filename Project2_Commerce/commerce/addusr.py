from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import datetime
import os
import django

script_path = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auctions.settings")
django.setup()


date_time = datetime.datetime.now()

users = []

employee_number_list = [
    ['1', '2'],
    ['3', '4'],
    ['5', '6'],
    ['7', '8'],
    ['9', '10']
]

User.objects.bulk_create([
    User(
        username=each[0],
        email=each[1],
        password=make_password('common_password'),
        is_staff=True,
    ) for each in employee_number_list
])
