import subprocess
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import video,Subtitle
from .forms import VideoUploadForm
import os
from django.http import JsonResponse




class VideoListView(ListView):
    model = video
    template_name = 'video_list.html'
    context_object_name = 'videos'



class VideoDetailView(DetailView):
    model = video
    template_name = 'video_detail.html'
    context_object_name = 'video'    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        language = self.request.GET.get('language', 'eng')
        subtitles = video.subtitles.all()
        print(subtitles)


        context['subtitles'] = subtitles
        context['start_time'] = self.request.GET.get('start_time', None)
        context['language'] = language
        return context

    
    
    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            query = request.POST.get('q', '').lower()
            language = request.POST.get('language', 'en')  
            print('languaaaaaaaaaage',language)
            video = self.get_object()

            subtitles = video.subtitles.filter(language=language).first()
            results = []
            

            if subtitles and query:
                lines = subtitles.text_index.split('\n')
                i = 0   

                while i < len(lines):
                    if '-->' in lines[i]:
                        timestamp_range = lines[i]
                        timestamp = timestamp_range.split(' --> ')[0].strip()
                        subtitle_text = lines[i+1].strip()
                        if query in subtitle_text.lower():
                            results.append({'timestamp': timestamp, 'line': subtitle_text})
                        i += 2
                    else:
                        i += 1

                return JsonResponse({'results': results})
        return JsonResponse({'error': 'Invalid request'}, status=400)
    


    


class videoCreateView(CreateView):
    model = video
    form_class = VideoUploadForm
    template_name = 'video_upload.html'
    success_url = reverse_lazy('video_list')

    def form_valid(self,form):
        video = form.save()
        self.process_video(video)
        return redirect(self.success_url)
    
    def process_video(self,video):
        video_path = video.video_file.path

        srt_path_template = os.path.join(settings.MEDIA_ROOT, 'subtitles', os.path.basename(video_path) + '_{lang}.srt')
        vtt_path_template = os.path.join(settings.MEDIA_ROOT, 'subtitles', os.path.basename(video_path) + '_{lang}.vtt')

        os.makedirs(os.path.dirname(srt_path_template.format(lang='en')), exist_ok=True)

        languages = self.get_available_languages(video_path)


            
        for i, lang in enumerate(languages):
            srt_path = srt_path_template.format(lang=lang)
            vtt_path = vtt_path_template.format(lang=lang)

            try:
                command = [
                    settings.FFMPEG_PATH,
                    '-i', video_path,
                    '-map', f'0:s:{i}',  
                    '-c:s', 'srt',
                    srt_path
                ]
                subprocess.run(command, check=True)

                if os.path.exists(srt_path):
                    command = [
                        settings.FFMPEG_PATH,
                        '-i', srt_path,
                        '-c:s', 'webvtt',
                        vtt_path
                    ]
                    subprocess.run(command, check=True)
                    self.index_subtitles(video, vtt_path, lang)
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg command failed: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def get_available_languages(self, video_path):
        command = [
            settings.FFMPEG_PATH,
            '-i', video_path  
        ]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        output = result.stderr
        print('FFmpeg Output:', output)

        subtitles_list = []
        
        for line in output.splitlines():
            if "Subtitle:" in line:
                language = line.split('(')[1].split(')')[0]  
                subtitles_list.append(language)
        
        print('Subtitles List:', subtitles_list)
        
        return subtitles_list






    def index_subtitles(self, video, vtt_path, language):
        try:
            with open(vtt_path, 'r', encoding='utf-8') as f: 
                subtitle_text = f.read()
        except UnicodeDecodeError as e:
            print(f"Error reading subtitle file: {e}")
            return
            

        Subtitle.objects.create(
            video=video,
            file=os.path.relpath(vtt_path, settings.MEDIA_ROOT),
            text_index=subtitle_text,
            language=language
        )