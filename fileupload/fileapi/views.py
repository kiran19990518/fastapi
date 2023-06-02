from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import UploadedFile
from .tasks import process_file

@api_view(['POST'])
def upload_file(request):
    file_obj = request.FILES.get('file')
    uploaded_file = UploadedFile.objects.create(file=file_obj)
    process_file.delay(uploaded_file.id)  # Start asynchronous processing
    return JsonResponse({'status': 'success'})

