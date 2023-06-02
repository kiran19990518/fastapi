
from django.shortcuts import render
from .models import UploadedFile, SeparatedData

def upload_file(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        uploaded_file = UploadedFile.objects.create(file=file_obj)
        separate_data(uploaded_file)
        return render(request, 'uploadsucess.html')
    return render(request, 'uploadfile.html')

def separate_data(uploaded_file):
    text = ""
    numbers = ""
    words = ['hi', 'hello', 'bye', 'thanks', 'one', 'two', 'three', 'four', 'five',
             'six', 'seven', 'eight', 'nine', 'ten', 'sunday', 'monday', 'tuesday',
             'wednesday', 'thursday', 'friday', 'saturday', 'and']
    with uploaded_file.file.open('r') as file:
        for line in file:
            for word in line.split():
                if word.isdigit():
                    numbers += word + " "
                else:
                    text += word + " "
    is_words = [word in text for word in words]
    separated_data = SeparatedData.objects.create(
        uploaded_file=uploaded_file,
        text=text.strip(),
        numbers=numbers.strip(),
        is_words = is_words
    )
    res= separated_data.save()
    return res

