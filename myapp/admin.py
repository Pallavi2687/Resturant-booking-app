from django.contrib import admin

# Register your models here.
from myapp.models import *
# Register your models here.

admin.site.register(ItemList)
admin.site.register(Items)
admin.site.register(AboutUs)
admin.site.register(Feedback)
admin.site.register(BookTable)