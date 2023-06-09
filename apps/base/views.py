from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404, )
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from apps.base.models import CustomUser, User
from apps.base.serializers import RegisterSerializer, UserSerializer
from .permission import IsOwnUserOrReadOnly


# Create your views here.
class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserListView(ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    permission_classes = (IsOwnUserOrReadOnly,)
    lookup_field = 'phone'

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, phone=kwargs['phone'])
        serializer = UserSerializer(get_object_or_404(User, phone=user), many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(CustomUser, phone=kwargs['phone'])
        serializer = UserSerializer(get_object_or_404(User, phone=instance), data=request.data, partial=partial,
                                    many=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
