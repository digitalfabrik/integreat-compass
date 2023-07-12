"""
Debug lists and forms for all models
"""
from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model

if settings.DEBUG:
    admin.site.register(apps.get_model("auth", "Permission"))
    for model in apps.get_app_config("cms").get_models():
        admin.site.register(model)
    for model in apps.get_app_config("admin").get_models():
        admin.site.register(model)
    for model in apps.get_app_config("contenttypes").get_models():
        admin.site.register(model)
    for model in apps.get_app_config("sessions").get_models():
        admin.site.register(model)
else:
    admin.site.register(get_user_model())
