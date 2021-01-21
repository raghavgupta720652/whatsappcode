from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext, ugettext_lazy as _

# Create your models here.
class User(AbstractUser):
                
    first_name = models.CharField(null=True,blank=True, max_length=15)
    last_name = models.CharField(null=True,blank=True, max_length=15)
    created_time = models.DateTimeField(auto_now_add=True, blank=True)
    admin_verified = models.BooleanField(default=False)
    contact_no = models.CharField(null=True,blank=True, max_length=15)
     
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'User'
        
class PhoneNumber(models.Model):
    
    phone_number =  models.CharField(null=True,blank=True, max_length=15)
    added_by = models.ForeignKey(User,blank=True, null=True, on_delete=models.deletion.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)  
    
    class Meta:
        verbose_name = _('Phone Number')
        verbose_name_plural = _('Phone Numbers')
        db_table = 'Phone Number'


        
class Content(models.Model):
    
    phones =  models.ForeignKey(PhoneNumber,blank=True, null=True, on_delete=models.deletion.CASCADE)
    sent_by = models.ForeignKey(User,blank=True, null=True, on_delete=models.deletion.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_on = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    
    
    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Content')
        db_table = 'Content'
        
        
class ContentImages(models.Model):
    
    image = models.FileField(upload_to="images", null=True, blank=True)
    phone_numbers = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="images")
    created_by = models.ForeignKey(User, related_name="content_images", on_delete=models.CASCADE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'tbl_content_images'
        verbose_name_plural = "content images"        
        
        