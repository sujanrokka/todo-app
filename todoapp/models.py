from django.db import models
from django.contrib.auth.models  import User



# Create your models here.
class TODO(models.Model):
    title=models.CharField(max_length=20)
    description = models.TextField()
    is_done=models.BooleanField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.title