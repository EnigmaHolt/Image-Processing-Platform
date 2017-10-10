# Import 
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse,JsonResponse
from .models import ImageControll,Topic,ModelObject,Model_Topic,work_queue
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db.models import Q
import datetime
import time
from celery import app
from django.utils.timezone import now
import requests
import os
import shutil
import json

import imageManagement.inception.retrain as retrain
import imageManagement.inception.classify_image as classify
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):

    return render(request,'index.html')

def info(request):
    list_model = []
    if ModelObject.objects.all().exists():
        model_list = ModelObject.objects.all()
        list_model.append(model_list[0].modelName)
        if len(model_list)> 1:
            list_model.append(model_list[len(model_list)-1].modelName)
    return render(request,'info.html',{'model_list':list_model})

@csrf_exempt
def topic_AddOrSelectTopic(request):
    if request.method == 'POST':
        topicName = request.POST['new_topic_name']
        topicNote = request.POST['new_topic_note']
        if Topic.objects.filter(topicName=topicName).exists():
            topic = Topic.objects.get(topicName=topicName)
        else:
            topic = Topic()
            topic.topicName = topicName
            topic.note = topicNote
            topic.save()
        return redirect('/uploadTrainingImages/{}'.format(topic.id))
    else:
        searchText = request.GET.get('searchText')
        if searchText:
            current_topics = Topic.objects.filter(Q(topicName=searchText)|Q(note=searchText))
        else:
            current_topics = Topic.objects.all()
        rows =[{
            'id':topic.id,
            'topicName': topic.topicName,
            'trainTimes':topic.trainTimes,
            'createTime':topic.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            'note':_changeNoneToString(topic.note),
            'lastUpdateTime':topic.lastUpdateTime.strftime("%Y-%m-%d %H:%M:%S")
        } for topic in current_topics]
        return render(request, 'add_or_select_training_topic.html', {"data":json.dumps(rows)})
@csrf_exempt
def topic_addTopicWithoutRedirect(request):
    if request.method == 'POST':
        topicName = request.POST['topic_name']
        topicNote = request.POST['topic_note']
        if Topic.objects.filter(topicName=topicName).exists():
            return HttpResponse('error')
        else:
            topic = Topic()
            topic.topicName = topicName
            topic.note = topicNote
            topic.save()
            return HttpResponse('success')

@csrf_exempt
def topic_deleteTheTopic(request):
    if request.method=='POST':
        topic_list = request.POST['topic_list']
        topic_json = json.loads(topic_list)
        for topic in  topic_json:
            topicId=topic['id']
            topic_object = Topic.objects.get(id=topicId)
            topic_object.delete()
        return HttpResponse('success')

@csrf_exempt
def topic_modifyTheTopic(request):
    if request.method=='POST':
        row_name = request.POST['object']
        topic_data = request.POST['strJson']
        topic_json = json.loads(topic_data)
        if row_name =='topicName':
            if topic_json['topicName']=='':
                return HttpResponse('empty')
            elif not Topic.objects.filter(topicName=topic_json['topicName']).exists():
                topicId = topic_json['id']
                topic = Topic.objects.get(id = topicId)
                topic.topicName = topic_json['topicName']
                topic.note = topic_json['note']
                topic.save()
                return HttpResponse('success')
            else:
                return HttpResponse('error')
        elif row_name == 'note':
            topicId = topic_json['id']
            topic = Topic.objects.get(id=topicId)
            topic.topicName = topic_json['topicName']
            topic.note = topic_json['note']
            topic.save()
            return HttpResponse('success')
def topic_GetTopicJsonData(request):
    current_topics = Topic.objects.all()
    rows = [{
                'id': topic.id,
                'topicName': topic.topicName,
                'trainTimes': topic.trainTimes,
                'createTime': topic.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                'note': _changeNoneToString(topic.note),
                'lastUpdateTime': topic.lastUpdateTime.strftime("%Y-%m-%d %H:%M:%S"),
            } for topic in current_topics]
    data = {
        'total': len(current_topics),
        'rows': rows
    }
    return JsonResponse(data)
def image_GetImageJsonData(request,topicId):
    if topicId=='0':
        images_object = ImageControll.objects.filter(isTraining=2 )
    else:
        images_object = ImageControll.objects.filter(topic=Topic.objects.get(id=topicId))

    rows = [{
                    'id':image.id,
                    'imageFileName': image.imageFileName,
                    'imageFormat': image.imageFormat,
                    'imageSize': image.imageSize,
                    'url':image.imageUrl[image.imageUrl.find('photos')+6:],
                    'createTime': image.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                    'note': _changeNoneToString(image.note)
                } for image in images_object]
    data = {
        'total': len(images_object),
        'rows': rows
    }
    return JsonResponse(data)
@csrf_exempt
def image_deleteImage(request):
    if request.method=='POST':
        image_list = request.POST['image_list']
        image_json = json.loads(image_list)
        for image in  image_json:
            imageId=image['id']
            image_object = ImageControll.objects.get(id=imageId)
            image_object.imageFile.delete()
            image_object.delete()
        return HttpResponse('success')
@csrf_exempt
def image_modifyImage(request):
    if request.method == 'POST':
        row_name = request.POST['object']
        image_data = request.POST['strJson']
        image_json = json.loads(image_data)
        if row_name =='imageFileName':
            if image_json['imageFileName']=='':
                return HttpResponse('empty')
            elif not ImageControll.objects.filter(imageFileName=image_json['imageFileName']).exists():
                imageId = image_json['id']
                image = ImageControll.objects.get(id = imageId)
                image.imageFileName = image_json['imageFileName']
                image.save()
                return HttpResponse('success')
            else:
                return HttpResponse('error')
        elif row_name == 'note':
            imageId = image_json['id']
            image = ImageControll.objects.get(id=imageId)
            image.note = image_json['note']
            image.save()
            return HttpResponse('success')
def upLoadTrainingImagePage(request,topicId):
    topicId = topicId
    return render(request,'upload_the_training_image.html',{"topicId":topicId})
@csrf_exempt
def upLoadTestingImagePage(request):
    #delete All the file in Testing Image Folder
    user_upload_folder = os.path.join(settings.MEDIA_ROOT + '/TESTING_IMAGE')
    if not os.path.exists(user_upload_folder):
        os.makedirs(user_upload_folder)
        os.chmod(user_upload_folder, 0o777)
    ImageControll.objects.filter(isTraining=2).delete()
    shutil.rmtree(user_upload_folder)
    list_model = []
    if ModelObject.objects.all().exists():
        model_list = ModelObject.objects.all()
        list_model.append(model_list[0].modelName)
        if len(model_list)> 1:
            list_model.append(model_list[len(model_list)-1].modelName)
    return render(request, 'upload_the_testing_image.html', {"model_list":list_model})

@csrf_exempt
def uploadify_script(request):
    id = int(request.POST['topicID'])
    topic = Topic.objects.get(id=id)
    imageUrl,imageName,imageFormat = upload_image(request,topic.topicName)
    imageControll = ImageControll()
    imageControll.createTime = datetime.datetime.now()
    imageControll.topic = topic
    imageControll.imageUrl =imageUrl
    imageControll.isTraining = 1
    imageControll.imageFile.save(imageUrl,request.FILES['Filedata'],save=False)
    imageControll.imageFileName = imageName
    imageControll.imageFormat =imageFormat
    imageControll.imageHeight = imageControll.imageFile.height
    imageControll.imageWidth = imageControll.imageFile.width
    imageControll.imageSize = imageControll.imageFile.size
    imageControll.note = ''
    imageControll.save()
    return render(request,'show_the_saving_result.html',{'save':'true'})
@csrf_exempt
def image_getTestingImage(request):
    file_ext = str(request.FILES['Filedata'].name).split('.')[-1]
    file_name = time.strftime('%Y%m%d%H%M%S') + str(datetime.datetime.now().microsecond)+'.'+file_ext
    user_upload_folder = os.path.join(settings.MEDIA_ROOT + '/TESTING_IMAGE/')
    #   shutil.rmtree(user_upload_folder)
    if not os.path.exists(user_upload_folder):
        os.makedirs(user_upload_folder)
        os.chmod(user_upload_folder, 0o777)

    # file_url = os.path.join(user_upload_folder, file_name + '.' + file_ext)
    # file_upload = open(file_url, 'wb')
    # file_upload.write(request.FILES['Filedata'].read())
    # file_upload.close()

    #
    # test image
    imageControll = ImageControll()
    imageControll.createTime = datetime.datetime.now()
    imageControll.topic = None
    imageControll.imageUrl =user_upload_folder+file_name
    imageControll.isTraining = 2
    imageControll.imageFile.save(user_upload_folder,request.FILES['Filedata'],save=False)
    imageControll.imageFileName = file_name
    imageControll.imageFormat =file_ext
    imageControll.imageHeight = imageControll.imageFile.height
    imageControll.imageWidth = imageControll.imageFile.width
    imageControll.imageSize = imageControll.imageFile.size
    imageControll.note = ''
    imageControll.save()


    return redirect('/topic')
@csrf_exempt
def image_getImageFromGoogleSearch(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        url = "https://www.googleapis.com/customsearch/v1?q="+topic+"&cx=011694950429578715460%3Afvggocgzvsw&key= AIzaSyB-XWLmQ7QhmDhElq5MxuiuiF3VQ5-amoQ&fields=items(pagemap/cse_image/src)&num=10"
        request = requests.get(url)
        raw_data = str(request.text)
        json_data = json.loads(raw_data)
        # imageUrl_list= [{
        #     'url': item['pagemap']['cse_image'][0]['src']
        #                 } for item in json_data['items']]
        # data = {
        #     'urllist':imageUrl_list
        # }
        image_list = []
        for item in json_data['items']:
            image_list.append( item['pagemap']['cse_image'][0]['src'])

        return HttpResponse(json.dumps(image_list))

def upload_image(request,topic_name):
    file_ext = str(request.FILES['Filedata'].name).split('.')[-1]
    file_name = time.strftime('%Y%m%d%H%M%S')+str(datetime.datetime.now().microsecond)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    user_upload_folder = os.path.join(settings.MEDIA_ROOT+'/photos', topic_name.strip('\n'))
    if not os.path.exists(user_upload_folder):
         os.makedirs(user_upload_folder)
         os.chmod(user_upload_folder, 0o777)
    file_url = os.path.join(user_upload_folder, file_name + '.' + file_ext)
    #file_upload = open(file_url, 'wb')
    #file_upload.write(request.FILES['Filedata'].read())
    #file_upload.close()
    return file_url,file_name+'.'+file_ext,file_ext

def _changeNoneToString(string):
    if string == None:
        return 'null'
    else:
        return string
def __testThePage(request):
    return render(request,'add_or_select_training_topic.html')

@csrf_exempt
def testing(request):
    if request.method == 'POST':
        test_model = request.POST['model']
        model_pb = ModelObject.objects.get(modelName=test_model).modelRoute
        model_txt = ModelObject.objects.get(modelName=test_model).modelTextRoute
        test_raw_image_list = ImageControll.objects.filter(isTraining=2)
        test_image_url_list = []
        result_list = []

        for item in test_raw_image_list:
            test_image_url_list.append([item.imageUrl,item.imageFileName,item.imageSize])

        for image in test_image_url_list:
            context = {
                'url': image[0],
                #'model' : os.path.join(settings.MODEL_ROOT + '/output_graph.pb'),
                #'map' : os.path.join(settings.MODEL_ROOT + '/output_labels.txt'),
                'model':model_pb,
                'map':model_txt,
            }

            result = classify.classify_image(context)
     
            data = {
                'url' : '../photo/' + context['url'][context['url'].index('TESTING_IMAGE'):],
                'imageName':image[1],
                'imageSize':image[2],
                'result' : result,
            }
            result_list.append(data)
        if(len(result_list) == 0):
            return render(request, 'show_testing_result.html', {'re' : result_list, 'size' : 0})
        else: 
            return render(request, 'show_testing_result.html', {'re' : result_list})
    else:
        return render(request, 'testing.html')

@csrf_exempt
def training(request):
    description = ''
    if work_queue.objects.all().exists():
        job_id = work_queue.objects.all()[0].workID
    else:
            if request.method == 'POST':
                description = request.POST['description']
                model_option = request.POST['model_option']
                if model_option == 'Debug Mode (Iteration: 1)':
                    training_step = 1
                elif model_option =='Speed Priority Training Mode (Iteration: 300)':
                    training_step = 300
                elif model_option == 'Speed-Accuracy Balance Mode (Iteration: 600)':
                    training_step = 600
                elif model_option == 'Accuracy Priority Mode (Iteration: 1200)':
                    training_step = 1200
                job_id = retrain.connect.delay().id
                work = work_queue()
                work.workID = job_id
                work.workStatus = 'processing'
                work.save()
    job = AsyncResult(job_id)
    data = job.result or job.state
    context = {
        'data':data,
        'task_id':job_id,
        'descriptions':description
    }

    return render(request,"show_training_status.html",context)


@csrf_exempt
def poll_state(request):
    """ A view to report the progress to the user """
    if request.method == 'POST':
        if 'task_id' in request.POST.keys():
            task_id = request.POST['task_id']
            description = request.POST['descriptions']
            task = AsyncResult(task_id)
            print("Stats: "+task.state)
            if task.state != "SUCCESS" and task.state != "PENDING" and task.state!='FAILURE':
                if task.result:
                    data = task.result
                    data['type'] = 'processing'
                else:
                    data ={}
                    data['type'] = 'failure'
            elif task.state =='FAILURE':
                if task.result:
                    data = task.result
                else:
                    data = {}
                data['type'] = 'failure'
                work_queue.objects.all().delete()
            elif task.state == 'PENDING':
                data = {}
                data['type'] = 'pending'
            elif task.status=='SUCCESS':

                work_queue.objects.all().delete()

                data = {}
                data_result = task.result
                model_name = data_result[1][data_result[1].index('output_graph'):len(data_result[1]) - 3]
                mode_txt_url = data_result[0]
                mode_graph_url = data_result[1]
                if not ModelObject.objects.filter(modelName=model_name).exists():
                    model = ModelObject()
                    model.modelName = model_name
                    model.modelRoute = mode_graph_url
                    model.modelTextRoute = mode_txt_url
                    model.modelNote = description
                    model.save()
                    data['type']='done'
                    # topics = Topic.objects.all()
                    # for topic in topics:
                    #     topic.trainTimes += 1
                    #     topic.lastUpdateTime =now
                    #     topic.save()
                    #     mt = Model_Topic()
                    #     mt.model = model
                    #     mt.topic = topic
                    #     mt.save()
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
