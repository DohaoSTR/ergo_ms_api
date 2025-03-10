# Файл для создания sql запросов
# Пример:
# def get_users(user_id: int):
#     return tuple(
#         [
#             """
#             select
#                 id,
#                 username,
#                 email,
#                 first_name,
#                 last_name
#             from
#                 auth_user
#             where id = %s
#             """,
#             tuple([user_id]),
#         ]
#     )