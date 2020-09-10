
''' COMMENT MODEL '''



from django.db import models
from project.models import Project,ProjectBanner
from post.models import Post

from user.models import Profile

from django.utils import timezone
from django.utils.text import slugify

from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType



from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.

class Comment(models.Model):
 

    limit = models.Q(model='post') | models.Q(model ='project')| models.Q(model='projectbanner')

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,
        limit_choices_to=limit, blank=False, null=False
    )

    object_id 	=models.PositiveIntegerField(null =False,blank=False)

    content_object = GenericForeignKey('content_type', 'object_id')
    user       =models.ForeignKey(Profile ,on_delete =models.CASCADE , related_name ='for_comments')
    
    question	= models.TextField()
    date_created=models.DateTimeField(default=timezone.now) 

    class Meta:
        db_table = "Comments"
        ordering = ('-date_created',)
    
    def __str__(self):
       return str(self.question)
    

class Reply(models.Model):

    user       =models.ForeignKey(Profile ,on_delete =models.CASCADE , related_name="for_replies")
    for_comment	=models.ForeignKey(Comment,on_delete=models.CASCADE, related_name = "replies")
    answer		=models.TextField()
    date_created=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.answer)

    class Meta:
        db_table = "Replies"
        ordering = ('-date_created',)
    

