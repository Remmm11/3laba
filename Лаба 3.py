"""
С клавиатуры вводятся два числа K и N. Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц,
B, C, D, E заполняется случайным образом целыми числами в интервале [-10,10]. Для тестирования использовать не случайное
заполнение, а целенаправленное.
Вид матрицы А:
D	Е
С	В
Каждая из матриц B, C, D, E имеет вид:
     4
  3     1
     2
Вариант 13:
Формируется матрица F следующим образом: если в "С" количество четных чисел в нечетных столбцах в области 1 больше,
чем сумма чисел в нечетных строках в области 4, то поменять в Е симметрично области 1 и 4 местами, иначе В и Е
поменять местами несимметрично. При этом матрица А не меняется. После чего вычисляется выражение: A * А – K * AT.
Выводятся по мере формирования А, F и все матричные операции последовательно."""

from math import ceil
import random as r


def print_matrix(matrix):  # Функция вывода матрицы
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("{:5d}".format(matrix[i][j]), end="")
        print()


try:
    n = int(input('N: '))
    k = int(input('K: '))
    while n < 5:
        n = int(input('Введите число N больше 4: '))

    cnt_ch1 = sum_nchstr4 = 0
    middle_n = ceil(n / 2)  # Середина матрицы
    A = [[r.randint(-10, 10) for i in range(n)] for j in range(n)]  # Задаём матрицу A
    AT = [[0 for i in range(n)] for j in range(n)]  # Заготовка под транспонированную матрицу А
    F = A.copy()  # Задаём матрицу F
    AA = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат умножения матрицы A на матрицу А
    KAT = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат умножения матрицы AT на коэффициент K
    result = [[0 for i in range(n)] for j in range(n)]  # Заготовка под результат вычитания двух матриц

    for i in range(n):  # Транспонируем матрицу А
        for j in range(n):
            AT[i][j] = A[j][i]

    print('\nМатрица А:')
    print_matrix(A)
    print('\nТранспонированная А:')
    print_matrix(AT)

    # Выделяем матрицы E C B
    if n % 2 == 1:
        E = [A[i][middle_n - 1:n] for i in range(middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n - 1, n)]
        B = [A[i][middle_n - 1:n] for i in range(middle_n - 1, n)]
    else:
        E = [A[i][middle_n:n] for i in range(0, middle_n)]
        C = [A[i][0:middle_n] for i in range(middle_n, n)]
        B = [A[i][middle_n:n] for i in range(middle_n, n)]

    for i in range(middle_n):  # Считаем в 1 области в нечётных столбцах в матрице С кол-во чётных значений
        for j in range(middle_n):
            if (i + j + 1) >= middle_n and (i <= j) and ((j + 1) % 2 == 1):
                if C[i][j] % 2 == 0:
                    cnt_ch1 += 1

    for i in range(middle_n):  # Считаем сумму чисел в зоне 4 в нечётных строках в матрице С
        for j in range(middle_n):
            if (i <= j) and ((i + j + 1) <= middle_n) and ((i + 1) % 2 == 1):
                sum_nchstr4 += C[i][j]

    if cnt_ch1 > sum_nchstr4:
        print(f'\nВ матрице "С" количество четных чисел в нечетных столбцах в области 1({cnt_ch1})')
        print(f'больше чем сумма чисел в нечётных строках в области 4({sum_nchstr4})')
        print('поэтому симметрично меняем местами области 1 и 4 в Е.')
        for i in range((ceil(middle_n / 2))):
            for j in range(middle_n - i):
                if i <= j:
                    E[i][j], E[(middle_n - j) - 1][(middle_n - i) - 1] = E[(middle_n - j) - 1][(middle_n - i) - 1], E[i][j]  # Симметрично меняем местами области 1 и 4 в Е

        if n % 2 == 1:
            for i in range(middle_n):
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]
    else:
        print(f'\nВ матрице "С" количество четных чисел в нечетных столбцах в области 1({cnt_ch1})')
        print(f'меньше чем сумма чисел в нечётных строках в области 4({sum_nchstr4}) или равно ей')
        print('поэтому несимметрично меняем местами области B и E:')
        B, E = E, B  # Меняем значениями B и E
        if n % 2 == 1:
            for i in range(middle_n - 1, n):
                for j in range(middle_n - 1, n):
                    F[i][j] = B[i - (middle_n - 1)][j - (middle_n - 1)]  # Перезаписываем B
            for i in range(middle_n):  # Перезаписываем Е
                for j in range(middle_n - 1, n):
                    F[i][j] = E[i][j - (middle_n - 1)]
        else:
            for i in range(middle_n, n):
                for j in range(middle_n, n):
                    F[i][j] = B[i - middle_n][j - middle_n]  # Перезаписываем B
            for i in range(middle_n):
                for j in range(middle_n, n):
                    F[i][j] = E[i][j - middle_n]  # Перезаписываем E
    print('\nМатрица F:')
    print_matrix(F)

    # K * AT
    for i in range(n):
        for j in range(n):
            KAT[i][j] = k * AT[i][j]  # Производим умножение матрицы KAT на коэффициент
    print('\nРезультат K * AT:')
    print_matrix(KAT)

    # A * A
    for i in range(n):
        for j in range(n):
            for m in range(n):
                AA[i][j] += A[i][m] * A[m][j]  # Производим умножение матрицы A на матрицу A
    print('\nРезультат A * А:')
    print_matrix(AA)

    # AA - KAT
    for i in range(n):
        for j in range(n):
            result[i][j] = AA[i][j] - KAT[i][j]  # Вычисляем разность двух матриц
    print('\nРезультат A * А – K * AT:')
    print_matrix(result)

except ValueError:  # ошибка на случай введения не числа в качестве порядка или коэффициента
    print('\nВведенный символ не является числом. Перезапустите программу и введите число.')
