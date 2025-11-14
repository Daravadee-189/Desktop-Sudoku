canvas_width = 500
canvas_height = 900
grid_size = 9
grid_top = 20
grid_bottom = 625
xflowchart = 650
yflowchart = 50

resetY = grid_bottom + 100
showY = grid_bottom + 100
showX = 280

clicked_cell = None
num = []
position_num = []
isError = []
solution = None

fixedCells = set()
selectedNumber = None
selectorTop = 0
selectorH = 50
cellSelectorW = 0

def shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = int(random(i + 1))
        tmp = arr[i]
        arr[i] = arr[j]
        arr[j] = tmp
    return arr

def setup():
    global cell_w, cell_h, cellSelectorW, selectorTop
    size(1000, canvas_height)
    cell_w = canvas_width / grid_size
    cell_h = (grid_bottom - grid_top) / grid_size
    cellSelectorW = canvas_width / grid_size
    selectorTop = grid_bottom + 20

    for row_index in range(grid_size):
        row = []
        for col_index in range(grid_size):
            row.append(0)
        num.append(row)
    
    for row_index in range(grid_size):
        row = []
        for col_index in range(grid_size):
            row.append(False)
        isError.append(row)

    for row in range(grid_size):
        row_pos = []
        for col in range(grid_size):
            x = col * cell_w
            y = grid_top + row * cell_h
            x2 = x + cell_w
            y2 = y + cell_h
            row_pos.append([x, y, x2, y2])
        position_num.append(row_pos)

    generatePuzzle()

def draw():
    background(255)
    draw_grid()
    draw_table()
    draw_errors()
    flowchart_section(650, 25)

def draw_grid():
    draw_table()
    if clicked_cell is not None:
        row = clicked_cell[0]
        col = clicked_cell[1]
        draw_rect_in_cell(row,col)
    drawNumbers()
    drawNumberSelector()

def draw_table():
    strokeWeight(5)
    stroke(0)
    line(0, grid_top, canvas_width, grid_top)
    line(0, grid_bottom, canvas_width, grid_bottom)

    for i in range(1, grid_size):
        x = i * cell_w
        y = grid_top + i * cell_h

        strokeWeight(3 if i % 3 == 0 else 1)
        line(x, grid_top, x, grid_bottom)
        line(0, y, canvas_width, y)

    strokeWeight(5)
    line(canvas_width - 1, grid_top, canvas_width - 1, grid_bottom)

def draw_rect_in_cell(row, col):
    x = col * cell_w
    y = grid_top + row * cell_h
    padding = 4

    fill(255, 0, 0, 100)
    noStroke()
    rect(x + padding, y + padding, cell_w - 2 * padding, cell_h - 2 * padding)

def calculate_box(Xuser, Yuser, x, y, x2, y2):
    return Xuser > x and Xuser < x2 and Yuser > y and Yuser < y2

def mousePressed():
    global clicked_cell, selectedNumber
    for row in range(grid_size):
        for col in range(grid_size):
            x, y, x2, y2 = position_num[row][col]
            if calculate_box(mouseX, mouseY, x, y, x2, y2):
                if (row * grid_size + col) not in fixedCells:
                    clicked_cell = (row, col)
                return

    if selectorTop <= mouseY <= selectorTop + selectorH:
        for i in range(9):
            x = i * cellSelectorW
            if x <= mouseX <= x + cellSelectorW:
                selectedNumber = i + 1
                if clicked_cell:
                    row, col = clicked_cell
                    if (row * grid_size + col) not in fixedCells:
                        num[row][col] = selectedNumber
                return

def keyPressed():
    global clicked_cell, selectedNumber
    if clicked_cell:
        row, col = clicked_cell
        if (row * grid_size + col) not in fixedCells:
            if '1' <= key <= '9':
                num[row][col] = int(key)
            elif key == '0' or key == 'Backspace' or key == 'Delete':
                num[row][col] = 0

    if key == 'r' or key == 'R':
        generatePuzzle()
        clicked_cell = None
        selectedNumber = None

def drawNumbers():
    textSize(24)
    textAlign(CENTER, CENTER)
    for row in range(grid_size):
        for col in range(grid_size):
            n = num[row][col]
            if n != 0:
                x = col * cell_w + cell_w / 2
                y = grid_top + row * cell_h + cell_h / 2
                if (row * grid_size + col) in fixedCells:
                    fill(0)
                else:
                    fill(50, 100, 255)
                text(str(n), x, y)
            
def draw_errors():
    noFill()
    stroke(255, 0, 0)
    strokeWeight(3)

    for r in range(grid_size):
        for c in range(grid_size):
            if num[r][c] == 0:
                continue

            wrong = False
            v = num[r][c]

            if solution and solution[r][c] != 0:
                wrong = (v != solution[r][c])
            else:
                for i in range(grid_size):
                    if i != c and num[r][i] == v:
                        wrong = True
                    if i != r and num[i][c] == v:
                        wrong = True

                sr = (r // 3) * 3
                sc = (c // 3) * 3
                for rr in range(sr, sr + 3):
                    for cc in range(sc, sc + 3):
                        if (rr != r or cc != c) and num[rr][cc] == v:
                            wrong = True

            if wrong:
                x = c * cell_w
                y = grid_top + r * cell_h
                rect(x, y, cell_w, cell_h)
                rect(x + 2, y + 2, cell_w - 4, cell_h - 4)

    noStroke()

def drawNumberSelector():
    for i in range(9):
        x = i * cellSelectorW
        y = selectorTop
        fill(200 if selectedNumber == i + 1 else 240)
        stroke(0)
        rect(x, y, cellSelectorW, selectorH)

        fill(0)
        textSize(24)
        textAlign(CENTER, CENTER)
        text(str(i + 1), x + cellSelectorW / 2, y + selectorH / 2)

def generateSolution():
    board = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    solveBoard(board)
    return board

def solveBoard(board):
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] == 0:
                nums = shuffle(list(range(1, 10)))
                for numTry in nums:
                    if isValid(board, row, col, numTry):
                        board[row][col] = numTry
                        if solveBoard(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def isValid(board, row, col, num):
    if num in board[row]:
        return False
    for r in range(grid_size):
        if board[r][col] == num:
            return False
    startRow = (row // 3) * 3
    startCol = (col // 3) * 3
    for r in range(startRow, startRow + 3):
        for c in range(startCol, startCol + 3):
            if board[r][c] == num:
                return False
    return True

def generatePuzzle():
    global num
    num = generateSolution()
    fixedCells.clear()
    for r in range(grid_size):
        for c in range(grid_size):
            if random(1) > 0.6:
                fixedCells.add(r * grid_size + c)
            else:
                num[r][c] = 0
