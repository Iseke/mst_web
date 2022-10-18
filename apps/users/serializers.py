from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.response import Response

from apps.users.models import MyUser
from apps.users.tokens import password_reset_token
from apps.users.utils import pre_send_confirmation_email


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name',
                  'phone', 'password']
        extra_kwargs = {
            'middle_name': {
                'required': False
            },
            'phone': {
                'required': False
            }
        }

    def validate_password(self, pswd):
        if len(pswd) < 5:
            raise serializers.ValidationError('Password length should be more than 5')
        return pswd

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(read_only=True)

    def validate_email(self, attrs):
        if not MyUser.objects.filter(email__iexact=attrs).exists():
            raise serializers.ValidationError("There is no active user registered with the specified email address.")

        return attrs

    def create(self, validated_data):
        user_instance = MyUser.objects.get(email__iexact=validated_data['email'])
        request = self.context['request']
        pre_send_confirmation_email(request, user_instance, 'emails/password_reset_email.html')
        return {'message': 'Reset your password through the link that was sent to your email.'}


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    new_password_confirmation = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirmation']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match.",
                                               'new_password_confirmation': "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        uidb64 = self.context.get('view').kwargs.get('uidb64')
        token = self.context.get('view').kwargs.get('token')

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            user.set_password(validated_data['new_password'])
            user.save()
            return Response({'message': 'Password has been reset.'})
        else:
            return Response({'message': 'The reset link was invalid, possibly because it '
                                        'has already been used. Please, request a new link.'})

