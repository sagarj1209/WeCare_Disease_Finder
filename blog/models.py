from django.db import models

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key = True)
    title = models.CharField(max_length=100)
    content1 = models.TextField()
    content2 = models.TextField()
    content3 = models.TextField()
    author = models.CharField(max_length=20)
    slug = models.CharField(max_length=15)
    timeStamp = models.DateTimeField(blank=True)
    thumbnail = models.ImageField(upload_to="blog/images", default="")
    
    def __str__(self):
        return self.title + 'by' + self.author