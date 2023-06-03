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
        fields = ('product', 'image', 'is_active')


class ProductCreateSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False)

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
        uploaded_images = validated_data.pop("product_images")
        category = validated_data.pop('category')
        product = Product.objects.create(**validated_data)
        product.category.set(category)
        print(uploaded_images)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product
