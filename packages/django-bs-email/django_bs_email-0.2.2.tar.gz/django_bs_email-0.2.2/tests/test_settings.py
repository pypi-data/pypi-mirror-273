DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "bootstrap_email.db",
    }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
    },
]

INSTALLED_APPS = [
    "django_bootstrap_email",
]
