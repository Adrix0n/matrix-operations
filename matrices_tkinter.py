from tkinter import *
from matrix import Matrix, Fraction
import copy

### To do
# Naprawić tworzenie macierzy tym drugim sposobem, aby nie usuwało '-' tam, gdzie nie trzeba
# Zapisywanie macierzy w schowku,
# Zabezpieczenie programu przed wpisaywaniem niechcianych danych.
# Dopisywanie kolumn/wierszy do macierzy
# Ogarnięcie bałaganu z przyciskami
# Usunięcie kodu ze schodkowaniem (1)
# Operacje dodawania/odejmowania/mnozenia macierzy przez liczbe/macierz w graficznej postaci
# Poprawić redukowanie krok po kroku, tworząc funkcję patrzącą czy jak od wiersza a odejmiejmy wielokrotność wiersza b
# to otrzymamy 1 na początku wiersza a (iczywiście wielokrotność w ludzkim zakresie)


matrix = Matrix(7, 5, [[0, 3, 0, 9, -3],
                       [1, 3, 2, 7, -4],
                       [4, 3, 8, 7, 3],
                       [5, 2, 10, 9, 9],
                       [6, 3, 12, 2, 2],
                       [2, 7, 1, 192, 7],
                       [13, -5, -2, 6, 3]])

matrix = Matrix(4, 5, [[0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0]
                       ,[0,0,0,0,0]])


def print_sequentially(A):
    global matrix_frame
    global label_list
    global index
    index = 0

    for i in range(A.ncol * A.nrow):
        label_list[i].config(text=A[i // A.ncol, i % A.ncol])
        label_list[i].place_forget()

    def sequence(A, index):
        if index >= A.ncol * A.nrow:
            return

        label_list[index].place(relx=1 / (A.ncol + 1) * (index % A.ncol + 1),
                                rely=1 / (A.nrow + 1) * (index // A.ncol + 1), anchor=CENTER)
        index += 1
        element.after(50, lambda: sequence(A, index))

    sequence(A, index)


def print_out(A):
    global matrix_frame
    global label_list
    # matrix_frame.destroy()
    # matrix_frame = LabelFrame(root, height=200, width=200)

    for i in range(A.ncol * A.nrow):
        # element = Label(matrix_frame, text=A[i // A.ncol, i % A.ncol])
        # element.place(relx=1 / (A.ncol + 1) * (i % A.ncol + 1), rely=1 / (A.nrow + 1) * (i // A.ncol + 1))
        label_list[i].place_forget()
        label_list[i].config(text=A[i // A.ncol, i % A.ncol])
        # label_list[i] = Label(matrix_frame, text=A[i // A.ncol, i % A.ncol])
        label_list[i].place(relx=1 / (A.ncol + 1) * (i % A.ncol + 1), rely=1 / (A.nrow + 1) * (i // A.ncol + 1),
                            anchor=CENTER)

    # matrix_frame.grid(row=0, column=1)


def row_op():
    global matrix
    return


def transpose():
    global matrix
    matrix = matrix.transpose()
    print_out(matrix)
    # print(matrix)


def reduced_row_echelon(to_print):
    global matrix
    matrix.reduced_row_echelon(to_print)
    print_out(matrix)


def row_echelon_form_2(to_print):
    global matrix
    global sign
    sign *= matrix.row_echelon_form_2(to_print)
    print_out(matrix)


def row_echelon_form():
    global matrix
    matrix.row_echelon_form()
    print_out(matrix)


def det():
    global matrix
    global sign
    result = matrix.det() * sign
    det_label.config(text=f"Determinant = {result}")


def det_Laplace():
    global matrix
    global sign
    result = matrix.det_Laplace() * sign
    det_label.config(text=f"Determinant = {result}")
    return


def invert():
    global matrix
    matrix = matrix.invert()
    print_out(matrix)
    # print(matrix)


def matrix_creator():
    global matrix
    creator_window = Toplevel(root)
    creator_window.title("Matrix creator")

    def create_entries():
        global matrix
        if ready_matrix_entry.get() == "":
            if row_label_entry.get() == "":
                creator_window.destroy()
                return
            else:
                nrow = int(row_label_entry.get())
            if column_label_entry.get() == "":
                creator_window.destroy()
                return
            else:
                ncol = int(column_label_entry.get())
            entries_list = [Entry(entries_frame, width=6) for _ in range(nrow * ncol)]
            for i in range(nrow * ncol):
                entries_list[i].place(relx=1 / (ncol + 1) * (i % ncol + 1), rely=1 / (nrow + 1) * (i // ncol + 1),
                                      anchor=CENTER)

            def generate_matrix():
                global matrix
                global label_list
                for j in range(len(label_list)):
                    label_list[j].place_forget()

                matrix_data = [0 for _ in range(nrow * ncol)]
                for k in range(len(entries_list)):
                    if entries_list[k].get() != '':
                        matrix_data[k] = Fraction.str_to_Fraction(entries_list[k].get())
                    else:
                        matrix_data[k] = 0.0

                matrix = Matrix(nrow, ncol, matrix_data)
                is_square()
                if_determinant_zero()
                label_list = [Label(matrix_frame) for _ in range(matrix.ncol * matrix.nrow)]
                print_out(matrix)
                creator_window.destroy()

            confirm_row_col_button.config(text="Create", command=generate_matrix)
        else:
            # Należy sprytnie zrozumieć zapis
            # Możliwe zapisy matrixy
            # [2,3,[2, 3, 4, 5, 4, 3]]
            # [2,3,[[2, 3 ,4],[5, 4, 3]]]
            #  2,3,[2, 3, 4, 5, 4, 3]
            #  2,3,[[2, 3 ,4],[5, 4, 3]]

            #  2 3 2 3 4 5 4 3

            #  2 3
            #  2 3 4
            #  5 4 3
            # wszystkie powyższe formaty sprowadzamy do postaci 2 3 2 3 4 5 4 3 (W K data data data...)

            #  Wiersz i kolumna podana w rubrykach powyżej a w rubryce gotowa matrix podane jedynie wartości (z przecinkiem lub bez)
            # 2 3 4
            # 5 4 3
            # Te 2 powyższe przypadki będą wymagały większych założeń

            print(ready_matrix_entry.get())
            line = str(ready_matrix_entry.get())
            # Wygląda na to, że można łatwo pozbyć się niechcianych signów jak np. a,b, zastępując je spacjami.
            # split() i tak pominie wiele spacji położonych obok siebie
            # line = line.replace('[', ' ')
            # line = line.replace(']', ' ')
            # line = line.replace(',', ' ')
            ilen = line.count('\n')
            # print(f"ilen: {ilen}")
            line = line.translate(
                {ord(c): ' ' for c in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM[];',/?{}|-=+_)(*&^%$#@!`~"})
            # print(line)
            # print(line.split())
            line = line.split()
            if len(line) < 2:
                creator_window.destroy()
                return
            nrow = int(line[0])
            ncol = int(line[1])
            line = line[2:]
            if len(line) < nrow * ncol:
                for i in range(nrow * ncol - len(line)):
                    line.append(0)

            print(nrow, ncol, line)
            entries_list = [Entry(entries_frame, width=6) for _ in range(nrow * ncol)]
            for i in range(nrow * ncol):
                entries_list[i].insert(0, line[i])
                entries_list[i].place(relx=1 / (ncol + 1) * (i % ncol + 1), rely=1 / (nrow + 1) * (i // ncol + 1),
                                      anchor=CENTER)

            def generate_matrix():
                global matrix
                global label_list
                for j in range(len(label_list)):
                    label_list[j].place_forget()

                matrix_data = [0 for _ in range(nrow * ncol)]
                for k in range(len(entries_list)):
                    if entries_list[k].get() != '':
                        matrix_data[k] = Fraction.str_to_Fraction(entries_list[k].get())
                    else:
                        matrix_data[k] = 0.0

                matrix = Matrix(nrow, ncol, matrix_data)
                is_square()
                if_determinant_zero()
                label_list = [Label(matrix_frame) for _ in range(matrix.ncol * matrix.nrow)]
                print_out(matrix)
                creator_window.destroy()

            confirm_row_col_button.config(text="Create", command=generate_matrix)

    row_label = Label(creator_window, text="Number of rows")
    row_label_entry = Entry(creator_window, width=8)
    column_label = Label(creator_window, text="Number of columns")
    column_label_entry = Entry(creator_window, width=8)
    ready_matrix = Label(creator_window, text="Paste matrix (optional)")
    ready_matrix_entry = Entry(creator_window, width=20)
    confirm_row_col_button = Button(creator_window, text="Confirm", command=create_entries)
    entries_frame = LabelFrame(creator_window, height=300, width=300)

    row_label.grid(row=0, column=0, sticky=S)
    row_label_entry.grid(row=1, column=0, sticky=N)

    column_label.grid(row=2, column=0, sticky=S)
    column_label_entry.grid(row=3, column=0, sticky=N)

    ready_matrix.grid(row=4, column=0, sticky=S)
    ready_matrix_entry.grid(row=5, column=0, sticky=N)

    confirm_row_col_button.grid(row=6, column=0, ipadx=30, ipady=0)

    entries_frame.grid(row=0, column=1, rowspan=7)


def row_operation():
    global matrix
    row_op_window = Toplevel(root)
    row_op_window.title("row operation")

    def op_row():
        if op_label_a_entry.get() == "":
            a = 0
        else:
            a = int(op_label_a_entry.get()) - 1
        if op_label_b_entry.get() == "":
            b = 0
        else:
            b = int(op_label_b_entry.get()) - 1
        if op_label_c_entry.get() == "":
            c = 0
        else:
            c = Fraction.str_to_Fraction(op_label_c_entry.get())
        if op_label_d_entry.get() == "":
            d = 0
        else:
            d = int(op_label_d_entry.get()) - 1
        matrix.row_op(a, b, c, d)
        print_out(matrix)
        row_op_window.destroy()

    def op_swap():
        if swap_label_a_entry.get() == "":
            a = 0
        else:
            a = int(swap_label_a_entry.get()) - 1
        if swap_label_b_entry.get() == "":
            b = 0
        else:
            b = int(swap_label_b_entry.get()) - 1
        matrix.row_swap(a, b)
        print_out(matrix)
        row_op_window.destroy()

    op_label = Label(row_op_window, text="row operation\n r_a = r_b +c * r_d")
    op_label_a_label = Label(row_op_window, text="a")
    op_label_a_entry = Entry(row_op_window, width=8)
    op_label_b_label = Label(row_op_window, text="b")
    op_label_b_entry = Entry(row_op_window, width=8)
    op_label_c_label = Label(row_op_window, text="c")
    op_label_c_entry = Entry(row_op_window, width=8)
    op_label_d_label = Label(row_op_window, text="d")
    op_label_d_entry = Entry(row_op_window, width=8)

    op_button = Button(row_op_window, text="Confirm", command=op_row)

    swap_label = Label(row_op_window, text="Row swap\nr_a <=> r_b")
    swap_label_a_label = Label(row_op_window, text="a")
    swap_label_a_entry = Entry(row_op_window, width=8)
    swap_label_b_label = Label(row_op_window, text="b")
    swap_label_b_entry = Entry(row_op_window, width=8)

    swap_button = Button(row_op_window, text="Confirm", command=op_swap)

    op_label.grid(row=0, column=0, columnspan=4)
    op_label_a_label.grid(row=1, column=0, padx=5)
    op_label_b_label.grid(row=1, column=1, padx=5)
    op_label_c_label.grid(row=1, column=2, padx=5)
    op_label_d_label.grid(row=1, column=3, padx=5)
    op_label_a_entry.grid(row=2, column=0, padx=5)
    op_label_b_entry.grid(row=2, column=1, padx=5)
    op_label_c_entry.grid(row=2, column=2, padx=5)
    op_label_d_entry.grid(row=2, column=3, padx=5)
    op_button.grid(row=3, column=0, columnspan=4, ipadx=20, pady=5)

    Label(row_op_window, text="").grid(row=4, column=0, columnspan=4, ipady=10)

    swap_label.grid(row=5, column=0, columnspan=4)
    swap_label_a_label.grid(row=6, column=0, columnspan=2)
    swap_label_b_label.grid(row=6, column=2, columnspan=2)
    swap_label_a_entry.grid(row=7, column=0, columnspan=2)
    swap_label_b_entry.grid(row=7, column=2, columnspan=2)
    swap_button.grid(row=8, column=0, columnspan=4, ipadx=20, pady=5)


def step_by_step_reduction(matrix):
    reduction_window = Toplevel(root)
    reduction_window.title("Step by step reduction")

    temp = copy.deepcopy(matrix)
    index_r = 0

    result = temp.reduced_row_echelon_smarter_tkinter()

    def print_out_r(A):
        for i in range(A.ncol * A.nrow):
            label_list_r[i].place_forget()
            label_list_r[i].config(text=A[i // A.ncol, i % A.ncol])
            label_list_r[i].place(relx=1 / (A.ncol + 1) * (i % A.ncol + 1), rely=1 / (A.nrow + 1) * (i // A.ncol + 1),
                                  anchor=CENTER)

    def next(index_r):

        if index_r >= 0:
            previous_btn.config(state=NORMAL)
        index_r += 1
        print_out_r(Matrix(temp.nrow, temp.ncol, result[index_r][0]))
        if index_r + 1 <= len(result) - 1:
            operations.config(text=result[index_r + 1][1])
        else:
            operations.config(text="END")

        if index_r >= len(result) - 1:
            next_btn.config(state=DISABLED)

        next_btn.config(command=lambda: next(index_r))
        previous_btn.config(command=lambda: previous(index_r))

    def previous(index_r):
        if index_r == len(result) - 1:
            next_btn.config(state=NORMAL)
        index_r -= 1
        print_out_r(Matrix(temp.nrow, temp.ncol, result[index_r][0]))
        operations.config(text=result[index_r + 1][1])

        if index_r <= 0:
            previous_btn.config(state=DISABLED)

        next_btn.config(command=lambda: next(index_r))
        previous_btn.config(command=lambda: previous(index_r))

    matrix_frame_r = LabelFrame(reduction_window, height=200, width=200)
    label_list_r = [Label(matrix_frame_r) for _ in range(temp.ncol * temp.nrow)]

    operations = Label(reduction_window, text=result[1][1])
    operations.grid(row=0, column=1, ipadx=60)

    matrix_frame_r.grid(row=0, column=0)
    print_out_r(Matrix(temp.nrow, temp.ncol, result[0][0]))
    next_btn = Button(reduction_window, text=">>", command=lambda: next(index_r))
    previous_btn = Button(reduction_window, text="<<", command=lambda: previous(index_r), state=DISABLED)
    next_btn.grid(row=1, column=1, sticky=W + E)
    previous_btn.grid(row=1, column=0, sticky=W + E)


def edit_matrix():
    global matrix
    global label_list
    edit_window = Toplevel(root)
    edit_window.title("Edit matrix")

    entries_frame = LabelFrame(edit_window, height=300, width=300)

    nrow = matrix.nrow
    ncol = matrix.ncol
    entries_list = [Entry(entries_frame, width=6) for _ in range(nrow * ncol)]

    for i in range(nrow * ncol):
        entries_list[i].insert(0, matrix[i // ncol, i % ncol])
        entries_list[i].place(relx=1 / (ncol + 1) * (i % ncol + 1), rely=1 / (nrow + 1) * (i // ncol + 1),
                              anchor=CENTER)

    def generate_matrix():
        global matrix
        global label_list
        for j in range(len(label_list)):
            label_list[j].place_forget()

        matrix_data = [0 for _ in range(nrow * ncol)]
        for k in range(len(entries_list)):
            if entries_list[k].get() != '':
                matrix_data[k] = Fraction.str_to_Fraction(entries_list[k].get())
            else:
                matrix_data[k] = 0.0

        matrix = Matrix(nrow, ncol, matrix_data)
        is_square()
        if_determinant_zero()
        label_list = [Label(matrix_frame) for _ in range(matrix.ncol * matrix.nrow)]
        print_out(matrix)
        edit_window.destroy()

    confirm_button = Button(edit_window, text="Confirm", command=generate_matrix)
    cancel_button = Button(edit_window, text="Cancel", command=edit_window.destroy)

    entries_frame.grid(row=0, column=0, columnspan=2)
    confirm_button.grid(row=1, column=1)
    cancel_button.grid(row=1, column=0)


def invert_step_by_step(matrix):
    temp = Matrix(matrix.nrow, matrix.ncol * 2, 0)
    for row in range(matrix.nrow):
        for col in range(matrix.ncol):
            temp[row, col] = matrix[row, col]
    for j in range(temp.ncol // 2):
        temp[j, j + temp.ncol // 2] = 1
    step_by_step_reduction(temp)


root = Tk()
root.title("Matrix")

matrix_frame = LabelFrame(root, height=200, width=200)
label_list = [Label(matrix_frame) for _ in range(matrix.ncol * matrix.nrow)]
index = 0
element = Label(matrix_frame)
print_out(matrix)

# print(matrix)
buttons_frame = LabelFrame(root, height=200, width=290)

determinant = matrix.det()
sign = 1
det_label = Label(buttons_frame, text=f"Determinant = {determinant}")
det_label.grid(row=10, column=0, columnspan=2, sticky=W)

row_op_button = Button(buttons_frame, text="row operation", command=row_operation)
transpose_button = Button(buttons_frame, text="Transpose", command=transpose)
red_row_echelon_button = Button(buttons_frame, text="Red. row echelon form",
                                command=lambda: reduced_row_echelon(0))
row_echelon_form_2_button = Button(buttons_frame, text="Row ech.f.2", command=lambda: row_echelon_form_2(0))
row_echelon_form_button = Button(buttons_frame, text="Row ech.f.", command=row_echelon_form)
det_button = Button(buttons_frame, text="Determinant", command=det)
det_Laplace_button = Button(buttons_frame, text="Determinant Laplace's met.", command=det_Laplace)
invert_button = Button(buttons_frame, text="Invert", command=invert)
matrix_creator_button = Button(buttons_frame, text="Create matrix", command=matrix_creator)
edit_matrix_button = Button(buttons_frame, text="Edit matrix", command=edit_matrix)


def is_square():
    global matrix
    if matrix.ncol != matrix.nrow:
        invert_button.config(state=DISABLED)
        det_button.config(state=DISABLED)
        det_Laplace_button.config(state=DISABLED)
        invert_step_by_step_button.config(state=DISABLED)
    else:
        invert_button.config(state=NORMAL)
        det_button.config(state=NORMAL)
        det_Laplace_button.config(state=NORMAL)
        invert_step_by_step_button.config(state=NORMAL)


def if_determinant_zero():
    global matrix
    if matrix.det() == 0:
        invert_button.config(state=DISABLED)
        invert_step_by_step_button.config(state=DISABLED)
        row_echelon_form_2_button.config(state=DISABLED)
    else:
        invert_button.config(state=NORMAL)
        invert_step_by_step_button.config(state=NORMAL)
        row_echelon_form_2_button.config(state=NORMAL)


print_sequentially_button = Button(buttons_frame, text="Print out sequentially",
                                   command=lambda: print_sequentially(matrix))
invert_step_by_step_button = Button(buttons_frame, text="Invert step by step",
                                    command=lambda: invert_step_by_step(matrix))

step_by_step_reduction_button = Button(buttons_frame, text="Reduce step by step",
                                       command=lambda: step_by_step_reduction(matrix))
step_by_step_reduction_button.grid(row=5, column=0, sticky=W + E)

is_square()

print_sequentially_button.grid(row=4, column=0, sticky=W + E)
matrix_creator_button.grid(row=4, column=1, sticky=W + E)

row_op_button.grid(row=0, column=0, sticky=W + E)
transpose_button.grid(row=0, column=1, sticky=W + E)

red_row_echelon_button.grid(row=1, column=0, sticky=W + E)
row_echelon_form_2_button.grid(row=1, column=1, sticky=W + E)
# row_echelon_form_button.grid(row=1, column=1, sticky=W + E)

invert_button.grid(row=2, column=1, sticky=W + E)
invert_step_by_step_button.grid(row=2, column=0, sticky=W + E)

det_button.grid(row=3, column=0, sticky=W + E)
det_Laplace_button.grid(row=3, column=1, sticky=W + E)

edit_matrix_button.grid(row=5, column=1, sticky=W + E)

buttons_frame.grid_propagate(0)
matrix_frame.grid(row=0, column=1)
buttons_frame.grid(row=0, column=0)
root.mainloop()
