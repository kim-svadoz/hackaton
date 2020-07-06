from django.db import models
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from django.utils import timezone


def articles_image_path(instance, filename):
    return f'user_{instance.user.pk}/{filename}'

# Create your models here.


class Community(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    hits = models.PositiveIntegerField(default=0)
    # blank = 유효성 검사시
    # null = DB상에 컬럼에
    image = models.ImageField(blank=True, upload_to=articles_image_path)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(200, 300)],
        format='jpeg',
        options={'quality': 90}
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_articles',
        blank=True
    )

    recommend_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='recommend_articles',
        blank=True
    )

    

    @property
    def click(self):
        self.hits += 1
        self.save()



class Comment(models.Model):
    # models.ForeignKey(상속받을 클래스명, Article이 삭제되었을때 어떻게 할것인지)
    # 멤버 변수 = models.외래키(참조하는 객체)
    # 역참조 값 설정 related_name='comments'
    article = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    comment_select_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comment_select_users',
        blank=True
    )