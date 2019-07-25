from django.contrib import admin
from .models import Paper, PaperWithRefs

# Register your models here.
admin.site.register([Paper, PaperWithRefs])
