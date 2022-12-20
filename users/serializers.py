from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators = [UniqueValidator(User.objects.all(), "This field must be unique.")])
    username = serializers.CharField(validators = [UniqueValidator(User.objects.all(), "A user with that username already exists.")])


    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'is_superuser',]
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ["is_superuser"]

    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
