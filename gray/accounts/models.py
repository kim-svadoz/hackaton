from django.db import models
from imagekit.models import ProcessedImageField 
from imagekit.processors import ResizeToFill
from django.conf import settings

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