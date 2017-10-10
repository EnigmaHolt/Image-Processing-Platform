from django.db import models
from django.core.files import File
import urllib
import os

def setImageSaveLocation(instance,filename):
    return instance.imageUrl
class Topic(models.Model):
    topicName = models.CharField('Topic Name',max_length=30,null=False)
    createTime = models.DateTimeField('Topic Create Time',auto_now_add=True,editable=True)
    trainTimes = models.PositiveIntegerField('Training Time',default=0)
    lastUpdateTime = models.DateTimeField('Topic Last Update Time',auto_now=True,null=True, editable=True)
    note = models.CharField('Note',max_length=100,null=True)
    def __str__(self):
        return self.topicName
# Create your models here.
class ImageControll(models.Model):
    imageFileName = models.CharField('Image File Name',max_length=50,null=False)
    createTime = models.DateTimeField('Image Create Time',auto_now_add=True ,editable=True)
    topic=models.ForeignKey('Topic',blank=True,null=True)
    imageUrl = models.CharField(max_length=255)
    imageFile = models.ImageField(upload_to=setImageSaveLocation,blank=True)
    imageFormat = models.CharField('Image Format',max_length=10,null = False)
    imageSize = models.PositiveIntegerField('Image Size')
    imageHeight = models.PositiveIntegerField('Image Height')
    imageWidth = models.PositiveIntegerField('Image Width')
    note = models.CharField('Note',max_length=100,null = True)
    #1 training image 2. testing image
    isTraining = models.PositiveIntegerField('image Type')

    def __str__(self):
        return self.imageFileName

    def cache(self):
        if self.imageUrl and not self.imageFile:
            self.imageFile.save(os.path.basename(self.imageUrl))
            self.save()

class ModelObject(models.Model):
    modelName = models.CharField('Model Name',max_length=100,null=False)
    modelRoute = models.CharField('Model Route',max_length=1000,null= False)
    modelTextRoute = models.CharField('Model Text Route',max_length=1000,null  = True)
    modelType = models.CharField('Model type',max_length=1000,default ='retrain',null = True)
    modelNote = models.CharField('Model Node',max_length=1000,null = True)
class Model_Topic(models.Model):
    model = models.ForeignKey('ModelObject',null=False)
    topic = models.ForeignKey('Topic',null=False)
class work_queue(models.Model):
    workID = models.CharField('Work ID', max_length=100, null=False)
    workStatus = models.CharField('Work Status',max_length=100,null=False)
    workBeginTime = models.DateTimeField('Work Begin Time',auto_now_add=True ,editable=True)
