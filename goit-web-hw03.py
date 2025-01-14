import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
from time import time

def sort_files_by_extension(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    def process_directory(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                with ThreadPoolExecutor() as executor:
                    executor.submit(process_directory, item_path)
            else:
                copy_file(item_path)

    def copy_file(file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        if not ext:
            return

        ext_dir = os.path.join(target_dir, ext)
        if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

        shutil.copy(file_path, os.path.join(ext_dir, os.path.basename(file_path)))

    process_directory(source_dir)

def factorize_number(number):
    factors = []
    for i in range(1, int(number ** 0.5) + 1):
        if number % i == 0:
            factors.append(i)
            if i != number // i:
                factors.append(number // i)
    return sorted(factors)

def factorize(*numbers):
    return [factorize_number(num) for num in numbers]

def factorize_parallel(*numbers):
    with Pool(cpu_count()) as pool:
        return pool.map(factorize_number, numbers)

# Тестування
if __name__ == "__main__":
    source = "picture" 
    target = "dist"    

    print("Сортування файлів...")
    sort_files_by_extension(source, target)
    print("Сортування завершено!")

    numbers_to_factorize = [128, 255, 99999, 10651060]

    print("\nСинхронна факторизація...")
    start = time()
    result_sync = factorize(*numbers_to_factorize)
    end = time()
    print(f"Результат: {result_sync}")
    print(f"Час виконання: {end - start:.4f} секунд")

    print("\nПаралельна факторизація...")
    start = time()
    result_parallel = factorize_parallel(*numbers_to_factorize)
    end = time()
    print(f"Результат: {result_parallel}")
    print(f"Час виконання: {end - start:.4f} секунд")
