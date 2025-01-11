from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import MessageSerializer
from ..courses.models import Course
from ..instructor.models import Author
from ..payments.models import Enrollment


def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = User.objects.get(id=id)
        # if user act as student
        # Retrieve all courses related to this user through enrollments
        courses = Course.objects.filter(enrollment__user=user).distinct()
        friends = []
        if courses:
            for id in courses:
                num = str(id.author.id)
                fr = User.objects.get(id=int(num))
                friends.append(fr)
        else:
            # if user act as author
            # Retrieve all authors related to this user through enrollments
            authors = Enrollment.objects.filter(course__author__user=user).distinct()
            for id in authors:
                num = str(id.user.id)
                fr = User.objects.get(id=int(num))
                friends.append(fr)
        return friends
    except Exception as e:
        print("Error", e)
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = User.objects.get(username=username)
    id = use.id
    return id


def index(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        return render(request, "chat/Base.html", {'friends': friends})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.user.username
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("/search")


def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = User.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = User.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(
        sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
