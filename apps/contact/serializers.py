from rest_framework import serializers
from apps.contact.models import GetInTouch


class GetInTouchSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetInTouch
        fields = ['id',
                  'full_name',
                  'phone',
                  'email',
                  'message',
                  'user_data',
                  ]
