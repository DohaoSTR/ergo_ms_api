import os
from datetime import datetime

from django.conf import settings

from rest_framework.exceptions import ValidationError

from src.core.utils.auto_api.base_handler import BaseHandler

class HandlerClass(BaseHandler):
    def process(self):
        file = self.params.get('file')
        if not file:
            raise ValidationError('Файл не найден')

        # Создаем директорию, если она не существует
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)

        # Генерируем уникальное имя файла с timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_name = file.name
        file_extension = os.path.splitext(original_name)[1]
        new_filename = f"{timestamp}_{original_name}"
        
        # Полный путь для сохранения файла
        file_path = os.path.join(upload_dir, new_filename)
        
        # Сохраняем файл
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Формируем относительный путь для URL
        relative_path = os.path.join('uploads', new_filename)
        
        return {
            "message": "Файл успешно загружен",
            "file_name": new_filename,
            "original_name": original_name,
            "file_size": file.size,
            "file_type": file.content_type,
            "path": relative_path
        } 