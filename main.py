import time

class Sudoku:

    def __init__(self, file):
        self.board = self.make_board(file)
        self.coords = self.make_coords()


    def make_board(self, file):
        a = file.split("\n")
        a.remove("")
        a.remove("")
        board = {}
        for i in range(len(a)):
            board[i] = a[i]
        return board


    def make_coords(self):
        coords = {}
        for i in self.board:
            # fix if not right len
            while len(self.board[i]) != 9:
                self.board[i] += " "
            for j in range(len(self.board[i])):
                name = f"{i}{j}"
                if i in range(0, 3):
                    b1 = 0
                elif i in range(3,6):
                    b1 = 1
                else:
                    b1 = 2
                if j in range(0, 3):
                    b2 = 0
                elif j in range(3,6):
                    b2 = 1
                else:
                    b2 = 2
                if self.board[i][j] == " ":
                    coords[name] = (set(), f"{b1}{b2}")
                else:
                    coords[name] = (int(self.board[i][j]), f"{b1}{b2}")
        return coords

    def show_board(self):
        file = ""
        for i in self.board:
            for j in range(len(self.board[i])):
                name = f"{i}{j}"
                if type(self.coords[name][0]) == int:
                    file += str(self.coords[name][0])
                else:
                    file += " "
            file += "\n"
        return file

    def mark(self):
        """Marks what coord cant be"""
        for i in self.coords:
            # print(self.coords[i])
            if type(self.coords[i][0]) == int:
                x = i[1]
                y = i[0]
                for j in range(9):
                    new = f"{j}{x}"
                    if type(self.coords[new][0]) == set:
                        self.coords[new][0].add(self.coords[i][0])
                for j in range(9):
                    new = f"{y}{j}"
                    if type(self.coords[new][0]) == set:
                        self.coords[new][0].add(self.coords[i][0])
        a = self.coords.items()
        # sorts list by box coors so 0-8 is first box
        b = sorted(a, key=lambda x: x[1][1])
        for i in range(0, len(b), 9):
            n = 0
            numbers = set()
            while n < 9:
                if type(b[i + n][1][0]) == int:
                    numbers.add(b[i + n][1][0])
                n += 1
            n = 0
            while n < 9:
                if type(b[i + n][1][0]) == set:
                    b[i + n][1][0].update(numbers)
                n += 1


    def solve(self):
        """Uses other algorithms."""
        self.mark()
        print(self.show_board())
        time.sleep(1)
        change = self.lenght()
        if change:
            self.solve()
        else:
            change2 = self.box()
            if change2:
                self.solve()
        # return self.show_board()

    def lenght(self):
        numbers = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        change = False
        for i in self.coords:
            # print(self.coords[i])
            if type(self.coords[i][0]) == set:
                if len(self.coords[i][0]) == 8:
                    change = True
                    self.coords[i] = (list(numbers - self.coords[i][0])[0], self.coords[i][1])
        return change

    def box(self):
        a = self.coords.items()
        # sorts list by box coors so 0-8 is first box
        b = sorted(a, key=lambda x: x[1][1])
        change = False
        for i in range(0, len(b), 9):
            n = 0
            numbers = set()
            all_numbers = set([1,2,3,4,5,6,7,8,9])
            while n < 9:
                if type(b[i + n][1][0]) == int:
                    numbers.add(b[i + n][1][0])
                n += 1
            all_numbers -= numbers
            sets = []
            n = 0
            while n < 9:
                if type(b[i + n][1][0]) == set:
                    sets.append((b[i + n][1][0], b[i + n][0]))
                n += 1
            for j in all_numbers:
                value = []
                for k in sets:
                    if j not in k[0]:
                        value.append(k)
                if len(value) == 1:
                    change = True
                    self.coords[value[0][1]] = (j, self.coords[value[0][1]][1])
        return change



    # def box(self):
    #     keys = list(self.coords.keys())
    #     some_list = []
    #     for i in range(0, len(keys), 3):
    #         if keys[i][0] in ["0", "3", "6"]:
    #             box = []
    #             a = keys[i]
    #             b = keys[i+1]
    #             c = keys[i+2]
    #             d = str(int(keys[i][0])+1) + keys[i][1]
    #             e = str(int(keys[i][0])+1) + keys[i+1][1]
    #             f = str(int(keys[i][0])+1) + keys[i+2][1]
    #             g = str(int(keys[i][0])+2) + keys[i][1]
    #             h = str(int(keys[i][0])+2) + keys[i+1][1]
    #             i = str(int(keys[i][0])+2) + keys[i+2][1]
    #             box.extend((a, b, c, d, e, f, g, h, i))
    #             some_list.append(box)
    #     return some_list
    #
    # def box_box(self):
    #     some_list = self.box()
    #     change = False
    #     for box in some_list:
    #         numbers = []
    #         for j in box:
    #             if type(self.coords[j]) == int:
    #                 numbers.append(self.coords[j])
    #         for j in box:
    #             if type(self.coords[j]) == list:
    #                 for k in numbers:
    #                     if k not in self.coords[j]:
    #                         change = True
    #                         self.coords[j].append(k)
    #     return change
    #
    # def box_one_position(self):
    #     some_list = self.box()
    #     all_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #     change = False
    #     for box in some_list:
    #         numbers = []
    #         lists = []
    #         for j in box:
    #             if type(self.coords[j]) == int:
    #                 numbers.append(self.coords[j])
    #         a = list(set(all_numbers) - set(numbers))
    #         for j in box:
    #             if type(self.coords[j]) == list:
    #                 lists.append((self.coords[j], j))
    #         for j in a:
    #             places = []
    #             for k in lists:
    #                 if j not in k[0]:
    #                     places.append(k[1])
    #             if len(places) == 1:
    #                 change = True
    #                 # print(self.coords[places[0]], j)
    #                 self.coords[places[0]] = j
    #     return change




if __name__ == '__main__':
#     file = """
# 5  4673 9
# 9 381 427
# 1742 3
# 231976854
# 857124 9
# 4963 8172
#     8926
# 782641  5
#  1    7 8
# """
#     s = Sudoku(file)
#     s.solve()

#     file = """
# 53  7
# 6  195
#  98    6
# 8   6   3
# 4  8 3  1
# 7   2   6
#  6    28
#    419  5
#     8  79
# """
#     s = Sudoku(file)
#     a = s.solve()


    file = """
1   7  3
83 6
  29  6 8
6    49 7
 9     5
3 75    4
2 3  91
     2 43
 4  8   9
"""
    s = Sudoku(file)
    s.solve()
