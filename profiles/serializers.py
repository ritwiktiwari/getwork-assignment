from rest_framework import serializers
from profiles import models

class UserSerializer(serializers.ModelSerializer):
	"""
	Serializes a user profile object
	"""
	class Meta:
		model = models.UserProfile
		fields = ('id', 'email', 'name', 'password')
		extra_kwargs = {
			'password': {
				'write_only': True,
				'style': {
					'input_type': 'password'
				}
			}
		}

	def create(self, validated_data):
		"""
		Creata and return a new user
		"""
		user = models.UserProfile.objects.create_user(
				email = validated_data['email'],
				name = validated_data['name'],
				password = validated_data['password']

			)

		return user

class UserSigninSerializer(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)