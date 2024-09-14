from django import forms
from .models import video

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = video
        fields = ['title','video_file']