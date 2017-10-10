import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IPP.settings")
import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()
 
 
def main():
    from imageManagement.models import Topic
    f = open('raw_topic_data.txt')
    for topic in f:
        Topic.objects.create(topicName=topic)
    f.close()
 
if __name__ == "__main__":
    main()
    print('Done!')