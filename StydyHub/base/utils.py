from .models import Topic
from pprint import pprint

def get_topics(request , context):
    all_topics = Topic.objects.all()

    topics = {}
    for tpc in all_topics:
        topics[tpc.id] = {'name':tpc ,'is_subscribed':False}
        if request.user.is_authenticated and tpc.subscribe.filter(id=request.user.id):
            topics[tpc.id]['is_subscribed'] = True
    print(topics)

    context['topics']=topics



    
