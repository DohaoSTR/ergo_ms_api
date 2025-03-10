import os
import mimetypes

from django.conf import settings
from django.http import FileResponse
from django.utils.encoding import smart_str

from rest_framework.exceptions import NotFound

from src.core.utils.auto_api.base_handler import BaseHandler

class HandlerClass(BaseHandler):
    def process(self):
        filename = self.params.get('filename')
        if not filename:
            raise NotFound('Имя файла не указано')
            
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        
        if not os.path.exists(file_path):
            raise NotFound(f'Файл {filename} не найден')
            
        try:
            # Получаем размер файла
            file_size = os.path.getsize(file_path)
            
            # Открываем файл
            file = open(file_path, 'rb')
            
            # Определяем content_type
            content_type = self.get_content_type(filename)
            
            # Создаем response
            response = FileResponse(
                file,
                content_type=content_type,
                as_attachment=True,
                filename=filename
            )
            
            # Устанавливаем заголовки для корректной загрузки
            response['Content-Length'] = str(file_size)
            response['Content-Disposition'] = f'attachment; filename="{smart_str(filename)}"'
            
            # Добавляем заголовки безопасности
            response['X-Content-Type-Options'] = 'nosniff'
            response['Cache-Control'] = 'no-cache'
            
            return response
            
        except IOError as e:
            raise NotFound(f'Ошибка при чтении файла {filename}: {str(e)}')
        except Exception as e:
            raise NotFound(f'Ошибка при обработке файла {filename}: {str(e)}')
    
    def get_content_type(self, filename):
        """Определяет content_type для любого типа файла"""
        # Пробуем определить тип через mimetypes
        guessed_type = mimetypes.guess_type(filename)[0]
        if guessed_type:
            return guessed_type
            
        # Если не удалось определить тип, используем общий бинарный тип
        return 'application/octet-stream' 