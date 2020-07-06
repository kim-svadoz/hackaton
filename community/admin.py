from django.contrib import admin
from community.models import Comment, Community

# Register your models here.

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','created_at','updated_at','date','user','hits')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','article','content','created_at','user',)

admin.site.register(Community,CommunityAdmin)
admin.site.register(Comment,CommentAdmin)