from rest_framework import serializers
from content.models import Mashup, Output


class OutputSerializer(serializers.ModelSerializer):
    """
    Serializer for GET method, reading Output
    """
    class Meta:
        model = Output
        depth = 2 # Include details about fk relationships
        fields = ('id', 'body', 'num_votes', 'mashup')


class OutputWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for PUT methods. Checks for key validity in mashup field
    """
    mashup = serializers.PrimaryKeyRelatedField(queryset=Mashup.objects.all(), allow_null=False)

    class Meta:
        model = Output
        fields = ('id', 'body', 'num_votes', 'mashup')