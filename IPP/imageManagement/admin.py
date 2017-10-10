from django.contrib import admin

# Register your models here.
from .models import ImageControll,Topic

class ImageControllAdmin(admin.ModelAdmin):
    list_display = ('imageFileName','imageFile','imageFormat','imageSize','imageHeight','imageWidth','createTime','note')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('topicName','trainTimes','lastUpdateTime','createTime','note')

admin.site.register(ImageControll,ImageControllAdmin)
admin.site.register(Topic,TopicAdmin)