from django.db import models
from tvsmashup.validators import FileValidator
from django.dispatch import receiver
from PIL import Image
from accounts.models import Account
import os, secrets

class TVShow(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name')
        ]

############################ File handling #####################################

#ADDED TO HANDLE FILE UPLOAD
validate_file = FileValidator(max_size=1024 * 5000,
                             content_types=('image/jpeg','image/png','image/gif','image/tiff','application/x-empty',))

def image_path_handler(instance, filename):
    fn, ext = os.path.splitext(filename)
    #Create a random filename using hash function
    name = secrets.token_hex(20)
    print("uploading",instance.__dict__)
    return "titleimage_{id}/{name}{ext}".format(id=instance.show_id,name=name,ext=ext)

def _delete_file(path):
   """ Deletes file from filesystem. """
   print("Deleting Image")
   if os.path.isfile(path):
        os.remove(path)

class TVImage(models.Model):
    show = models.ForeignKey(TVShow,on_delete=models.CASCADE)
    picture = models.FileField(upload_to=image_path_handler,validators=[validate_file],null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['show'], name='unique_tvimage')
        ]

@receiver(models.signals.post_delete, sender=TVImage)
def delete_title_image(sender, instance, *args, **kwargs):
    print("DELETING")
    if instance.picture:
        _delete_file(instance.picture.path)

@receiver(models.signals.post_save, sender=TVImage)
def save_title_image(sender, instance, *args, **kwargs):
    if instance.picture:
        image = Image.open(instance.picture.path)
        new_image = image.resize((300, 200))
        filename, file_extension = os.path.splitext(instance.picture.path)
        #new_file_path = filename + '_NEW' + file_extension
        new_image.save(instance.picture.path)


class SmashUp(models.Model):
    creator = models.ForeignKey(Account,on_delete=models.CASCADE)
    show_1 = models.ForeignKey(TVShow,on_delete=models.CASCADE,related_name='show1')
    show_2 = models.ForeignKey(TVShow,on_delete=models.CASCADE,related_name='show2')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('show_1', 'show_2',)

    def clean(self):
        print("cleaning")
        direct = SmashUp.objects.filter(show_1 = self.show_1, show_2 = self.show_2)
        reverse = SmashUp.objects.filter(show_1 = self.show_2, show_2 = self.show_1)


        if direct.exists() or reverse.exists() or (self.show_1 == self.show_2):
            raise ValidationError({'key':'Already exists in another combination'})
