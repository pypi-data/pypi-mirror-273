import pandas as pd
import torch
import torch.nn as nn
import numpy as np
from .methods import *


file_path = '../data/Data_learning.csv'
train_data = pd.read_csv(file_path)


class Exponentation(nn.Module):
    def __init__(self):
        super(Exponentation, self).__init__()
        self.fc1 = nn.Linear(4, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc_time = nn.Linear(64, 7)
        self.fc_memory = nn.Linear(64, 7)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)

        time_prediction = self.fc_time(x)
        memory_prediction = self.fc_memory(x)

        return time_prediction, memory_prediction


model = Exponentation()

model.load_state_dict(torch.load('../data/my_model.pth'))

# Перевод модели в режим оценки
model.eval()


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def is_prime(n_array):
    primes = []
    for n in n_array:
        if n <= 1:
            primes.append(False)
        elif n == 2:
            primes.append(True)
        elif n % 2 == 0:
            primes.append(False)
        else:
            is_prime_flag = True
            for i in range(3, int(n**0.5) + 1, 2):
                if n % i == 0:
                    is_prime_flag = False
                    break
            primes.append(is_prime_flag)
    return primes


best_method = {'power_with_naive': 0, 'accum': 1, 'tree': 2, 'binary': 3, 'stairs': 4, 'power_fact': 5, 'right_left': 6}


def get_prediction(your_base, your_exp, t_factor):
    # Преобразование списков в массивы NumPy
    your_base = np.array(your_base)
    your_exp = np.array(your_exp)
    t_factor = np.array(t_factor)


    # Нормализация входных данных
    max_base = train_data.max().iloc[0]
    min_base = train_data.min().iloc[0]
    max_exp = train_data.max().iloc[1]
    min_exp = train_data.min().iloc[1]
    normalized_base = (your_base - min_base) / (max_base - min_base)
    normalized_exp = (your_exp - min_exp) / (max_exp - min_exp)


    # Создание тестового массива с правильной размерностью
    tester = np.vstack((normalized_base, normalized_exp, t_factor, is_prime(your_exp)))
    tester_torch = torch.tensor(tester.T, dtype=torch.float32)


    # Передача данных модели для предсказания
    with torch.no_grad():
        time_outputs, memory_outputs = model(tester_torch)


    # Определение индексов с максимальными значениями для времени и памяти
    predicted_time = torch.argmax(time_outputs, dim=1)
    predicted_memory = torch.argmax(memory_outputs, dim=1)


    # Получение предсказанных методов
    predicted_time_method = [get_key(best_method, idx.item()) for idx in predicted_time]
    predicted_memory_method = [get_key(best_method, idx.item()) for idx in predicted_memory]


    # Составление DataFrame
    df = pd.DataFrame({
        'Base': your_base,
        'Exponent': your_exp,
        'Consider Temperature': t_factor,
        'Best method time': predicted_time_method,
        'Best method memory': predicted_memory_method
    })

    # Конвертация значений в тип Decimal
    df['Base'] = df['Base'].apply(lambda x: Decimal(str(x)))
    df['Exponent'] = df['Exponent'].apply(lambda x: Decimal(str(x)))

    return df


def add_result_column(df, best_method_time=True):

    methods = {
        'power_with_naive': power_with_naive,
        'tree': tree,
        'accum': accum,
        'right_left': right_left,
        'stairs': stairs,
        'power_fact': power_fact,
        'binary': binary
    }
    method_column = 'Best method time' if best_method_time else 'Best method memory'

    # Конвертация значений обратно в тип float перед применением функции
    df['Base'] = df['Base'].apply(lambda x: float(x))
    df['Exponent'] = df['Exponent'].astype(int)

    df['result'] = df.apply(lambda row: Decimal(str(methods[row[method_column]](row['Base'], row['Exponent']))), axis=1)

    return df



