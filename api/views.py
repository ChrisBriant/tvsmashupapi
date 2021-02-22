from django.shortcuts import render
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import RefreshToken
from tvsmashup.permissions import is_authorised
from tvsmashup.settings import BASE_URL
from .serializers import *
from tv.models import *
from difflib import SequenceMatcher
# from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from tvsmashup.email import sendjoiningconfirmation, sendpasswordresetemail
import random



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



@api_view(['POST','OPTIONS'])
def get_token(request):
    if request.method == "POST":
        try:
            email = request.data["email"]
            password = request.data["password"]
            user = authenticate(username=email,password=password)
            if user:
                if user.is_enabled:
                    #Issue token
                    token = get_tokens_for_user(user)
                    return Response(token, status=status.HTTP_200_OK)
                else:
                    print("Account Disabled")
                    return Response(ResponseSerializer(GeneralResponse(False,"User is not enabled")).data, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Credentials Failed")
                return Response(ResponseSerializer(GeneralResponse(False,"User name or password are incorrect")).data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(ResponseSerializer(GeneralResponse(False,"Unable to retrieve token")).data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    password = request.data['password']
    passchk = request.data['passchk']
    username = request.data['username']
    email = request.data['email']

    # Create a schema
    schema = PasswordValidator()
    schema\
    .min(8)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()\

    if password != passchk or not schema.validate(password):
        return Response(ResponseSerializer(GeneralResponse(False,'Password does not meet the complexity requirements.')).data, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = Account.objects.create_user (email,username,password)
        #Get joining confirmation information over to user
        user.hash = hex(random.getrandbits(128))
        user.save()
        url = BASE_URL + "confirm/" + user.hash + "/"
        sendjoiningconfirmation(url,user.name,user.email)
        return Response(ResponseSerializer(GeneralResponse(True,'Account Created')).data, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        print(type(e).__name__)
        return Response(ResponseSerializer(GeneralResponse(False,'Email already exists with us, please try a different one or send a forgot password request')).data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(ResponseSerializer(GeneralResponse(False,'Problem creating account')).data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forgot_password(request):
    email = request.data['email']
    try:
        user = Account.objects.get(email=email)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,'Email address not found, please register a new account.')).data, status=status.HTTP_400_BAD_REQUEST)
    user.hash = hex(random.getrandbits(128))
    user.save()
    url = BASE_URL + "passwordresetapi/" + user.hash + "/"
    sendpasswordresetemail(url,user.name,user.email)
    return Response(ResponseSerializer(GeneralResponse(True,'Please check your email and click on the link to reset your password')).data, status=status.HTTP_200_OK)


# # Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_tvshow(request):
    # TODO: Look into logic, if no image, etc. do we enforce image upload?
    name = request.data.get('name')
    tvshow, success = TVShow.objects.get_or_create(
        user = request.user,
        name = name
    )
    picture = request.data.get('picture',None)
    if picture and success:
        picture = picture
        try:
            pic = TVImage(
                show = tvshow,
                picture=picture
            )
            pic.full_clean()
            pic.save()
        except Exception as e:
            print("File upload failed", e)
            return Response(ResponseSerializer(GeneralResponse(False,"Invalid File")).data, status=status.HTTP_400_BAD_REQUEST)
    elif picture and not success:
        #Update picture instead of create new one
        try:
            pic = TVImage.objects.get(show_id=tvshow.id)
            pic.picture = picture
            pic.full_clean()
            pic.save()
        except Exception as e:
            print("File upload failed", e)
            return Response(ResponseSerializer(GeneralResponse(False,"Invalid File")).data, status=status.HTTP_400_BAD_REQUEST)
    serializer = TVShowSerializer(tvshow)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_smashup(request):
    show1 = request.data.get('show1')
    show2 = request.data.get('show2')
    categories = request.data.get('categories')
    try:
        show1 = TVShow.objects.get(id=request.data.get('show1'))
        show2 = TVShow.objects.get(id=request.data.get('show2'))
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"At least one of the shows doesn't exist")).data, status=status.HTTP_400_BAD_REQUEST)
    try:
        smashup = SmashUp(
            creator = request.user,
            show_1 = show1,
            show_2 = show2
        )
        smashup.clean()
        smashup.save()
        #Create the categories
        for cat in categories:
            category, created = Category.objects.get_or_create(
                user = request.user,
                category = cat
            )
            CategorySmashup.objects.create(
                smashup = smashup,
                category = category
            )
        serializer = TVSmashupSerializer(smashup)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Unable to create smashup, a smashup probably alredy exists for these shows.")).data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def all_smashups(request):
    smashups = SmashUp.objects.all().order_by('-date_added')
    serializer = TVSmashupSerializer(smashups,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def get_smashup(request):
    try:
        smashup = SmashUp.objects.get(id=request.query_params['id'])
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Smashup doesn't exist")).data, status=status.HTTP_400_BAD_REQUEST)
    serializer = TVSmashupSerializer(smashup)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_smashups(request):
    smashups = SmashUp.objects.filter(creator=request.user)
    serializer = TVSmashupSerializer(smashups,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_tvshows(request):
    shows = TVShow.objects.filter(user=request.user)
    serializer = TVShowSerializer(shows,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def search_tvshows(request):
    searchstr = request.query_params['search']
    shows = TVShow.objects.filter(name__icontains=searchstr)
    serializer = TVShowSerializer(shows,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
def add_rating(request):
    rating = request.data.get('rating')
    catsmashupid = request.data.get('id')
    if request.user.id == None:
        user = None
    else:
        user = request.user
    if rating in range(1,6):
        try:
            rating = CategoryScore.objects.create(
                user = user,
                rating = rating,
                categorysmashup = CategorySmashup.objects.get(id=catsmashupid)
            )
        except IntegrityError as e:
            print(e)
            return Response(ResponseSerializer(GeneralResponse(False,"You have already addded a rating for this category.")).data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(ResponseSerializer(GeneralResponse(False,"Unable to add rating.")).data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"Rating must be a number between 1 and 5")).data, status=status.HTTP_400_BAD_REQUEST)
    serializer = RatingSerializer(rating)
    return Response(serializer.data,status=status.HTTP_200_OK)




#
# # Create your views here.
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def addround(request):
#     try:
#         #Get the quiz
#         quiz = Quiz.objects.get(id=request.data['quiz_id'])
#     except Exception as e:
#         return Response(ResponseSerializer(GeneralResponse(False,e)).data, status=status.HTTP_400_BAD_REQUEST)
#
#     roundserializer = RoundSerializer(data=request.data['round'],context={'user':request.user,'quiz':quiz})
#     try:
#         if roundserializer.is_valid():
#             round = roundserializer.save()
#         else:
#             print("Not Valid")
#             print(roundserializer.errors)
#             template = "Field {0} failed because {1}\n"
#             errs = [template.format(e,roundserializer.errors[e][0]) for e in roundserializer.errors.keys()]
#             return Response(ResponseSerializer(GeneralResponse(False,'Validation failed\n'+'\n'.join(errs))).data, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         print('failed',e)
#         return Response(ResponseSerializer(GeneralResponse(False,e)).data, status=status.HTTP_400_BAD_REQUEST)
#     round_data = StoredRoundSerializer(round).data
#     return Response(round_data, status=status.HTTP_201_CREATED)
