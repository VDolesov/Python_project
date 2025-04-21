import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib

matplotlib.use('TkAgg')  # Устанавливаем правильный бэкенд для Tkinter
import matplotlib.pyplot as plt
import pandas as pd


# Функции для работы с бинарными отношениями
def build_relation_matrix(A, relation):
    """Создает матрицу бинарного отношения."""
    size = len(A)
    matrix = np.zeros((size, size), dtype=int)
    for (a, b) in relation:
        matrix[A.index(a)][A.index(b)] = 1
    return matrix


def inverse_relation(matrix):
    """Находит обратное отношение."""
    return matrix.T


def composition_relation(matrix1, matrix2):
    """Находит композицию двух бинарных отношений."""
    return np.dot(matrix1, matrix2) > 0


def union_relation(matrix1, matrix2):
    """Находит объединение двух бинарных отношений."""
    return (matrix1 | matrix2).astype(int)


def transitive_closure(matrix):
    """Вычисляет транзитивное замыкание бинарного отношения (алгоритм Уоршалла)."""
    closure = matrix.copy()
    size = matrix.shape[0]
    for k in range(size):
        for i in range(size):
            for j in range(size):
                closure[i, j] = closure[i, j] or (closure[i, k] and closure[k, j])
    return closure


def equivalence_closure(matrix):
    """Вычисляет эквивалентностное замыкание бинарного отношения."""
    size = matrix.shape[0]
    closure = matrix | np.eye(size, dtype=int)  # Рефлексивное замыкание
    return transitive_closure(closure)  # Затем транзитивное замыкание


def draw_graph(A, relation, title):
    """Рисует граф бинарного отношения."""
    G = nx.DiGraph()
    G.add_nodes_from(A)
    G.add_edges_from(relation)

    # Используем фиксированное расположение узлов для постоянного результата
    pos = nx.spring_layout(G, seed=42)  # seed фиксирует расположение
    plt.figure(figsize=(5, 5))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=14)
    plt.title(title)
    plt.show()


def submit():
    # Получаем введенные данные для бинарных отношений
    try:
        rho_values = entry_rho.get()
        sigma_values = entry_sigma.get()

        # Преобразуем строки в кортежи (например, '1,2' -> (1, 2))
        relation_rho = [tuple(map(int, pair.split(','))) for pair in rho_values.split()]
        relation_sigma = [tuple(map(int, pair.split(','))) for pair in sigma_values.split()]

        A = [1, 2, 3, 4, 5]

        # Построение матриц
        matrix_rho = build_relation_matrix(A, relation_rho)
        matrix_sigma = build_relation_matrix(A, relation_sigma)

        # Операции над отношениями
        inverse_rho = inverse_relation(matrix_rho)
        composition_rho_sigma = composition_relation(matrix_rho, matrix_sigma)
        union_rho_sigma = union_relation(matrix_rho, matrix_sigma)
        transitive_rho = transitive_closure(matrix_rho)
        equivalence_rho = equivalence_closure(matrix_rho)

        # Выводим результаты
        display_matrix("Матрица бинарного отношения ρ", matrix_rho)
        display_matrix("Обратное отношение ρ^-1", inverse_rho)
        display_matrix("Композиция ρ ∘ σ", composition_rho_sigma)
        display_matrix("Объединение ρ ∪ σ", union_rho_sigma)
        display_matrix("Транзитивное замыкание ρ", transitive_rho)
        display_matrix("Эквивалентностное замыкание ρ", equivalence_rho)

        # Визуализируем графы бинарных отношений
        draw_graph(A, relation_rho, "Граф бинарного отношения ρ")
        draw_graph(A, relation_sigma, "Граф бинарного отношения σ")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка в вводе данных: {str(e)}")


def display_matrix(title, matrix):
    df = pd.DataFrame(matrix, index=[1, 2, 3, 4, 5], columns=[1, 2, 3, 4, 5])
    print(f"{title}:\n", df)
    print("\n")


# Создаем окно приложения
root = tk.Tk()
root.title("Ввод бинарных отношений")

# Метки и поля для ввода данных
label_rho = tk.Label(root, text="Введите бинарное отношение ρ (например, '1,2 2,3 3,4'):")
label_rho.pack()

entry_rho = tk.Entry(root, width=50)
entry_rho.pack()

label_sigma = tk.Label(root, text="Введите бинарное отношение σ (например, '1,3 2,4 3,5'):")
label_sigma.pack()

entry_sigma = tk.Entry(root, width=50)
entry_sigma.pack()

# Кнопка отправки данных
submit_button = tk.Button(root, text="Выполнить", command=submit)
submit_button.pack()

# Запуск приложения
root.mainloop()
