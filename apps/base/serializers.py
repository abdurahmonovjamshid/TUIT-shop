from rest_framework import serializers
from .models import CustomUser, User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    city = serializers.ChoiceField(choices=[
        'Andijan', 'Bukhara', 'Jizzakh', 'Kashkadarya', 'Navoi', 'Namangan', 'Samarkand', 'Samarkand', 'Sirdarya',
        'Surkhandarya', 'Tashkent',
        'Fergana', 'Khorezm'])

    class Meta:
        model = CustomUser
        fields = ('phone', 'password', 'password2', 'first_name', 'last_name', 'city')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        custom_user = CustomUser.objects.create(
            phone=validated_data['phone'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            city=validated_data['city'],
        )

        custom_user.set_password(validated_data['password'])
        custom_user.save()

        user = User.objects.create(
            phone=custom_user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            city=validated_data['city']
        )
        user.save()

        return custom_user


class ChangeNewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'password' 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                'success': False, 'message': 'Old password did not match, please try again'
            })
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': 'Password did not match, please try again'
            })
        user.set_password(password)
        user.save()
        return attrs


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(read_only=True)
    city = serializers.ChoiceField(choices=[
        'Andijan', 'Bukhara', 'Jizzakh', 'Kashkadarya', 'Navoi', 'Namangan', 'Samarkand', 'Samarkand', 'Sirdarya',
        'Surkhandarya', 'Tashkent',
        'Fergana', 'Khorezm'])

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'city']

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            # 'pic': 'http://127.0.0.1:8000' + obj.pic.url,
            'phone': obj.phone.phone,
            'city': obj.city,
        }
