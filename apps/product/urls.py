from django.urls import path

from apps.product.views import CategoryListAPIView, CategoryRetrieveAPIView, BrandListAPIView, BrandRetrieveAPIView, \
    ProductCreateAPIView, ProductListAPIView, NewProductListAPIView, ProductRetrieveAPIView, BannerListAPIView, \
    BrandedProductsAPIView

urlpatterns = [
    # category -->
    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:pk>/', CategoryRetrieveAPIView.as_view()),

    # brand
    path('brand-list/', BrandListAPIView.as_view()),
    path('brand/<int:pk>/', BrandRetrieveAPIView.as_view()),
    path('brand/<int:pk>/products/', BrandedProductsAPIView.as_view()),

    # product
    path('product-create/', ProductCreateAPIView.as_view()),
    path('product/', ProductListAPIView.as_view()),
    path('product/new/', NewProductListAPIView.as_view()),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view()),

    path('banner/', BannerListAPIView.as_view())
]
