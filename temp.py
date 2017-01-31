import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PropertyScraper_Web.settings")
django.setup()


from Trustee import models
import constants


properties = models.PropertyRecord.objects.all()
for property in properties:
    print(property.id)
    property.save()
