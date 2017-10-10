"""IPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from imageManagement.views import topic_AddOrSelectTopic,upLoadTrainingImagePage,uploadify_script,topic_GetTopicJsonData,\
    image_GetImageJsonData,topic_modifyTheTopic,__testThePage,topic_deleteTheTopic,topic_addTopicWithoutRedirect,image_modifyImage,image_deleteImage,image_getTestingImage,upLoadTestingImagePage,image_getImageFromGoogleSearch,index,testing,poll_state,training, info

urlpatterns = [
    url(r'^$',index, name = 'home'),
    url(r'^info/',info, name = 'info'),

    url(r'^admin/', admin.site.urls),

    url(r'^topic/$',topic_AddOrSelectTopic, name = 'topic'),
    url(r'^uploadTrainingImages/(\d+)/$', upLoadTrainingImagePage),
    url(r'^upLoadTestingImage/$',upLoadTestingImagePage, name = "upload_test"),
    # Original 
    url(r'^upload-testing-to-server',image_getTestingImage),
    url(r'^upload-to-server/$',uploadify_script),
    url(r'^getTopicJsonData/$',topic_GetTopicJsonData),
    url(r'^getImageJsonData/(\d+)/$$', image_GetImageJsonData),
    url(r'^modify-topic/$', topic_modifyTheTopic),
    url(r'^delete-topic/$',topic_deleteTheTopic),
    url(r'^add-topic-without-image/$',topic_addTopicWithoutRedirect),
    url(r'^modify-image/$',image_modifyImage),
    url(r'^get-testing-image-from-goolesearch',image_getImageFromGoogleSearch),
    url(r'^delete-image/$',image_deleteImage),
    url(r'^test/$',__testThePage),

    url(r'^testing/$',testing, name = 'test'),
    url(r'^training/',include('imageManagement.urls')),
    url(r'^poll_state$', poll_state),



]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
