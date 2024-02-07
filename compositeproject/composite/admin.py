from django.contrib import admin
from .models import Item, Composite, Comp_List, Previous_List

admin.site.register(Item)
admin.site.register(Composite)
admin.site.register(Comp_List)
admin.site.register(Previous_List)