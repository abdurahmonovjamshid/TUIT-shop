from django.urls import path
from .views import OrderListAPIView, OrderCreateAPIView

urlpatterns = [
    path('order-list/', OrderListAPIView.as_view()),
    path('order/', OrderCreateAPIView.as_view())
]
