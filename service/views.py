from django.shortcuts import render, redirect
from .serializer import  NoticeSerializer
from rest_framework import status
from django.contrib.auth.models import update_last_login
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Notice
from rest_framework.pagination import PageNumberPagination
from service.serializer import LoginSerializer
from rest_framework.views import APIView
from django.views import View
from service.forms import AdminForm
from django.http import HttpResponse



def index(request):
    return render(request, 'index.html')

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
        
#         if user is not None:
#             auth_login(request, user)
#             return redirect('index')  # Redirect to the index or another page
#         else:
#             messages.error(request, 'Invalid credentials')
    
#     return render(request, 'login.html')

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'detail': 'Form validation failed'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_notice': '/',
        'Add': '/Create',
        'Update': '/Update/pk',
        'Delete': '/Delete/pk',
        'All list':'/NoticeList',
        'View by title': '/view/?title=title name'
    }

    return Response(api_urls)


def custom_logout(request):
    logout(request)
    messages.success(request,("successfully logged out"))
    return redirect('api/v1/login')




@api_view(['GET'])
def NoticeList(request, pk):
    notice = Notice.objects.get(id = pk)
    serializer = NoticeSerializer(notice, many=False)
    return Response(serializer.data)


@api_view(['Post'])
def AddNotice(request):
    # import pdb
    # pdb.set_trace()
    # parser_class = [MultiPartParser, FormParser]
    serializer = NoticeSerializer(data=request.data)
     
    # if serializer.objects.filer(**request.data).exists():
    #     raise serializers.ValidationError('This Notice already exits')
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,  status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def UpdateNotice(request, pk):
    # import pdb
    # pdb.set_trace()
    notice = Notice.objects.get(id = pk)
    serializer = NoticeSerializer(instance= notice, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def NoticeDelete(request, pk):
    # import pdb
    # pdb.set_trace()
    notice = Notice.objects.get(id = pk)
    notice.delete()
 
    return Response("Notice deleted successfully !!!")

@api_view(['GET'])
def NoticeList(request):
    if request.query_params:
        notice = Notice.objects.filter(*request.query_params.dict())
    else:
        notice = Notice.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    result_page = paginator.paginate_queryset(notice, request)
    serializer = NoticeSerializer(result_page, many = True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def view_items(request):
    if request.query_params:
        items = Notice.objects.filter(**request.query_params.dict())
    else:
        items = Notice.objects.all()
 
    if items:
        serializer = NoticeSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class AddUser(View):
    def get(self, request):
        if request.user.is_superuser:
            form = AdminForm()
            context = {'form': form}
            return render(request, 'login.html', context)
        else:
            return HttpResponse("Opps you are not the admin, Please log is as Admin from <a href='http://127.0.0.1:8000/admin/'>here</a>")
        
    def post(self, request):
        if request.user.is_superuser:
            form = AdminForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse("Successfully added") 
            else:
                context = {'form': form}
                return render(request, 'login.html', context)
        else:
            return HttpResponse("You do not have access to perform this action!")
