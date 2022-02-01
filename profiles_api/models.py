from django.db import models

# below 2 lines are to overwrite default Django user model. refer to doc.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings # retrieve settings.py in project dir for data relationship


class UserProfileManager(BaseUserManager):
  """manager for user profiles"""
  
  def create_user(self, email, name, password = None):
    """create a new user profile"""
    if not email:
      raise ValueError('User must have an email')
    
    email = self.normalize_email(email)
    user = self.model(email = email, name = name)

    # set hashed password, 'set_password' comes from AbstractBaseUser
    user.set_password(password)
    user.save(using = self._db) # standard procedure in django to save
    
    return user

  def create_superuser(self, email, name, password):
    """create an admin user with given details"""
    user = self.create_user(email, name, password) # 'self' parameter is automatically passed in
    
    user.is_superuser = True # is_superuser comes from PermissionsMixin
    user.is_staff = True
    user.save(using = self._db)
    
    return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
  """Database model for users in the system"""
  email = models.EmailField(max_length = 255, unique = True)
  name = models.CharField(max_length = 255)
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  
  objects = UserProfileManager()
  
  # username field is required by just writing "USERNAME_FIELD = 'email'"
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
  
class ProfileFeedItem(models.Model):
  """ profile status update """
  
  user_profile = models.ForeignKey(
    settings.AUTH_USER_MODEL, # this way, it reflects the changes automatically
    on_delete = models.CASCADE
    )

  status_text = models.CharField(max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    """ return the model as string """
    
    return slef.status_text