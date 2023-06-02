from celery import shared_task
from .models import UploadedFile, ProcessedFile

@shared_task
def process_file(file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    text = uploaded_file.file.read().decode('utf-8')
    words = ['hi', 'hello', 'bye', 'thanks', 'one', 'two', 'three', 'four', 'five',
             'six', 'seven', 'eight', 'nine', 'ten', 'sunday', 'monday', 'tuesday',
             'wednesday', 'thursday', 'friday', 'saturday', 'and']
    numbers = []
    processed_words = []

    # Separate text and numbers
    for word in text.split():
        if word.isdigit():
            numbers.append(int(word))
        else:
            processed_words.append(word)

    # Check if the text contains the specified words
    is_words = [word in processed_words for word in words]

    # Save the processed data
    processed_file = ProcessedFile.objects.create(
        uploaded_file=uploaded_file,
        text=' '.join(processed_words),
        numbers=numbers,
        is_words=is_words
    )
    processed_file.save()
