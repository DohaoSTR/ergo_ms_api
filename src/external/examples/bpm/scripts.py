import random
import string

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email():
    return f"{generate_random_string(8)}@{generate_random_string(5)}.com"

def generate_random_status():
    return random.choice(['Pending', 'In Progress', 'Completed', 'Cancelled'])

def get_tasks(num_processes, num_tasks, num_users):
    # Генерация данных о процессах
    processes = [
        {"id": i + 1, "name": f"Process {i + 1}", "description": generate_random_string(50)}
        for i in range(num_processes)
    ]

    # Генерация данных о задачах
    tasks = [
        {"id": i + 1, "process_id": random.randint(1, num_processes), "name": f"Task {i + 1}", "status": generate_random_status()}
        for i in range(num_tasks)
    ]

    # Генерация данных о пользователях
    users = [
        {"id": i + 1, "name": f"User {i + 1}", "email": generate_random_email()}
        for i in range(num_users)
    ]

    # Формирование структуры данных для JSON
    bpm_data = {
        "processes": processes,
        "tasks": tasks,
        "users": users
    }

    return bpm_data