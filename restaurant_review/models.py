from datetime import date, datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField('review date')    
    def __str__(self):
        return self.restaurant.name + " (" + self.review_date.strftime("%x") +")"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experiment_one = models.BooleanField(default=False) #is experiment one complete
    experiment_one_result = models.BooleanField(default=True) #true = yes false = no 

    experiment_two = models.BooleanField(default=False) #is experiment two complete
    experiment_two_day = models.IntegerField(default=0) #day cnt of experiment completed
    experiment_two_last_photo_date = models.DateField(default=date(1999, 1, 1)) #date of last photo taken
    # experiment_two_result = models.BooleanField()
    isARCamera = models.BooleanField(default=True) #show participant AR camera
    showARImage = models.BooleanField(default=True) #show participant AR image 

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @property
    def isPhotoTaken(self):
        return date.today() == self.experiment_two_last_photo_date

    @property 
    def isComplete(self):
        return self.experiment_two_day >= 7