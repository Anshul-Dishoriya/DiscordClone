from .models import Topic
from pprint import pprint

def get_topics(request , context ,topics=None):
    all_topics = topics if topics else Topic.objects.all()[:7]

    topics = {}
    for tpc in all_topics:
        topics[tpc.id] = {'name':tpc ,'is_subscribed':False}
        
        if request.user.is_authenticated and tpc.subscribe.filter(id=request.user.id):
            topics[tpc.id]['is_subscribed'] = True

    context['topics']=topics




def get_messages(request , context ,messages=None):
    room_messages = {}
    for msg in messages:
        room_messages[msg.id] = {'data':msg , 'isLiked':False} 

        if request.user.is_authenticated and msg.likes.filter(id=request.user.id):
            room_messages[msg.id]['isLiked'] = True
    context['room_messages']= room_messages
