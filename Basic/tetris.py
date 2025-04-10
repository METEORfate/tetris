import tkinter as tk
from tkinter import messagebox
import random

# 定义每个方块的大小
cell_size = 30
# 定义游戏区域的列数和行数
C = 12
R = 20
# 计算游戏区域的高度和宽度
height = R * cell_size
width = C * cell_size

# 刷新页面的毫秒间隔
FPS = 200

# 定义各种形状的相对坐标
SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],  # 正方形
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],  # S 形
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],   # T 形
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],   # I 形
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)], # L 形
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)], # J 形
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],  # Z 形
}

# 定义各种形状的颜色
SHAPESCOLOR = {
    "O": "blue",
    "S": "red",
    "T": "yellow",
    "I": "green",
    "L": "purple",
    "J": "orange",
    "Z": "Cyan",
}

def draw_cell_by_cr(canvas, c, r, color="#CCCCCC", tag_kind=""):
    """
    在画板上绘制一个方块
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :param tag_kind: 方块的标签类型，用于后续操作
    """
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = c * cell_size + cell_size
    y1 = r * cell_size + cell_size
    if tag_kind == "falling":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                                outline="white", width=2, tag=tag_kind)
    elif tag_kind == "row":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                                outline="white", width=2, tag="row-%s" % r)
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                                outline="white", width=2)

def draw_board(canvas, block_list, isFirst=False):
    """
    绘制游戏面板
    :param canvas: 画板
    :param block_list: 游戏区域的状态列表
    :param isFirst: 是否是第一次绘制
    """
    for ri in range(R):
        canvas.delete("row-%s" % ri)  # 清除之前的行

    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_cell_by_cr(canvas, ci, ri, SHAPESCOLOR[cell_type], tag_kind="row")
            elif isFirst:
                draw_cell_by_cr(canvas, ci, ri)

def draw_cells(canvas, c, r, cell_list, color="#CCCCCC"):
    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param c: 该形状设定的原点所在的列
    :param r: 该形状设定的原点所在的行
    :param cell_list: 该形状各个方格相对自身所处位置
    :param color: 该形状颜色
    """
    for cell in cell_list:
        cell_c, cell_r = cell
        ci = cell_c + c
        ri = cell_r + r
        # 判断该位置方格在画板内部(画板外部的方格不再绘制)
        if 0 <= ci < C and 0 <= ri < R:
            draw_cell_by_cr(canvas, ci, ri, color, tag_kind="falling")

win = tk.Tk()
canvas = tk.Canvas(win, width=width, height=height)
canvas.pack()

# 初始化游戏区域的状态列表
block_list = []
for i in range(R):
    i_row = ['' for j in range(C)]
    block_list.append(i_row)

# 第一次绘制游戏面板
draw_board(canvas, block_list, True)

def draw_block_move(canvas, block, direction=[0, 0]):
    """
    绘制向指定方向移动后的俄罗斯方块
    :param canvas: 画板
    :param block: 俄罗斯方块对象
    :param direction: 俄罗斯方块移动方向
    """
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    # 移动前，先清除原有位置绘制的俄罗斯方块,也就是用背景色绘制原有的俄罗斯方块
    canvas.delete("falling")

    dc, dr = direction
    new_c, new_r = c + dc, r + dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])

def generate_new_block():
    """
    随机生成新的俄罗斯方块
    :return: 新的俄罗斯方块对象
    """
    kind = random.choice(list(SHAPES.keys()))
    # 对应横纵坐标，以左上角为原点，水平向右为x轴正方向，
    # 竖直向下为y轴正方向，x对应横坐标，y对应纵坐标
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': SHAPES[kind],
        'cr': cr
    }

    return new_block

def check_move(block, direction=[0, 0]):
    """
    判断俄罗斯方块是否可以朝指定方向移动
    :param block: 俄罗斯方块对象
    :param direction: 俄罗斯方块移动方向
    :return: boolean 是否可以朝指定方向移动
    """
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]
        # 判断该位置是否超出左右边界，以及下边界
        if c < 0 or c >= C or r >= R:
            return False

        # 判断该位置是否已经被其他方块占据
        if r >= 0 and block_list[r][c]:
            return False

    return True

def check_row_complete(row):
    """
    检查某一行是否已经填满
    :param row: 游戏区域的某一行
    :return: boolean 该行是否填满
    """
    for cell in row:
        if cell == '':
            return False

    return True

score = 0
win.title("SCORES: %s" % score)  # 标题中展示分数

def check_and_clear():
    """
    检查并清除填满的行，更新分数
    """
    has_complete_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_list[cur_ri] = block_list[cur_ri - 1][:]
                block_list[0] = ['' for j in range(C)]
            else:
                block_list[ri] = ['' for j in range(C)]
            global score
            score += 10

    if has_complete_row:
        draw_board(canvas, block_list)
        win.title("SCORES: %s" % score)

def save_block_to_list(block):
    """
    将俄罗斯方块保存到游戏区域的状态列表中
    :param block: 俄罗斯方块对象
    """
    canvas.delete("falling")

    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr
        # block_list 在对应位置记下其类型
        block_list[r][c] = shape_type

        draw_cell_by_cr(canvas, c, r, SHAPESCOLOR[shape_type], tag_kind="row")

def horizontal_move_block(event):
    """
    左右水平移动俄罗斯方块
    :param event: 键盘事件
    """
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(canvas, current_block, direction)

def rotate_block(event):
    """
    旋转俄罗斯方块
    :param event: 键盘事件
    """
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, -cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        'kind': current_block['kind'],  # 对应俄罗斯方块的类型
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):
        cc, cr = current_block['cr']
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        draw_cells(canvas, cc, cr, rotate_list, SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate

def land(event):
    """
    使俄罗斯方块立即下落到最底部
    :param event: 键盘事件
    """
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = R
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if r >= 0 and block_list[r][c]:
            return
        h = 0
        for ri in range(r + 1, R):
            if block_list[ri][c]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, down):
        draw_block_move(canvas, current_block, down)

def game_loop():
    """
    游戏主循环
    """
    win.update()
    global current_block
    if current_block is None:
        new_block = generate_new_block()
        # 新生成的俄罗斯方块需要先在生成位置绘制出来
        draw_block_move(canvas, new_block)
        current_block = new_block
        if not check_move(current_block, [0, 0]):
            messagebox.showinfo("Game Over!", "Your Score is %s" % score)
            win.destroy()
            return
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            # 无法移动，记入 block_list 中
            save_block_to_list(current_block)
            current_block = None
            check_and_clear()

    win.after(FPS, game_loop)  # 在FPS 毫秒后调用 game_loop方法

canvas.focus_set()  # 聚焦到canvas画板对象上
canvas.bind("<KeyPress-Left>", horizontal_move_block)
canvas.bind("<KeyPress-Right>", horizontal_move_block)
canvas.bind("<KeyPress-Up>", rotate_block)
canvas.bind("<KeyPress-Down>", land)

current_block = None

win.update()
win.after(FPS, game_loop)  # 在FPS 毫秒后调用 game_loop方法

win.mainloop()