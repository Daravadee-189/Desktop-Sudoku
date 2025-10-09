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
num = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
position_num = []
isError = [[False for _ in range(grid_size)] for _ in range(grid_size)]
solution = None

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
    size(1000, canvas_height)
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
    background(255)
    draw_grid()
    draw_table()
    draw_errors()
    flowchart_section(650, 25)

def draw_grid():
    draw_table()
    if clicked_cell is not None:
        draw_rect_in_cell(*clicked_cell)
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
                
# Flowchart section
def start_stop_type(posx, posy, size, word):
    fill(255)
    stroke(0)
    strokeWeight(2)
    ellipse(posx, posy, size, size / 2)
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(16)
    text(word, posx, posy)
    return posy + size / 2 + 20

def process_type(posx, posy, size, word):
    fill(255)
    stroke(0)
    strokeWeight(2)
    rect(posx - size / 2, posy - size / 2, size, size)
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(16)
    text(word, posx, posy)
    return posy + size / 2 + 100

def decision_type(posx, posy, size, word):
    fill(255)
    stroke(0)
    strokeWeight(2)
    quad(
        posx, posy - size / 2,
        posx + size, posy,
        posx, posy + size / 2,
        posx - size, posy
    )
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(16)
    text(word, posx, posy)
    return posy + size / 2 + 100

def drawArrow(x, y1, y2):
    arrowGap = 10
    stroke(0)
    strokeWeight(2)
    line(x, y1, x, y2)
    
    fill(0)
    triangle(x-6, y2-arrowGap,x+6, y2-arrowGap, x, y2)

def drawArrowHorizontal(x1, x2, y):
    stroke(0)
    strokeWeight(2)
    line(x1, y, x2, y)
    fill(0)
    triangle(x2-10, y-6, x2-10, y+6, x2, y)

def text_box(x, y, box_type, word):
    textAlign(CENTER, CENTER)
    textSize(14)
    text(word, x, y)

def flowchart_section(xflowchart, yflowchart):
    y1 = start_stop_type(xflowchart, yflowchart, 100, "START")
    drawArrow(xflowchart, yflowchart + 25, y1 - 50)

    y2 = process_type(xflowchart, y1, 100, "Initialize Grid")
    drawArrow(xflowchart, y1 + 50, y2 - 40)

    y3 = process_type(xflowchart, y2, 110, "User Interaction")
    drawArrow(xflowchart, y2 + 55, y3 - 50)

    y4 = decision_type(xflowchart, y3, 100, "Is Solved?")
    text_box(xflowchart + 25, y4 - 75, 1, "TRUE")
    drawArrowHorizontal(xflowchart + 100, xflowchart + 200, y3)
    text_box(xflowchart + 120, y3 - 20, 1, "FALSE")
    drawArrow(xflowchart + 200, y3, y4 - 50)
    drawArrow(xflowchart, y3 + 50, y4 - 50)

    y5 = process_type(xflowchart, y4, 100, "Show Result")
    drawArrow(xflowchart, y4 + 50, y5 - 70)
    drawArrowHorizontal(xflowchart, xflowchart + 200, y5 - 70)

    y5alt = process_type(xflowchart + 200, y4, 100, "Show Mistake")
    drawArrow(xflowchart + 200, y4 + 50, y5 - 50)

    start_stop_type(xflowchart + 200, y5alt - 25, 100, "END")
