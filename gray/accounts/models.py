from django.db import models
from imagekit.models import ProcessedImageField 
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.contrib.auth.models import UserManager as DefaultUserManager

def profile_image_path(instance, filename):
	return f'user_{instance.user.pk}/{filename}'

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40, blank =True)
    introduction = models.TextField(blank=True)
    image = ProcessedImageField (
    		blank = True,
        	upload_to = profile_image_path,
        	processors = [ResizeToFill(300, 300)],
        	format = 'JPEG',
        	options = {'quality':90},
    		)

# class UserManager(DefaultUserManager):
#     # 페이스북으로 가입하면 user_type을 K(Kakao)으로 지정한다. 
#     def get_or_create_facebook_user(self, user_pk, extra_data):
#         user = User.objects.get(pk=user_pk)
#         user.user_type = "K"
# 		user.nickname = extra_data['nickname']
#         user.save()
        
#         return user