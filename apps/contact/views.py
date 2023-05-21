from rest_framework import generics
from apps.contact.models import GetInTouch
from .serializers import GetInTouchSerializer


class GetInTouchCreateAPIView(generics.CreateAPIView):
    queryset = GetInTouch.objects.all()
    serializer_class = GetInTouchSerializer
