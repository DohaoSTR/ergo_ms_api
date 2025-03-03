from random import randint
def generate_random_list(start, end, count):
    """
    Генерирует случайный список чисел в указанном диапазоне.
    """
    start,end,count = int(start), int(end), int(count)
    if start >= end or count <= 0:
        raise ValueError("Неверные параметры")
    return [randint(start, end) for _ in range(count)]