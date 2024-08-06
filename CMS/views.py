from rest_framework import viewsets
from service.serializer import NoticeSerializer
from service.models import Notice


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    # def delete (self, request):
    #     Notice.objects.all().delete()
    #     retsn