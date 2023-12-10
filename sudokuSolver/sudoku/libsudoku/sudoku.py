from copy import deepcopy

N = 9


class SudokuSolver():
    def __init__(self, matrix):
        self.matrix = deepcopy(matrix)

    def print(self):
        for row in range(len(self.matrix)):
            print(self.matrix[row])

    def get_mat(self):
        sudoku = list()
        for row in range(9):
            sudoku_row = list()
            for col in range(9):
                sudoku_row.append(self.matrix[row][col].number)
            sudoku.append(sudoku_row)
        return sudoku

    def is_fail(self):
        get_candidate(self.matrix)
        emptyList = get_empty_loc(self.matrix)

        if not emptyList:
            return None

        if len(emptyList[0].candidate) == 0:
            return True
        else:
            return False

    def is_finish(self):
        for row in range(9):
            for column in range(9):
                if self.matrix[row][column].number == 0:
                    return False

        return True


class loc():
    def __init__(self, row, column, number):
        self.row = row
        self.column = column
        self.number = number
        self.candidate = []
        self.candidate_mask = 0

    def __repr__(self):
        return '{0}'.format(self.number)


def three_by_three_matrix(sdk, row, column):
    startRowIdx = (row // 3) * 3
    startColumnIdx = (column // 3) * 3

    return [sdk[row][column].number for row in range(startRowIdx, startRowIdx + 3)
            for column in range(startColumnIdx, startColumnIdx + 3)]


def column_list(sdk, column):
    return [sdk[row][column].number for row in range(N)]


def row_list(sdk, row):
    return [sdk[row][column].number for column in range(N)]


def get_empty_loc(sdk):
    toRet = []
    for row in range(N):
        for column in range(N):
            if sdk[row][column].number == 0:
                toRet.append(sdk[row][column])

    return sorted(toRet, key=lambda x: len(x.candidate))


def get_candidate(sdk):
    emptyList = get_empty_loc(sdk)

    for loc in emptyList:
        existNumbers = sorted(list(set(three_by_three_matrix(sdk, loc.row, loc.column) +
                                       column_list(sdk, loc.column) +
                                       row_list(sdk, loc.row))))

        loc.candidate = [num for num in range(1, 10) if num not in existNumbers]

        loc.candidate_mask = (1 << 10) - 1
        for num in existNumbers:
            loc.candidate_mask &= ~(1 << num)


def play_sdk(sdk):
    get_candidate(sdk.matrix)

    if sdk.is_fail():
        return None
    if sdk.is_finish():
        return sdk

    emptyList = get_empty_loc(sdk.matrix)

    if not emptyList:
        return sdk

    topLoc = emptyList[0]
    candidate_mask = topLoc.candidate_mask
    while candidate_mask:
        num = (candidate_mask & -candidate_mask).bit_length() - 1
        tmpSdk = deepcopy(sdk)
        tmpSdk.matrix[topLoc.row][topLoc.column].number = num

        result = play_sdk(tmpSdk)
        if result is not None:
            return result
        candidate_mask &= ~(1 << num)


