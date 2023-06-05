from rest_framework import generics, permissions, status
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.product.models import *
from .serializers import ProductCreateSerializer, CategorySerializer, BannerSerializer, BrandSerializer, \
    ProductSerializer, SubCategorySerializer

from rest_framework.views import APIView


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


class BrandedProductsAPIView(APIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk):
        print(request.data)
        qs = self.queryset.filter(brand=pk)
        sr = self.serializer_class(qs, many=True)
        return Response(sr.data)


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = (permissions.IsAdminUser,)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-id')
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = self.queryset.all()
        param = self.request.GET.get('search')
        cat = self.request.GET.get('category')
        param_condition = Q()
        if param:
            param_condition = Q(name__icontains=param) | Q(category__title_uz__icontains=param) | Q(
                category__title_en__icontains=param) | Q(category__title_ru__icontains=param)
        cat_condition = Q()
        if cat:
            cat_condition = Q(category__title_uz__icontains=cat) | Q(
                category__title_en__icontains=cat) | Q(category__title_ru__icontains=cat)

        qs = qs.filter(param_condition | cat_condition)
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
