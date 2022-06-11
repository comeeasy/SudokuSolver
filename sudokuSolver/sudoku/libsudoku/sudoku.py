# sudoku.py

from copy import *
# sys.stdin = open('sample.txt', 'r')

# 스도쿠의 크기
N = 9

# 위치의 클래스를 정의한다.
class SudokuSolver() :
    def __init__(self, matrix) :
        self.matrix = deepcopy(matrix)

    def print(self) :
        for row in range(len(self.matrix)) :
            print(self.matrix[row])  
    
    def get_mat(self):
        sudoku = list()
        for row in range(9):
            sudoku_row = list()
            for col in range(9):
                sudoku_row.append(self.matrix[row][col].number)
            sudoku.append(sudoku_row)
        return sudoku

    def is_fail(self) :
        # 빈 loc들에 후보가 존재하지 않으면 게임 실패
        # 경우의 수가 다른 loc에서 중복되었으므로 다시
        # 이전으로 돌아가 다른 방법을 찾아봐야함
        get_candidate(self.matrix)
        emptyList = get_empty_loc(self.matrix)
        
        # 후보 리스트의 크기의 오름순으로 정렬하였으므로
        # emptyList의 가장 앞 loc의 후보 리스트의 크기가 0 이라면
        # 게임 실패 
        # 아니라면 게임을 더해봐야한다.
        
        # emptyList가 비었다면 게임이 끝났는지 안끝났는지 알 수 없으므로 None return
        if not emptyList :
            return None
        
        if len(emptyList[0].candidate) == 0 :
            return True
        else :
            return False
    
    def is_finish(self) :            
        # 게임을 완성했는지를 return하는 함수
        # 모든 loc에 0이 아닌 숫자가 들어가 있으면 게임이 끝난 것이다
        
        # 9 * 9를 모두 조사하여 만약 하나라도 0이 존재한다면
        # 끝나지 않아서 False reture
        for row in range(9) :
            for column in range(9) :
                if self.matrix[row][column].number == 0 :
                    return False
        
        # 모든 순회가 종료되었음에도 False를 return 하지 않았으므로
        # 게임이 끝났다
        return True


class loc() :
    def __init__(self, row, column, number) :
        self.row = row
        self.column = column
        self.number = number
        # 빈 후보의 리스트를 할당한다.
        self.candidate = []
        
    def __repr__(self) :
        return '{0}'.format(self.number)

# 해당 loc이 위치하는 3*3 n square 의 숫자들의 list return
# sudoku.matrix 인자로 줘야함
def three_by_three_matrix(sdk, row, column) :
    startRowIdx    = (row // 3) * 3
    startColumnIdx = (column // 3) * 3
    
    return [sdk[row][column].number for row in range(startRowIdx, startRowIdx+3)
                           for column in range(startColumnIdx, startColumnIdx+3)]

# 해당 loc의 column, row의 list들을 return
# sudoku.matrix 인자로 줘야함
def column_list(sdk, column) :
    return [sdk[row][column].number for row in range(N)]

def row_list(sdk, row) :
    return [sdk[row][column].number for column in range(N)]

# sdk에서 빈 loc들의 list를 
# sudoku.matrix 인자로 줘야함
def get_empty_loc(sdk) :
    toRet = []
    for row in range(N) :
        for column in range(N) :
            if sdk[row][column].number == 0 :
                toRet.append(sdk[row][column])
    
    return sorted(toRet, key=lambda x: len(x.candidate))

# 비어있는 loc들을 받아서 각 loc의 3*3, column, row list들을 받아서 후보들을 지정한다
# sudoku.matrix 인자로 줘야함
def get_candidate(sdk) :
    emptyList = get_empty_loc(sdk)
    
    for loc in emptyList :
        existNumbers = sorted(list(set(three_by_three_matrix(sdk, loc.row, loc.column) + 
                           column_list(sdk, loc.column) + 
                           row_list(sdk, loc.row))))
        existNumbers.remove(0)
        
        loc.candidate = [num for num in range(1, 10) if num not in existNumbers]
        
# 비어있는 loc이 없다면 모두 찼으므로 게임 종료
def play_sdk(sdk) :
    # 각 빈 자리에 후보들 list에 넣어둠
    get_candidate(sdk.matrix)
    
    # 가장 위에 있는 loc의 후보들을 해당 loc에 넣은 sudoku를
    # 모두 stack에 넣어놓고 다시 재귀적으로 호출한 함수에서
    # pop하여 게임을 진행한 뒤 풀 수 없다면 종료, 
    # 스도쿠를 해결하였다면 해결한 스도쿠를 return한다.
    
    # 게임을 풀 수 없음
    if sdk.is_fail() :
        return None
    # 게임이 끝났다면
    elif sdk.is_finish() :
        return sdk
    # 게임을 진행할 수 있다면
    else :
        emptyList = get_empty_loc(sdk.matrix)
        
        # 가장 위의 emptyList를 모두 넣어보면서 진행
        topLoc = emptyList[0]
        for candidateNum in topLoc.candidate :
            tmpSdk = deepcopy(sdk)
            tmpSdk.matrix[topLoc.row][topLoc.column].number = candidateNum
            
            result = play_sdk(tmpSdk)
            if result != None :
                return result
        