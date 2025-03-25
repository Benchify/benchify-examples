from typing import List

def divide_numbers(x: int, y: int) -> float:
    return x / y

def find_maximum(lst: List[int]) -> int:
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val

def concatenate_strings(str1: str, str2: str) -> str:
    return str1 + str2

def calculate_area(radius: int) -> float:
    return 3.14 ** radius * 2
