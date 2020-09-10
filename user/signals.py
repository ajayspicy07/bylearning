
from django.db.models.signals import post_save
from . models import User,Page,Profile
from django.dispatch import receiver




''' Signal For Page  '''

''' Signal For User '''
@receiver(post_save,sender=Page)
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(content_object=instance)



@receiver(post_save,sender=Page )
@receiver(post_save,sender=User )
def update_profile(sender,instance,created,**kwargs):
	if created == False:
		if sender == User:
			profile = Profile.objects.get(users__username=instance.username)
		else:
			profile = Profile.objects.get(pages__name = instance.name)

		profile.save()
	
