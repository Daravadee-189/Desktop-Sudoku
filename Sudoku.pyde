canvas_width = 500
canvas_height = 750
grid_size = 9
grid_top = 20
grid_bottom = 625

cell_w = canvas_width / grid_size
cell_h = (grid_bottom - grid_top) / grid_size

clicked_cell = None
num = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
position_num = []

fixedCells = set()
selectedNumber = None
selectorTop = 0
selectorH = 50
cellSelectorW = 0

def shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = int(random(i + 1))
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def setup():
    global cell_w, cell_h, cellSelectorW, selectorTop
    size(canvas_width, canvas_height)
    cell_w = canvas_width / grid_size
    cell_h = (grid_bottom - grid_top) / grid_size
    cellSelectorW = canvas_width / grid_size
    selectorTop = grid_bottom + 20

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
    draw_grid()

def draw_grid():
    background(255)
    draw_table()
    draw_subtable()
    if clicked_cell is not None:
        draw_rect_in_cell(*clicked_cell)
    drawNumbers()
    drawNumberSelector()

def draw_table():
    strokeWeight(5)
    line(0, grid_top, width, grid_top)
    line(0, grid_bottom, width, grid_bottom)

    for i in range(1, grid_size):
        if i % 3 == 0:
            x = i * cell_w
            line(x, grid_top, x, grid_bottom)

    for j in range(1, grid_size):
        if j % 3 == 0:
            y = grid_top + j * cell_h
            line(0, y, width, y)

def draw_subtable():
    strokeWeight(1)
    for i in range(1, grid_size):
        if i % 3 != 0:
            x = i * cell_w
            line(x, grid_top, x, grid_bottom)

    for j in range(1, grid_size):
        if j % 3 != 0:
            y = grid_top + j * cell_h
            line(0, y, width, y)

def draw_rect_in_cell(row, col):
    x = col * cell_w
    y = grid_top + row * cell_h
    padding = 4

    fill(255, 0, 0, 100)
    noStroke()
    rect(x + padding, y + padding, cell_w - 2 * padding, cell_h - 2 * padding)

def culculate_box(Xuser, Yuser, x, y, x2, y2):
    return Xuser > x and Xuser < x2 and Yuser > y and Yuser < y2

def mousePressed():
    global clicked_cell, selectedNumber
    for row in range(grid_size):
        for col in range(grid_size):
            x, y, x2, y2 = position_num[row][col]
            if culculate_box(mouseX, mouseY, x, y, x2, y2):
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
