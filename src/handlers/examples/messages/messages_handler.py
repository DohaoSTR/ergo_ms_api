from src.core.utils.auto_api.base_handler import BaseHandler

class HandlerClass(BaseHandler):
    def process(self):
        message_type = self.params.get('type', 'info')
        
        messages = {
            'info': {
                'title': 'Информационное сообщение',
                'text': 'Это информационное сообщение для пользователя',
                'level': 'info'
            },
            'error': {
                'title': 'Сообщение об ошибке',
                'text': 'Произошла ошибка при выполнении операции',
                'level': 'error'
            },
            'warning': {
                'title': 'Предупреждение',
                'text': 'Внимание! Это предупреждающее сообщение',
                'level': 'warning'
            },
            'success': {
                'title': 'Успешное выполнение',
                'text': 'Операция успешно выполнена',
                'level': 'success'
            }
        }
        
        return {
            "message": messages.get(message_type, messages['info'])
        } 