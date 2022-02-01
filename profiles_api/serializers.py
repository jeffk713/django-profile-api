from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
  """Serializer name field for testing our APIView"""
  
  name = serializers.CharField(max_length = 10)
  
class UserProfileSerializer(serializers.ModelSerializer):
  """Serializes a user profile object"""
  
  class Meta: 
    model = models.UserProfile
    fields = ('id', 'email', 'name', 'password')
    extra_kwargs = {
      'password': {
        'write_only': True, # cannot retrieve
        'style': { 'input_type': 'password' } # hash the input 
      }
    }

  # this create function overwrites the default create function from ModelSerializer
  def create(self, validated_data): 
    """ create a new user """
    user = models.UserProfile.objects.create_user(
      # calling create_user function in UserProfileManager
      email = validated_data['email'], 
      name = validated_data['name'],
      password = validated_data['password'],
    )
    
    return user
  
  def update(self, instance, validated_data):
        """Handle updating user account"""
        
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)