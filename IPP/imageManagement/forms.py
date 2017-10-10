from django import forms
from django.forms import BaseFormSet,formset_factory
from multiupload.fields import MultiImageField
from .models import Topic, ImageControll
import datetime

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topicName','note']
    images = MultiImageField()
    def save(self, commit=True):
        self.trainTimes = 0
        topic = super(TopicForm, self).save(commit)
        for each in self.cleaned_data['images']:
            image = each
            imageControll = ImageControll()
            imageControll.createTime = datetime.datetime.now()
            imageControll.topic = topic
            imageControll.imageFile = image
            imageControll.imageFileName = image.name
            imageControll.imageFormat = image.name[image.name.index('.'):]
            imageControll.imageHeight = imageControll.imageFile.height
            imageControll.imageWidth = imageControll.imageFile.width
            imageControll.imageSize = imageControll.imageFile.size
            imageControll.note = ''
            imageControll.save()
        return topic