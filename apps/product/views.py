from rest_framework import generics, permissions, status
from django.db.models import Q
from rest_framework.response import Response

from apps.product.models import *
from .serializers import ProductCreateSerializer, CategorySerializer, BannerSerializer, BrandSerializer, \
    ProductSerializer, SubCategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent__isnull=True).order_by('-id')
    serializer_class = CategorySerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = SubCategorySerializer
    lookup_field = 'pk'


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # permission_classes = (permissions.IsAdminUser,)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-id')
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = self.queryset.all()
        param = self.request.GET.get('search')
        cat = self.request.GET.get('category')

        param_condition = Q()
        if param:
            print(param)
            param_condition = Q(name__icontains=param)
        cat_condition = Q()
        if cat:
            cat_condition = Q(category__title__icontains=cat)

        qs = qs.filter(param_condition, cat_condition)
        return qs


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class NewProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-created_at')[:10]
    serializer_class = ProductSerializer
    pagination_class = None


class BannerListAPIView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None
