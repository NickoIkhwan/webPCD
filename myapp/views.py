from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from .detector import TrafficDetector
from .forms import UploadFile
from .models import Document
from django.shortcuts import render, redirect
import os


MODEL_PATH = os.path.join(settings.BASE_DIR, 'myapp', 'media', 'model_4', 'model_4.pt')
detector = TrafficDetector(MODEL_PATH)

def detect_stream(request, file_id):
    doc = get_object_or_404(Document, id=file_id)
    file_path = doc.uploaded_file.path
    
    # Track current file being processed
    detector.current_file_id = file_id
    detector.stop_processing = False
    
    return StreamingHttpResponse(
        detector.process_file(file_path),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

def get_vehicle_count(request):
    return JsonResponse({'objects_count': detector.objects_count})

def delete_file(request, file_id):
    doc = get_object_or_404(Document, id=file_id)
    # Get the file path before deleting from database
    file_path = doc.uploaded_file.path
    
    # If this file is currently being processed, stop it
    if detector.current_file_id == file_id:
        detector.stop_processing = True
        import time
        time.sleep(1)  # Wait for stream to stop
    
    # Delete from database
    doc.delete()
    
    # Delete the physical file from the uploads folder
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
    
    return redirect('traffic')

# def file_upload(request):
#     if request.method == 'POST':
#         form = UploadFile(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return render('list')
#     else:
#         # This part creates the empty form for the user to see
#         form = UploadFile()
    
#     # Make sure this points to 'upload_file.html'
#     return render(request, 'upload_file.html', {'form': form})

# def file_list(request):
#     files = Document.objects.all()
#     return render(request, 'file_list.html', {'files': files})


# def video_feed(request):
#     detector = TrafficDetector('model_4/model_4.pt')
#     video_path = 'myapp/media/traffic_video2.mp4'  # Update this path
#     return StreamingHttpResponse(
#         detector.get_frames(video_path),
#         content_type='multipart/x-mixed-replace; boundary=frame'
#     )

def traffic_view(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadFile()
    
    files = Document.objects.all()

    active_file_id = request.GET.get('play')
    return render(request, 'traffic_system.html',{
        'form': form,
        'files':files,
        'active_file_id': active_file_id,
        'objects_count': detector.objects_count
        })

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'index.html')

def Doc(request):
    return render(request, 'doc.html')

