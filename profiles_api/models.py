from django.db import models

# below 2 lines are to overwrite default Django user model. refer to doc.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionMixin


class UserProfile(AbstractBaseUser, PermissionMixin):
  """Database model for users in the system"""
  email = models.EmailField(max_length=255, unique=True)
  name = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  
  objects = UserProfileManager()
  
  # username file is required by just writing "USERNAME_FIELD = 'email'"
  USERNAME_FIELD = 'email' # overwriting username, we pass email instead of username
  REQUIRED_FIELDS = ['name'] 
  
  # pass "self" into the first parameter!
  def get_full_name(self): 
    """Retrieve full name of user"""
    return self.name
  
  def get_short_name(self):
    """Retrieve short name of user"""
    return self.name
  
  # string representation for user, it is recommended 
  def __str__(self):
    """Return string representation of user"""
    return self.email
  