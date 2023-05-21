from django.urls import path
from .views import GetInTouchCreateAPIView

urlpatterns = [
    path('contact/', GetInTouchCreateAPIView.as_view()),
]
