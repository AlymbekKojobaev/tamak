from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cook
from rest_framework.relations import SlugRelatedField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "date_joined",
        )


class CookSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='first_name', read_only=True)


    def create(self, validated_data):
        if self.context.get('user_id', None):
            validated_data['user_id']=self.context.get('user_id')
        else:
            validated_data['user_id']=self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = Cook
        fields = (
                'user',
                'position',
                'education',
                'experience',
                'work_history'
        )
