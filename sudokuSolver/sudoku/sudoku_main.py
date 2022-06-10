from sudoku import Sudoku
from sudoku.sudoku import SudokuSolver

T = int(input())
for testCase in range(1, T+1) :
    # sdk 입력, 빈 list 인자로 줌
    sdk = SudokuSolver([])
    for row in range(N) :
        ithRow = list(map(int, list(input())))
        # 스도쿠에 loc들을 삽입
        sdk.matrix.append([loc(row, column, ithRow[column]) for column in range(N)])

    print('=== testCase {0} ==='.format(testCase))
    print('---------- before -------------')
    sdk.print()

    sdk = play_sdk(sdk)

    print('\n---------- after -------------')
    sdk.print()

