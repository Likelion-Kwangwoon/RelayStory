from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","nickname")

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            nickname=validated_data['nickname']
        )
        return user