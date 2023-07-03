import math
import random
import copy
import time


class Fraction:
    __slots__ = ["numerator", "denominator"]

    def __init__(self, numerator, denominator):
        if type(numerator) is Fraction:
            denominator *= numerator.denominator
            numerator = numerator.numerator
        if type(denominator) is Fraction:
            numerator *= denominator.denominator
            denominator = denominator.numerator
        if type(numerator) is int and type(denominator) is int:
            gcd = math.gcd(numerator, denominator)
            sign = -1 if (numerator < 0 < denominator) or (numerator > 0 > denominator) else 1
            self.numerator = int(sign * abs(numerator) / gcd)
            self.denominator = int(abs(denominator) / gcd)

    def __repr__(self):
        if self.denominator == 1:
            return f"{self.numerator}"
        else:
            return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return float(self.numerator / self.denominator) == float(other)
        if isinstance(other, Fraction):
            return (self.numerator == other.numerator and self.denominator == other.denominator)
        return False

    def __lt__(self, other):
        if isinstance(other, (int, float)):
            return self.numerator < other * self.denominator
        elif isinstance(other, Fraction):
            return self.numerator * other.denominator < other.numerator * self.denominator
        else:
            return False

    def __le__(self, other):
        if isinstance(other, (int, float)):
            return self.numerator <= other * self.denominator
        elif isinstance(other, Fraction):
            return self.numerator * other.denominator <= other.numerator * self.denominator
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return self.numerator > other * self.denominator
        elif isinstance(other, Fraction):
            return self.numerator * other.denominator > other.numerator * self.denominator
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, (int, float)):
            return self.numerator >= other * self.denominator
        elif isinstance(other, Fraction):
            return self.numerator * other.denominator >= other.numerator * self.denominator
        else:
            return False

    @staticmethod
    def float_to_Fraction(x):
        for i in range(10):
            if math.floor(x * 10 ** i) == x * 10 ** i:
                x = Fraction(int(x * 10 ** i), 10 ** i)
                break
            if i == 9:
                raise AttributeError("Invalid float")
        return x

    def __mul__(self, other):
        if type(other) is float:  # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
        if type(other) is int:
            return Fraction(other * self.numerator, self.denominator)
        elif type(other) is Fraction:
            return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)
        else:
            raise ValueError("Zle dane")

    def __rmul__(self, other):
        return self * other

    def __add__(self, other):
        if type(other) is float:  # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
        if type(other) is int:
            return Fraction(self.numerator + self.denominator * other, self.denominator)
        elif type(other) is Fraction:
            return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)
        else:
            raise ValueError("Zle data")

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) is float:  # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
        if type(other) is int:
            return Fraction(self.numerator - self.denominator * other, self.denominator)
        elif type(other) is Fraction:
            return Fraction(self.numerator * other.denominator - other.numerator * self.denominator,
                            self.denominator * other.denominator)
        else:
            raise ValueError("Zle data")

    def __rsub__(self, other):
        if type(other) is float:  # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
            return other - self
        if type(other) is int:
            return Fraction(other * self.denominator - self.numerator, self.denominator)
        else:
            raise ValueError("Zle data")

    def __truediv__(self, other):
        if type(other) is float:  # # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
        if type(other) is int and other != 0:
            return Fraction(self.numerator, self.denominator * other)
        elif type(other) is Fraction:
            return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)
        else:
            raise ValueError("Zle data")

    def __rtruediv__(self, other):
        if type(other) is float:  # # Checks, if other is float and if it is possible to convert it to Fraction
            other = self.float_to_Fraction(other)
            return other / self
        if type(other) is int and self.numerator != 0:
            return Fraction(other * self.denominator, self.numerator)
        else:
            raise ValueError("Zle data")

    def __float__(self):
        return self.numerator / self.denominator

    def __int__(self):
        if self.denominator == 1:
            return self.numerator
        else:
            raise ValueError("Fraction cannot be converted to Int")

    @staticmethod
    def str_to_Fraction(x):
        slash_index = x.find("/")
        if slash_index == -1:
            return float(x)
        fnumerator = int(x[:slash_index])
        fdenominator = int(x[slash_index + 1:])
        return Fraction(fnumerator, fdenominator)


class Matrix:
    __slots__ = ["nrow", "ncol", "__data", "__shape"]

    def __init__(self, nrow, ncol, data):
        self.nrow = nrow
        self.ncol = ncol
        self.__shape = [nrow, ncol]
        if type(data) is float or type(data) is int:
            self.__data = [Fraction(data, 1) for _ in range(nrow * ncol)]
        elif type(data) is list:
            if type(data[0]) is list:
                self.__data = [Fraction(0, 1)] * (nrow * ncol)
                for row in range(nrow):
                    for col in range(ncol):
                        self.__data[row * ncol + col] += data[row][col]
            else:
                self.__data = [Fraction(0, 1)] * (nrow * ncol)
                for i in range(min(len(data), nrow * ncol)):
                    self.__data[i] += data[i]

    def __repr__(self):
        result = "Matrix(["
        for row in range(self.nrow):
            result += "\n        "
            result += "["
            for col in range(self.ncol):
                result += str(self.__data[row * self.ncol + col])
                if col < self.ncol - 1:
                    result += ", "
            result += "]"
            if row < self.nrow - 1:
                result += ", "
        result += "])"
        return result

    def row_op(self, a, b, c, d):  # a = b + c * d, where a, b, d  are row numbers (counting from 0)
        assert type(a) is int and type(b) is int and type(d) is int
        if (a >= self.nrow) or (b >= self.nrow) or (d >= self.nrow):
            raise ValueError("Zle data!")
        for i in range(self.ncol):
            self.__data[self.ncol * a + i] = self.__data[self.ncol * b + i] + c * self.__data[self.ncol * d + i]

    def row_swap(self, row1, row2):
        buffer = [0 for _ in range(self.ncol)]
        for j in range(self.ncol):
            buffer[j] = self.__data[row1 * self.ncol + j]
        self.row_op(row1, row2, 0, 0)
        for k in range(self.ncol):
            self.__data[row2 * self.ncol + k] = buffer[k]

    def __add__(self, other):
        suma = Matrix(self.nrow, self.ncol, 0)
        if (type(other) is int) or (type(other) is float):
            for i in range(self.nrow * self.ncol):
                suma.__data[i] = self.__data[i] + other
        else:
            if self.__shape != other.__shape:
                raise ValueError("invalid data")
            for i in range(self.nrow * self.ncol):
                suma.__data[i] = self.__data[i] + other.__data[i]
        return suma

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        product = Matrix(self.nrow, self.ncol, 0)
        if (type(other) is int) or (type(other) is float):
            for i in range(self.nrow * self.ncol):
                product.__data[i] = self.__data[i] * other
        else:
            if self.__shape != other.__shape:
                raise ValueError("invalid data")
            for i in range(self.nrow * self.ncol):
                product.__data[i] = self.__data[i] * other.__data[i]
        return product

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        if self.ncol != other.nrow:
            raise ValueError("Invalid data")
        result = Matrix(self.nrow, other.ncol, 0)
        for i in range(self.nrow * other.ncol):
            for j in range(other.nrow):
                result.__data[i] += other.__data[j * other.ncol + (i % other.ncol)] * self.__data[
                    (i // other.ncol) * self.ncol + j]
        return result

    def __getitem__(self, item):
        return self.__data[item[0] * self.ncol + item[1]]

    def __setitem__(self, key, value):
        self.__data[key[0] * self.ncol + key[1]] = value

    def transpose(self):
        result = Matrix(self.ncol, self.nrow, 0)
        for row in range(self.ncol):
            for col in range(self.nrow):
                result.__data[row * self.nrow + col] = self.__data[col * self.ncol + row]
        return result

    def reduced_row_echelon(self, to_print):
        if to_print != 1:
            to_print = 0

        x = min(self.nrow, self.ncol)  # To avoid going out of matrix
        for col in range(x):  # We compute diagonally, so row = col
            row = col
            curr_cell = self.__data[row * self.ncol + col]
            while curr_cell == 0 and row + 1 < self.nrow:  # Looking for non-zero value in column 'col'...
                row += 1
                curr_cell = self.__data[row * self.ncol + col]
            if float(curr_cell) == 0.0:  # ... if whole column has zeros
                continue
            if row != col:  # case, when cell a[col][col] is zero
                self.row_op(col, col, 1,
                            row)   # Adding row 'row' to row 'col' (with zero value cell) to change value in a[col][col]
            self.row_op(col, col, Fraction(1, curr_cell) - 1,
                        col)  # Transforming row 'col' to  0,..., 0, 1,...
            if to_print == 1:
                print(f"r{col + 1} = r{col + 1} / a{col + 1}{col + 1}")  # printing
                print(self)  # printing

            # print(Fraction(1, curr_cell) - 1)
            for p in range(
                    self.nrow):  # We replace other cells in column to 0 with simple row operations
                if p == col:  # skip row, which is currently use in row operations
                    continue
                curr_cell = self.__data[p * self.ncol + col]
                self.row_op(p, p, Fraction(curr_cell, -1), col)
                if to_print == 1:
                    print(f"r{p + 1} = r{p + 1} + {curr_cell * -1} * r{col + 1}")  # printing
                    print(self)  # printing

    def reduced_row_echelon_smarter(self):
        # To avoid getting out of matrix
        x = min(self.nrow, self.ncol)

        ### We will reduce the matrix to the upper triangular echelon form
        for col in range(x):
            if_only_zeros = True
            # We create a list containing all the elements of the 'col' column
            col_elements = [0 for _ in range(self.nrow)]
            for i in range(self.nrow):
                col_elements[i] = self.__data[i * self.ncol + col]
                if float(col_elements[i]) != 0.0:
                    if_only_zeros = False
            if if_only_zeros:
                continue

            ## We arrange the rows so that the zeros are always at the bottom in the matrix
            def arrange_rows(self):
                product_of_col_elems = 1
                for i in range(len(col_elements)):
                    product_of_col_elems *= col_elements[i]

                # We check if there is 0 in the column (We are not interested in the elements in the finished rows)
                print("Moving zero rows to bottom...")
                if float(product_of_col_elems) == 0.0:
                    row_operations_list = []
                    # We go through the elements of the column, skipping the finished rows (hence the range() starting with col)
                    # We will look for the zero element
                    for j in range(col, len(col_elements)):
                        last_index = len(col_elements) - 1

                        if float(col_elements[j]) == 0:
                            # We now go from the end of the list of elements to the zero element without considering itself
                            # We will look for a non-zero element
                            for k in range(last_index, j, -1):

                                # If we find such an element, we swap the places of the zero element with this element
                                # and write down what rows should be replaced with each other
                                if float(col_elements[k]) != 0:
                                    row_operations_list.append((j, k))
                                    col_elements[j], col_elements[k] = col_elements[k], col_elements[j]
                                    break
                    print(f"Column: {col}, list of row operations: {row_operations_list}")

                    # We swap rows with each other using a list that tells us which rows to replace
                    for l in range(len(row_operations_list)):
                        self.row_swap(row_operations_list[l][0], row_operations_list[l][1])
                print(col_elements)
                print(self)

            ## We check if we can do some row operations cleverly and we do them
            # We check to see if there is a 1 or -1 at the beginning of a row and place that row as high as possible
            def find_one(self):

                print("Looking for 1, -1 and fraction with numerator = 1...")
                for d in range(col, len(col_elements)):
                    if float(col_elements[d]) == 1.0 or float(col_elements[d]) == -1.0:
                        if float(col_elements[d]) == 1.0:
                            self.row_swap(d, col)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                        if float(col_elements[d]) == -1.0:
                            self.row_swap(d, col)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                            self.row_op(col, col, -2, col)
                            col_elements[col] *= -1
                        break
                    if type(col_elements[d]) is Fraction:
                        if col_elements[d].numerator == 1 or col_elements[d].numerator == -1:
                            self.row_op(d, d, col_elements[d].denominator - 1, d)
                            col_elements[d] *= col_elements[d].denominator
                            if col_elements[d].numerator == -1:
                                self.row_op(d, d, -2, d)
                                col_elements[d] *= -1
                            self.row_swap(col, d)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                            break

                print(col_elements)
                print(self)

            # We check if the elements of the column are repeated:
            def find_equal_values(self):
                print("Looking for equal values...")
                for b in range(col, len(col_elements)):
                    for c in range(b + 1, len(col_elements)):
                        if col_elements[b] == col_elements[c]:
                            self.row_op(c, c, -1, b)
                            col_elements[c] *= 0

                        if col_elements[b] == -1 * col_elements[c]:
                            self.row_op(c, c, 1, b)
                            col_elements[c] *= 0

                print(col_elements)
                print(self)

            # We check if one element of the column is a multiple of another
            def find_multiples(self):
                print("Looking for multiples...")
                for d in range(col, len(col_elements)):
                    for g in range(d + 1, len(col_elements)):
                        if type(col_elements[d]) is not Fraction or type(col_elements[g]) is not Fraction:
                            continue
                        if col_elements[d].denominator == col_elements[g].denominator and col_elements[
                            d].numerator != 0 and col_elements[g].numerator != 0:
                            sign = -1 if (col_elements[d] * col_elements[g]) < 0 else 1
                            if abs(col_elements[d].numerator) > abs(col_elements[g].numerator):
                                if col_elements[d].numerator // col_elements[g].numerator == col_elements[
                                    d].numerator / col_elements[g].numerator:
                                    # print(d,g)
                                    self.row_op(d, d, -1 * col_elements[d].numerator / col_elements[g].numerator,
                                                g)
                                    col_elements[d] *= 0
                            else:
                                if col_elements[g].numerator // col_elements[d].numerator == col_elements[
                                    g].numerator / col_elements[d].numerator:
                                    # print(d,g)
                                    self.row_op(g, g, -1 * col_elements[g].numerator / col_elements[d].numerator,
                                                d)
                                    col_elements[g] *= 0
                print(col_elements)
                print(self)

            # We zero with row operations
            def zero_with_row_op(self):
                print("Zero with row operations...")
                if float(col_elements[col]) == 1.0:
                    for f in range(col + 1, len(col_elements)):
                        try:
                            self.row_op(f, f, int(-1 * col_elements[f]), col)
                            col_elements[f] *= 0
                        except:
                            if type(col_elements[f]) is Fraction:
                                self.row_op(f, f, col_elements[f].denominator - 1, f)
                                col_elements[f] *= col_elements[f].denominator
                                self.row_op(f, f, int(-1 * col_elements[f]), col)
                                col_elements[f] *= 0
                print(col_elements)
                print(self)

            # We reduce one of the elements of the column to 1
            def reduce_to_one(self):
                print("Reducing to one...")
                minimum = 0
                index = col
                for j in range(col, len(col_elements)):
                    if float(col_elements[j]) != 0.0:
                        minimum = col_elements[j]
                        break

                if float(minimum) == 0.0:
                    return

                for k in range(col, len(col_elements)):
                    if abs(float(minimum)) >= abs(float(col_elements[k])) and float(col_elements[k]) != 0.0:
                        minimum = col_elements[k]
                        index = k

                self.row_op(index, index, (Fraction(1, col_elements[index]) - 1), index)
                col_elements[index] *= Fraction(1, col_elements[index])

                print(col_elements)
                print(self)

            arrange_rows(self)
            find_one(self)
            find_equal_values(self)
            find_multiples(self)
            zero_with_row_op(self)

            reduce_to_one(self)

            find_one(self)
            arrange_rows(self)
            find_multiples(self)
            zero_with_row_op(self)
            arrange_rows(self)

        ### Now we go from the right and zero the above column elements
        for col in range(x - 1, -1, -1):
            # We create a list containing all the elements of the 'col' column
            col_elements = [0 for _ in range(self.nrow)]
            for i in range(self.nrow):
                col_elements[i] = self.__data[i * self.ncol + col]
            # print(f"Column elements: {col_elements}")

            # print(col_elements)
            for k in range(col - 1, -1, -1):
                self.row_op(k, k, -1 * col_elements[k], col)
                col_elements[k] *= 0

            print(col_elements)

            print()

        return

    def reduced_row_echelon_smarter_tkinter(self):
        result = []
        result.append([copy.copy(self.__data), ""])

        # We are going diagonally, so it is important not to go beyond both the columns and the rows of the matrix
        x = min(self.nrow, self.ncol)

        ### We will reduce the matrix to the upper triangular echelon form
        for col in range(x):
            if_only_zeros = True
            # We create a list containing all the elements of the 'col' column
            col_elements = [0 for _ in range(self.nrow)]
            for i in range(self.nrow):
                col_elements[i] = self.__data[i * self.ncol + col]
                if float(col_elements[i]) != 0.0:
                    if_only_zeros = False
            if if_only_zeros:
                continue

            # print(f"Column elements: {col_elements}")

            ## We arrange the rows so that the zeros are always at the bottom in the matrix
            def arrange_rows(self):
                operations_list = ""

                product_of_col_elems = 1
                for i in range(len(col_elements)):
                    product_of_col_elems *= col_elements[i]

                # We check if there is 0 in the column (We are not interested in the elements in the finished rows)
                if float(product_of_col_elems) == 0.0:
                    row_operations_list = []
                    # We go through the elements of the column, skipping the finished rows (hence the range() starting with col)
                    # We will look for the zero element
                    for j in range(col, len(col_elements)):
                        last_index = len(col_elements) - 1

                        if float(col_elements[j]) == 0:
                            # We now go from the end of the list of elements to the zero element without considering itself
                            # We will look for a non-zero element
                            for k in range(last_index, j, -1):
                                # If we find such an element, we swap the places of the zero element with this element
                                # and write down what rows should be replaced with each other
                                if float(col_elements[k]) != 0:
                                    row_operations_list.append((j, k))
                                    if j != k:
                                        operations_list += f"r_{j + 1} <=> r_{k + 1}\n"
                                    col_elements[j], col_elements[k] = col_elements[k], col_elements[j]
                                    break

                    # print(f"Column: {col}, list of row operations: {row_operations_list}")

                    # We swap rows with each other using a list that tells us which rows to replace
                    for l in range(len(row_operations_list)):
                        self.row_swap(row_operations_list[l][0], row_operations_list[l][1])

                    if len(row_operations_list) != 0:
                        result.append([copy.copy(self.__data), operations_list])

                # print(col_elements)
                # print(self)

            ## We check if we can do some row operations cleverly and we do them
            # We check to see if there is a 1 or -1 at the beginning of a row and place that row as high as possible
            def find_one(self):
                operations_list = ""


                for d in range(col, len(col_elements)):
                    if float(col_elements[d]) == 1.0 or float(col_elements[d]) == -1.0:
                        if float(col_elements[d]) == 1.0:
                            self.row_swap(d, col)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                            if d != col:
                                operations_list += f"r_{d + 1} <=> r_{col + 1} \n"
                        if float(col_elements[d]) == -1.0:
                            self.row_swap(d, col)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                            if d != col:
                                operations_list += f"r_{d + 1} <=> r_{col + 1} \n"
                            self.row_op(col, col, -2, col)
                            col_elements[col] *= -1
                            operations_list += f"r_{col + 1} = -1 * r_{col + 1} \n"
                        break
                    if type(col_elements[d]) is Fraction:
                        if col_elements[d].numerator == 1 or col_elements[d].numerator == -1:
                            self.row_op(d, d, col_elements[d].denominator - 1, d)
                            if col_elements[d].denominator != 1:
                                operations_list += f"r_{d + 1} = {col_elements[d].denominator} * r_{d + 1} \n"
                            col_elements[d] *= col_elements[d].denominator

                            if col_elements[d].numerator == -1:
                                self.row_op(d, d, -2, d)
                                col_elements[d] *= -1
                                operations_list += f"r_{d + 1} = -1 * r_{d + 1} \n"
                            self.row_swap(col, d)
                            col_elements[d], col_elements[col] = col_elements[col], col_elements[d]
                            if d != col:
                                operations_list += f"r_{d + 1} <=> r_{col + 1} \n"
                            break

                if operations_list != "":
                    result.append([copy.copy(self.__data), operations_list])

                # (col_elements)
                # print(self)

            # We check if the elements of the column are repeated:
            def find_equal_values(self):
                operations_list = ""

                for b in range(col, len(col_elements)):
                    for c in range(b + 1, len(col_elements)):
                        if col_elements[b] == col_elements[c] and float(col_elements[b]) * float(
                                col_elements[c]) != 0:
                            self.row_op(c, c, -1, b)

                            operations_list += f"r_{c + 1} = r_{c + 1} - r_{b + 1}\n"

                            col_elements[c] *= 0


                        elif col_elements[b] == -1 * col_elements[c] and float(col_elements[b]) * float(
                                col_elements[c]) != 0:
                            self.row_op(c, c, 1, b)

                            operations_list += f"r_{c + 1} = r_{c + 1} + r_{b + 1}\n"

                            col_elements[c] *= 0

                if operations_list != "":
                    result.append([copy.copy(self.__data), operations_list])

                # print(col_elements)
                # print(self)

            # We check if one element of the column is a multiple of another
            def find_multiples(self):
                operations_list = ""

                for d in range(col, len(col_elements)):
                    for g in range(d + 1, len(col_elements)):
                        if type(col_elements[d]) is not Fraction or type(col_elements[g]) is not Fraction:
                            continue
                        if col_elements[d].denominator == col_elements[g].denominator and col_elements[
                            d].numerator != 0 and col_elements[g].numerator != 0:
                            # sign = -1 if (col_elements[d] * col_elements[g]) < 0 else 1
                            if abs(col_elements[d].numerator) > abs(col_elements[g].numerator):
                                if col_elements[d].numerator // col_elements[g].numerator == col_elements[
                                    d].numerator / col_elements[g].numerator:
                                    # print(d,g)
                                    self.row_op(d, d, -1 * col_elements[d].numerator / col_elements[g].numerator,
                                                g)

                                    if d != g and float(col_elements[d]) != 0.0:
                                        operations_list += f"r_{d + 1} = r_{d + 1} + {-1 * col_elements[d].numerator / col_elements[g].numerator} * r_{g + 1}\n"

                                    col_elements[d] *= 0
                            else:
                                if col_elements[g].numerator // col_elements[d].numerator == col_elements[
                                    g].numerator / col_elements[d].numerator:
                                    # print(d,g)
                                    self.row_op(g, g, -1 * col_elements[g].numerator / col_elements[d].numerator,
                                                d)

                                    if d != g and float(col_elements[g]) != 0.0:
                                        operations_list += f"r_{g + 1} = r_{g + 1} + {-1 * col_elements[g].numerator / col_elements[d].numerator} * r_{d + 1}\n"

                                    col_elements[g] *= 0

                if operations_list != "":
                    result.append([copy.copy(self.__data), operations_list])

                # (col_elements)
                # print(self)

            # We zero with row operations
            def zero_with_row_op(self):
                operations_list = ""

                if float(col_elements[col]) == 1.0:
                    for f in range(col + 1, len(col_elements)):
                        try:
                            self.row_op(f, f, int(-1 * col_elements[f]), col)
                            if f != col and float(col_elements[f]) != 0.0:
                                operations_list += f"r_{f + 1} = r_{f + 1} +{int(-1 * col_elements[f])} * r_{col + 1}\n"
                            col_elements[f] *= 0
                        except:
                            if type(col_elements[f]) is Fraction:
                                self.row_op(f, f, col_elements[f].denominator - 1, f)

                                if float(col_elements[f].denominator) != 0.0:
                                    operations_list += f"r_{f + 1} = {col_elements[f].denominator} * r_{f + 1}\n"

                                col_elements[f] *= col_elements[f].denominator
                                self.row_op(f, f, int(-1 * col_elements[f]), col)

                                if float(col_elements[f]) != 0.0:
                                    operations_list += f"r_{f + 1} = r_{f + 1} +{int(-1 * col_elements[f])} * r_{col + 1}\n"

                                col_elements[f] *= 0

                if operations_list != "":
                    result.append([copy.copy(self.__data), operations_list])
                # print(col_elements)
                # print(self)

            # We reduce one of the elements of the column to 1
            def reduce_to_one(self):
                operations_list = ""

                minimum = 0
                index = col
                for j in range(col, len(col_elements)):
                    if float(col_elements[j]) != 0.0:
                        minimum = col_elements[j]
                        break

                if float(minimum) == 0.0:
                    return

                for n in range(col, len(col_elements)):
                    if abs(float(minimum)) >= abs(float(col_elements[n])) and float(col_elements[n]) != 0.0:
                        minimum = col_elements[n]
                        index = n

                self.row_op(index, index, (Fraction(1, col_elements[index]) - 1), index)

                if float(col_elements[index]) != 1.0:
                    operations_list += f"r_{index + 1} = ({Fraction(1, col_elements[index])}) * r_{index + 1}\n"

                col_elements[index] *= Fraction(1, col_elements[index])

                if operations_list != "":
                    result.append([copy.copy(self.__data), operations_list])

                # print(col_elements)
                # print(self)

            arrange_rows(self)
            find_one(self)
            find_equal_values(self)
            find_multiples(self)
            zero_with_row_op(self)

            reduce_to_one(self)

            find_one(self)
            arrange_rows(self)
            find_multiples(self)
            zero_with_row_op(self)
            arrange_rows(self)

        ### Now we go from the right and zero the above column elements
        for col in range(x - 1, -1, -1):
            operations_list = ""
            # We create a list containing all the elements of the 'col' column
            col_elements = [0 for _ in range(self.nrow)]
            for i in range(self.nrow):
                col_elements[i] = self.__data[i * self.ncol + col]



            for k in range(col - 1, -1, -1):
                self.row_op(k, k, -1 * col_elements[k], col)
                if float(col_elements[k]) != 0.0:
                    operations_list += f"r_{k + 1} = r_{k + 1} +{-1 * col_elements[k]} * r_{col + 1}\n"
                col_elements[k] *= 0

            if operations_list != "":
                result.append([copy.copy(self.__data), operations_list])

            # print(col_elements)

            # print()

        return result

    def row_echelon_form_2(self, to_print):
        sign = 1
        if to_print != 1:
            to_print = 0
        x = min(self.nrow, self.ncol)  # Thanks to x, we know when to stop staggering and not go outside the matrix.
        for col in range(x):  # We walk diagonally, therefore at the beginning of the loop row = col
            row = col
            curr_cell = self.__data[row * self.ncol + col]
            while curr_cell == 0 and row + 1 < self.nrow:  # We are looking for a non-zero value in the column 'col'...
                row += 1
                curr_cell = self.__data[row * self.ncol + col]
            if float(curr_cell) == 0.0:  # ...and we consider the case when the entire column is null
                continue
            if row != col:  # case where cell a_'col''col' is zero
                buffer = [0 for _ in range(self.ncol)]
                for j in range(self.ncol):
                    buffer[j] = self.__data[col * self.ncol + j]
                self.row_op(col, row, 0, col)
                for k in range(self.ncol):
                    self.__data[row * self.ncol + k] = buffer[k]
                sign *= -1
            if to_print == 1:
                print(f"r{col + 1} = r{col + 1} / a{col + 1}{col + 1}")  # printing
                print(self)  # printing

            for p in range(
                    self.nrow):  # we convert the remaining values in the column to 0 by performing the usual step operations
                if p <= col:  # we omit the row that nulls the rest
                    continue
                curr_cell = self.__data[p * self.ncol + col]
                self.row_op(p, p, Fraction(-1 * curr_cell, self.__data[col * self.ncol + col]), col)
                if to_print == 1:
                    print(
                        f"r{p + 1} = r{p + 1} + {Fraction(-1 * curr_cell, self.__data[col * self.ncol + col])} * r{col + 1}")  # printing
                    print(self)  # printing

        return sign

    def row_echelon_form(self):
        maximum = self.__data[0]
        index = 0
        for i in range(self.ncol):
            if self.__data[i * self.ncol] > maximum:
                maximum = self.__data[i * self.ncol]
                index = i
        if index != 0:
            buffer = [0 for _ in range(self.ncol)]
            for j in range(self.ncol):
                buffer[j] = self.__data[j]
            self.row_op(0, index, 0, 0)
            for j in range(self.ncol):
                self.__data[index * self.ncol + j] = buffer[j]

        x = min(self.nrow, self.ncol)  # Thanks to x we know when to finish row_echelon_form and not go outside the matrix.
        for col in range(x):  # We walk diagonally, therefore at the beginning of the loop row = col
            row = col
            curr_cell = self.__data[row * self.ncol + col]
            while curr_cell == 0 and row + 1 < self.nrow:  # We are looking for a non-zero value in the column 'col'...
                row += 1
                curr_cell = self.__data[row * self.ncol + col]
            if float(curr_cell) == 0:  # ...and we consider the case when the entire column is zero
                continue
            if row != col:  # case where cell a_'col''col' is zero
                self.row_op(col, col, 1,
                            row)  # to the row 'col' (with a zero cell) we add the row 'row' so that the cell a_'col''col' is not zero

            for p in range(
                    self.nrow):  # we convert the remaining values in the column to 0 by performing the usual step operations
                if p <= col:  # we omit the row that zeros the rest
                    continue
                curr_cell = self.__data[p * self.ncol + col]
                # print(f"r{p+1} = r{p+1} + {curr_cell*-1} * r{col+1}")   #printing
                self.row_op(p, p, Fraction(curr_cell, -1 * self.__data[row * self.ncol + col]), col)
                # print(self)                                                  #printing

    def det(self):
        if self.ncol != self.nrow:
            # raise ValueError("It is not square matrix")
            return
        temp = copy.deepcopy(self)

        sign = temp.row_echelon_form_2(0)
        result = temp.__data[0]
        for i in range(1, temp.ncol):
            result *= temp.__data[i * temp.ncol + i]
        return result * sign

    def det_Laplace(self):
        if self.ncol != self.nrow:
            raise ValueError("Matrix is not square")
        temp = copy.copy(self)

        def rec_det(matrix):
            if matrix.ncol == 1:
                return matrix.__data[0]
            elif matrix.ncol == 2:
                return matrix.__data[0] * matrix.__data[3] - matrix.__data[2] * matrix.__data[1]
            elif matrix.ncol == 3:
                return matrix.__data[0] * matrix.__data[4] * matrix.__data[8] + matrix.__data[1] * matrix.__data[5] * \
                       matrix.__data[6] + matrix.__data[2] * matrix.__data[3] * matrix.__data[7] - matrix.__data[6] * \
                       matrix.__data[4] * matrix.__data[2] - matrix.__data[7] * matrix.__data[5] * matrix.__data[0] - \
                       matrix.__data[8] * matrix.__data[3] * matrix.__data[1]
            else:
                result = 0
                del_row = 0
                del_col = 0
                for m in range(matrix.ncol):
                    new_data = [Fraction for _ in range((matrix.nrow - 1) * (matrix.ncol - 1))]
                    new_data_index = 0
                    del_col = m
                    for i in range(matrix.ncol):
                        if i == del_row:
                            continue
                        for j in range(matrix.ncol):
                            if j == del_col:
                                continue
                            new_data[new_data_index] = matrix.__data[i * matrix.ncol + j]
                            new_data_index += 1
                    wsp = (-1) ** (del_row + 1 + del_col + 1) * matrix.__data[del_row * matrix.ncol + del_col]
                    result += wsp * rec_det(Matrix(matrix.nrow - 1, matrix.ncol - 1, new_data))

                return result

        return rec_det(temp)

    # To delete
    def det_rec(self):
        if self.ncol == 1:
            return self.__data[0]
        elif self.ncol == 2:
            return self.__data[0] * self.__data[3] - self.__data[2] * self.__data[1]
        elif self.ncol == 3:
            return self.__data[0] * self.__data[4] * self.__data[8] + self.__data[1] * self.__data[5] * self.__data[6] + \
                   self.__data[2] * self.__data[3] * self.__data[7] - self.__data[6] * self.__data[4] * self.__data[2] - \
                   self.__data[7] * self.__data[5] * self.__data[0] - self.__data[8] * self.__data[3] * self.__data[1]
        else:
            result = 0
            del_row = 0
            del_col = 0
            for m in range(self.ncol):
                new_data = [Fraction for _ in range((self.nrow - 1) * (self.ncol - 1))]
                new_data_index = 0
                del_col = m
                for i in range(self.ncol):
                    if i == del_row:
                        continue
                    for j in range(self.ncol):
                        if j == del_col:
                            continue
                        new_data[new_data_index] = self.__data[i * self.ncol + j]
                        new_data_index += 1
                wsp = (-1) ** (del_row + 1 + del_col + 1) * self.__data[del_row * self.ncol + del_col]
                matrix = Matrix(self.nrow - 1, self.ncol - 1, new_data)
                result += wsp * matrix.det_rec()

            return result

    def invert(self):
        temp_data = [0 for _ in range(2 * self.nrow * self.ncol)]
        for i in range(self.nrow):
            for j in range(2 * self.ncol):
                if j < self.ncol:
                    temp_data[i * 2 * self.ncol + j] = self.__data[i * self.ncol + j]
                else:
                    if j - self.ncol == i:
                        temp_data[i * 2 * self.ncol + j] = 1
                    else:
                        temp_data[i * 2 * self.ncol + j] = 0

        temp = Matrix(self.nrow, self.ncol * 2, temp_data)
        temp.reduced_row_echelon(0)

        new_data = [0 for _ in range(self.nrow * self.ncol)]
        for i in range(self.nrow):
            for j in range(self.ncol):
                new_data[i * self.ncol + j] = temp.__data[i * temp.ncol + j + self.ncol]

        return Matrix(self.nrow, self.ncol, new_data)


def main():
    random.seed(1234)
    A = [[1, 1, 1],
         [1, 1, 1],
         [1, 1, 1]]

    # for i in range(9):
    #     numerator = random.randint(-100, 100)
    #     denominator = random.randint(1, 100)
    #     u = Fraction(numerator, denominator)
    #     A[i // 3][i % 3] = u
    # A = Matrix(3, 3, A)
    #
    #
    # ncol = 5
    # nrow = 5
    # for i in range(100):
    #     data = [0 for _ in range(nrow * ncol)]
    #     for j in range(nrow * ncol):
    #         data[j] =  random.randint(-3, 3)
    #     matrix = Matrix(nrow, ncol, data)
    #     print(f"Matrix nr : {i+1}\n{matrix}")
    #     matrix.row_echelon_form()
    #     print(f"Matrix nr : {i+1} poschodkowana")
    #     print(matrix)
    #     print()
    #     time.sleep(0.1)

    matrix_a = Matrix(2, 2, [[1, 2], [2, 3]])
    matrix_b = Matrix(2, 2, [[2, 5], [1, 3]])
    matrix_c = Matrix(2, 2, [[0, -1], [1, -1]])
    matrix_a_p = Matrix(2, 2, [[-3, 2], [2, -1]])
    # rint(f"C@B'={matrix_c@matrix_b}")
    # matrix = Matrix(4, 5, [[2, 4, 1, 2, 0], [2, 10, 3, 6, -1], [4, 6, 2, 3, 1], [10, 15, 6, 9, -1]])
    # matrix.row_echelon_form()
    # matrix_x =Matrix(2, 2, [[Fraction(-5, 8), Fraction(13, 4)], [Fraction(7, 4), Fraction(-9, 2)]])
    # print(f"AXB=:{matrix_a@matrix_x@matrix_b}")

    #
    B = Matrix(2, 3, [[2, 1, 0], [-1, 4, 0]])
    # C = Matrix(3, 3, [[1, 3, 2], [-2, 0, 1], [5, -3, 2]])
    # V = Matrix(3, 1, [[1], [1], [1]])
    # # print(A)
    # #  print(A.transpose())
    # print(A)
    # print(B @ C)
    # print(B @ C + 2)
    # D = B @ C + 2.1
    # print(D)
    # fraction = Fraction(1, 2)
    # print(fraction, fraction + 2, 2 + fraction)
    # print(B)
    # E = Matrix(4, 8, [[1, 0, 0, 0, 5, -2, -6, 1],
    #                   [0, 1, 0, 0, -1, -4, 2, 8],
    #                   [0, 0, 1, 0, 3, 1, 2, 7],
    #                   [0, 0, 0, 1, 0, 4, 2, 1]])
    #
    # B = E
    #
    M = Matrix(4, 4, [[0, 2, 3, 4],
                      [3, 4, 2, 1],
                      [3, 1, 4, 2],
                      [3, 4, 2, 3]])

    S = Matrix(9, 9, [[0, 5, 8, 2, 6, 3, 7, 3, 2],
                      [7, 4, 3, 7, 4, 3, 6, 2, 9],
                      [4, 0, 0, 4, 5, 1, 7, 3, 5],
                      [6, 3, 2, 6, 0, 6, 1, 5, 2],
                      [8, 7, 5, 6, 4, 3, 5, 2, 7],
                      [5, 6, 3, 5, 2, 4, 5, 2, 5],
                      [6, 3, 0, 1, 1, 3, 8, 5, 4],
                      [7, 3, 6, 4, 7, 3, 7, 5, 2],
                      [5, 7, 7, 0, 8, 9, 3, 2, 6],
                      ])

    Dz = Matrix(4, 8, [[1, 1, -1, -1, 1, 0, 0, 0],
                       [1, 6, 2, 10, 0, 1, 0, 0],
                       [-1, 2, 3, 8, 0, 0, 1, 0],
                       [3, 6, -1, 3, 0, 0, 0, 1]])

    D = Matrix(4, 4, [[1, 1, -1, -1],
                      [1, 6, 2, 10],
                      [-1, 2, 3, 8],
                      [3, 6, -1, 3]])

    rD = Matrix(4, 4, [[14, -5, 8, 0],
                       [-9, 2, -4, 1],
                       [0, -3, 3, 2],
                       [4, 0, 1, -1]])

    h = Matrix(6, 6, [[0, 2, 3, 5, 2, 6],
                      [-3, -2, 5, -2, 9, 1],
                      [4 / 5, 0, -2, 0, -4, 8],
                      [2 / 5, -3, 2, -3, 1, 3],
                      [4, 4, 3, 0, -3, 7],
                      [-1 / 4, 3, 1, 11, 2, -3]])

    test = Matrix(3, 3, [
        [1, 1, 0],
        [-2, 1, 2],
        [1, 2, -1]])

    # print(test)
    # test = test.invert()
    # print(test)
    # # print(Dz.reduced_row_echelon())
    # # print(D@rD)
    # print(Dz)
    # print("Matrix transponowana")
    # print(Dz.transpose())

    # result = 0
    # start = time.time()
    # for i in range(1):
    #     result = h.det_Laplace()
    # stop = time.time()
    # print(f"Time det_Laplace: {stop-start}, determinant value: {result}")
    #
    # #print(rD)
    #
    # start = time.time()
    # for i in range(1):
    #     result = h.det_rec()
    # stop = time.time()
    # print(f"Time det_rec: {stop-start}, determinant value: {result}")
    #
    # #print(rD)
    #
    # start = time.time()
    # for i in range(1):
    #     result = h.det()
    # stop = time.time()
    # print(f"Time det: {stop-start}, determinant value: {result}")

    #    print(rD)

    # print(test)
    # print(*test.reduced_row_echelon_smarter_tkinter(), sep="\n")
    # print(test)
    # BB = Matrix(3,3,[[1,1,1],[1,5,1],[1,1,1]])
    # print(BB)
    # print(BB@BB)

    # print(S.det_Laplace())
    # numerator = 2
    # denominator = 1
    # print(f"numerator={numerator}, denominator={denominator},1/Fraction-1={Fraction(1,Fraction(numerator,denominator))-1} ")

    # B = M
    # print(B)
    # while True:
    #     #M.reduced_row_echelon()
    #     print("------------------------")
    #     M.row_echelon_form()
    #     a = int(input("a: "))
    #     b = int(input("b: "))
    #     numerator = int(input("numerator: "))
    #     denominator = int(input("denominator: "))
    #     d = int(input("d: "))
    #     B.row_op(a, b, Fraction(numerator, denominator), d)
    #     print(B)

    # B.row_op(0, 0, (1 / 2) - 1, 0)
    # print(B)
    # B.row_op(1, 1, 1, 0)
    # print(B)
    # B.row_op(1, 1, Fraction(-7, 9), 1)
    # print(B)
    # B.row_op(0, 0, -0.5, 1)
    # print(B)
    #


P = Matrix(3, 3, [[-7, 0, -2], [3, -4, 3], [4, 4, -1]])
print(P)
V = Matrix(3, 1, [[Fraction(-8, 28)], [Fraction(15, 28)], [1]])
print((P @ V))

# row_echelon_form

if __name__ == '__main__':
    main()
