import time

class Sudoku:

    def __init__(self, file):
        self.board = self.make_board(file)
        self.coords = self.make_coords()


    def make_board(self, file):
        a = file.split("\n")
        a.pop(0)
        a.pop(-1)
        board = {}
        for i in range(len(a)):
            board[i] = a[i]
        return board


    def make_coords(self):
        coords = {}
        for height in self.board:
            # fix if not right len
            while len(self.board[height]) < 9:
                self.board[height] += " "
            for lenght in range(len(self.board[height])):
                name = f"{height}{lenght}"
                if height in range(0, 3):
                    b1 = 0
                elif height in range(3,6):
                    b1 = 1
                else:
                    b1 = 2
                if lenght in range(0, 3):
                    b2 = 0
                elif lenght in range(3,6):
                    b2 = 1
                else:
                    b2 = 2
                if self.board[height][lenght] == " ":
                    coords[name] = set(), f"{b1}{b2}"
                else:
                    coords[name] = int(self.board[height][lenght]), f"{b1}{b2}"
        return coords

    def show_board(self, coord=False, reason=None):
        if coord:
            h = int(coord[0])
            l = int(coord[1])
        else:
            h = None
            l = None
        file = str()
        key = self.board.keys()
        for i in range(0, len(key), 3):
            part = {}
            for j in range(3):
                k = i + j
                line = self.board[k]
                p1 = line[:3]
                p2 = line[3:][:3]
                p3 = line[6:][:3]
                part[j] = f"{p1}|{p2}|{p3}"
                if k == h:
                    number = self.board[h][l]
                    part[j] += f" <---({number}) ({reason})"
            file += part[0] + "\n" + part[1] + "\n" + part[2]
            if i == 0 or i == 3:
                file += "\n---+---+---\n"
        return file

    def mark(self):
        """Marks coord with values of other boxes near it what it cant be"""
        # checks hor/ver lines
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
        # checks its 3x3 box values
        a = self.coords.items()
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
        change = True
        number = False
        while change:
            time.sleep(0.1)
            print(self.show_board(coord=number))
            print()
            self.mark()
            some = self.lenght()
            change = some[0]
            number = some[1]
            reason = some
            if change:
                continue
            else:
                change = self.box()
                if change:
                    some = self.lenght()
                    number = some[1]
                    continue
                else:
                    change = self.multi()
                    if change:
                        some = self.lenght()
                        number = some[1]
                        continue
                    else:
                        change = self.line()
                        # print(change)
                        if change:
                            some = self.lenght()
                            number = some[1]
                            continue


    def lenght(self):
        """solve if only 1 number can go into box"""
        numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in self.coords:
            if type(self.coords[i][0]) == set:
                if len(self.coords[i][0]) == 8:
                    number = list(numbers - self.coords[i][0])[0]
                    self.coords[i] = (number, self.coords[i][1])
                    h = int(i[0])
                    l = int(i[1])
                    lista = list(self.board[h])
                    lista[l] = str(number)
                    line = "".join(lista)
                    self.board[h] = line
                    return True, i
        return False, None

    def box(self):
        """solve 3x3 if a number can only be in 1 place"""
        a = self.coords.items()
        # sorts list by box coors so 0-8 is first box
        b = sorted(a, key=lambda x: x[1][1])
        change = False
        for i in range(0, len(b), 9):
            n = 0
            numbers = set()
            all_numbers = {1,2,3,4,5,6,7,8,9}
            while n < 9:
                if type(b[i + n][1][0]) == int:
                    numbers.add(b[i + n][1][0])
                n += 1
            remain = list(all_numbers - numbers)
            sets = []
            n = 0
            while n < 9:
                if type(b[i + n][1][0]) == set:
                    sets.append((b[i + n][1][0], b[i + n][0]))
                n += 1
            needed = len(remain) - 1
            for j in remain:
                count = 0
                for k in sets:
                    if j in k[0]:
                        count += 1
                    else:
                        value = k
                if needed == count:
                    # print(value[1], j)
                    values = all_numbers - {j}
                    self.coords[value[1]] = (values, self.coords[value[1]][1])
                    change = True
        return change

    def multi(self):
        """
        update other boxes if 2 or 3 boxes can only have certain numbers
        for example [123][123][123]|[1234] then 4th box is 4 as 123 can act as permanent values
        """
        a = self.coords.items()
        # sorts list by box coors so 0-8 is first box
        b = sorted(a, key=lambda x: x[1][1])
        change = False
        for i in range(0, len(b), 9):
            n = 0
            numbers = set()
            all_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            while n < 9:
                if type(b[i + n][1][0]) == int:
                    numbers.add(b[i + n][1][0])
                n += 1
            remain = list(all_numbers - numbers)
            sets = []
            n = 0
            while n < 9:
                if type(b[i + n][1][0]) == set:
                    sets.append((b[i + n][1][0], b[i + n][0]))
                n += 1
            # print(numbers, remain)
            # print(sets)
            # if 2 in a row
            rows = []
            for j in remain:
                coords = set()
                for k in sets:
                    # print(j, k[0], count)
                    if j not in k[0]:
                        coords.add(k[1])
                # print(count)
                if len(coords) == 2:
                    rows.append((coords,j))
            for j in rows:
                for k in rows:
                    # detect the number pair in a 3x3 area
                    if k[0] == j[0] and k[1] != j[1]:
                        lista = list(j[0])
                        one = lista[0]
                        two = lista[1]
                        # find x/y
                        # print(one, two)
                        if one[0] == two[0]:
                            some_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                            # print(int(one[1]) in some_numbers, int(one[1]), type(int(one[1])))
                            some_numbers.remove(int(one[1]))
                            some_numbers.remove(int(two[1]))
                            for l in some_numbers:
                                coord = one[0] + str(l)
                                if type(self.coords[coord][0]) == set:
                                    # print(self.coords[coord])
                                    self.coords[coord][0].add(k[1])
                                    self.coords[coord][0].add(j[1])
                                    change = True
        return change

    def line(self):
        # käib rea läbi
        # vaatab mis on ja mis pole ning siis vaatab mis nr on mis 3x3 alas
        a = self.coords.items()
        # h is horisontal and v is vertical
        h = sorted(a, key=lambda x: x[0][0])
        v = sorted(a, key=lambda x: x[0][1])
        ways = [h, v]
        change = False
        for x in ways:
            for i in range(0, len(x), 9):
                n = 0
                numbers = set()
                all_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                while n < 9:
                    if type(x[i + n][1][0]) == int:
                        numbers.add(x[i + n][1][0])
                    n += 1
                sets = []
                n = 0
                while n < 9:
                    if type(x[i + n][1][0]) == set:
                        sets.append((x[i + n][1][0], x[i + n][0]))
                    n += 1
                # print(sets)
                remain = list(all_numbers - numbers)
                for j in remain:
                    # print(j)
                    count = []
                    for k in sets:
                        if j not in k[0]:
                            count.append(k[1])
                    if len(count) == 1:
                        coord = count[0]
                        self.coords[coord] = all_numbers - {j}, self.coords[coord][1]
                        change = True
        return change




if __name__ == '__main__':
    file = """
1   7  3
83 6
  29  6 8
6    49 7
 9     5
3 75    4
2 3  91
   7 2 43
 4  8   9
"""

#     file = """
# 12345 7
# 2     6
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# """

    s = Sudoku(file)
    # print(s.show_board())
    s.solve()
