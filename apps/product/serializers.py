from rest_framework import serializers
from apps.product.models import Category, Brand, Banner, Product, ProductImage


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        qs = Category.objects.filter(parent=obj, is_active=True)
        sz = SubCategorySerializer(qs, many=True)
        return sz.data

    class Meta:
        model = Category
        fields = ['id', 'title', 'children', 'icon']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id',
                  'get_image_url'
                  ]


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    category = CategorySerializer(many=True, read_only=True)

    # def get_images(self, obj):
    #     qs = ProductImage.objects.filter(is_active=True, product=obj)
    #     sz = ProductImageSerializer(instance=qs, many=True)
    #     return sz.data

    class Meta:
        model = Product
        fields = ['id',
                  'status',
                  'name',
                  'category',
                  'brand',
                  'price',
                  'rating',
                  'discount',
                  'get_discounted_price',
                  'made_in',
                  'consists',
                  'capacity',
                  'guarantee',
                  'product_images',
                  ]
        extra_kwargs = {
            'slug': {'read_only': True}
        }


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)

    class Meta:
        model = ProductImage
        fields = ('image', 'is_active')


class ProductCreateSerializer(serializers.ModelSerializer):
    product_images = ProductImageCreateSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'status',
            'name',
            'category',
            'brand',
            'price',
            'rating',
            'discount',
            'made_in',
            'consists',
            'capacity',
            'guarantee',
            'product_images']

    def create(self, validated_data):
        images = validated_data.pop('product_images')
        product = Product.objects.create(**validated_data)
        print(images)
        for item in images:
            ProductImage.objects.create(product=product, **item)
        return product
