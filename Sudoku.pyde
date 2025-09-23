canvas_width = 500
canvas_height = 750
grid_size = 9
grid_top = 125
grid_bottom = 625
cell_w = canvas_width / grid_size
cell_h = (grid_bottom - grid_top) / grid_size
clicked_cell = None
number = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
position_num = []

for row in range(grid_size):
    row_pos = []#Create A Blank Column to recieve a box position 
    for col in range(grid_size):
        x = col * cell_w
        y = grid_top + row * cell_h
        x2 = x + cell_w
        y2 = y + cell_h
        row_pos.append([x,y,x2,y2])#Store Array Ex. row_pos = [[2,3,4,5],[?,?,?,?],....]
    position_num.append(row_pos)#Store Array in Array Ex. postion_num = [[[2,3,4,5],[?,?,?,?],....],[[2,3,4,5],[?,?,?,?],....]]
        
def setup():
    size(canvas_width, canvas_height)
    draw_grid()

def draw():
    draw_grid()

        
def draw_grid():
    background(255)
    draw_table()
    draw_subtable()
    if clicked_cell is not None:
        draw_circle_in_cell(*clicked_cell)

def draw_table():
    strokeWeight(5)
    line(0, grid_top, width, grid_top)
    line(0, grid_bottom, width, grid_bottom)
    
    for i in range(1, grid_size):
        if i % 3 == 0:
            x = i * cell_w #3 * (500/9)
            line(x, grid_top, x, grid_bottom)

    for i in range(1, grid_size):
        if i % 3 == 0:
            y = grid_top + i * cell_h
            line(0, y, width, y)

def draw_subtable():
    strokeWeight(1)
    
    for i in range(1, grid_size):
        if i % 3 != 0:
            x = i * cell_w #1 * (500/9)
            line(x, grid_top, x, grid_bottom)
    
    for i in range(1, grid_size):
        if i % 3 != 0:
            y = grid_top + i * cell_h
            line(0, y, width, y)

def draw_circle_in_cell(row, col):
    x = col * cell_w + cell_w / 2
    y = grid_top + row * cell_h + cell_h / 2
    fill(255, 0, 0)
    ellipse(x, y, 20, 20)
    
def culculate_box(Xuser,Yuser,x,y,x2,y2):
    return x < Xuser < x2 and y < Yuser < y2
        
def mousePressed():
    global clicked_cell
    for row in range(grid_size):#loop Matrix 9x9
        for col in range(grid_size):
            x , y , x2 , y2 = position_num[row][col] #assign multiple variable from position_num like Ex. position_num[0][0] is [12,23,24,54] then x = 12 , y = 23 , x2 =24 ,y2 = 54 
            if culculate_box(mouseX,mouseY,x,y,x2,y2):
                clicked_cell = (row,col)

def keyPressed():
    global number
    if clicked_cell is not None:
        row, col = clicked_cell
        if key.isdigit():
            number[row][col] = int(key)
            print("Inserted",key)