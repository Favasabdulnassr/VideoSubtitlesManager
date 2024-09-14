from django.db import models

# Create your models here.

class video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subtitle(models.Model):
    video =  models.ForeignKey(video,on_delete=models.CASCADE,related_name='subtitles')
    file = models.FileField(upload_to='subtitle/')
    language = models.CharField(max_length=50)    
    text_index = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subtitle for {self.video.title}"    
