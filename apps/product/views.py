from rest_framework import generics, permissions
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.product.models import *
from .serializers import CategorySerializer, BannerSerializer, BrandSerializer, ProductSerializer, SubCategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True, parent_category__isnull=True).order_by('-id')
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
    serializer_class = ProductSerializer
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
            param_condition = Q(name__icontains=param)
        cat_condition = Q()
        if cat:
            cat_condition = Q(category__name__icontains=cat)

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
