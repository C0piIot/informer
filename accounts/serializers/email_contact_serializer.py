from rest_framework import serializers


class EmailContactSerializer(serializers.Serializer):
    email = serializers.EmailField()
