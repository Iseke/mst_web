from rest_framework import serializers

from apps.api.models import Task
from apps.api.tasks import send_notification


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'is_done']
        extra_kwargs = {
            'description': {
                'write_only': True
            },
            'is_done': {
                'read_only': True
            }
        }


class TaskDetailSerializer(TaskSerializer):
    class Meta(TaskSerializer.Meta):
        extra_kwargs = {
            'description': {
                'required': True
            },
            'is_done': {
                'read_only': True
            }
        }


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    deadline = serializers.DateTimeField(read_only=True)
    is_done = serializers.BooleanField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'deadline', 'is_done']

    def update(self, instance, validated_data):
        instance.is_done = validated_data.get('is_done')
        instance.save()
        data = {
            'name': instance.name,
            'is_done': instance.is_done,
            'id': instance.id
        }
        user_email = self.context['request'].user.email
        try:
            send_notification.delay(user_email, data)
        except Exception as e:
            print(e)
        return instance
