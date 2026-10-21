from kandinsky import *
from ion import *
from time import *

pieces_imgs = {
    "": [-1],
    "BP": [0, 0, 0, 0, 78732, 262440, 815751, 802629, 796068, 262440, 78732, 78732, 78732, 78732, 796068, 2391120,
           7174332, 7174332, 0, 0],
    "BN": [0, 1653372, 2381643, 2388204, 7173360, 7174089, 9299853, 23117562, 21523239, 64569960, 64392813, 62267049,
           19397556, 265680, 797121, 2391444, 7174440, 7174440, 0, 0],
    "BB": [0, 78732, 78732, 255879, 255879, 769824, 2548584, 2902878, 2922561, 2391120, 796068, 262440, 78732, 78732,
           262440, 2391120, 21523320, 21523320, 0, 0],
    "BR": [0, 0, 20989692, 25851636, 25851636, 21523320, 21523320, 21523320, 7174332, 2391120, 2391120, 2391120,
           2391120, 2391120, 3187188, 21523320, 28697652, 21523320, 0, 0],
    "BQ": [0, 78732, 44982972, 238430772, 44904240, 44720532, 59603148, 59603148, 59786856, 64832508, 71481960,
           35872308, 21785760, 28435212, 21523320, 7968213, 13554783, 21523320, 0, 0],
    "BK": [0, 78732, 262440, 262440, 78732, 6640704, 21602052, 64832508, 193972680, 193788972, 193710240, 64832508,
           66698748, 26568972, 9303012, 12036276, 7358040, 7174332, 0, 0],
    "WP": [0, 0, 0, 0, 78732, 341172, 1058508, 1058508, 1058508, 341172, 98415, 98415, 98415, 98415, 874800, 3187188,
           9565452, 7174332, 0, 0],
    "WN": [0, 1653372, 2440692, 2978694, 9561564, 9030852, 7773327, 26551152, 28618596, 85856760, 83553849, 76645116,
           19426959, 354132, 1062720, 2657043, 7971480, 7174440, 0, 0],
    "WB": [0, 98415, 98415, 314928, 314928, 946971, 3082212, 3082212, 3160944, 3187188, 1058508, 341172, 98415, 98415,
           341172, 2653560, 23914440, 21523320, 0, 0],
    "WR": [0, 0, 20989692, 25851636, 25851636, 26385264, 28697652, 28697652, 7970400, 3187188, 3187188, 3187188,
           3187188, 3187188, 3187188, 23914440, 28697652, 21523320, 0, 0],
    "WQ": [0, 78732, 44982972, 238430772, 44904240, 44740215, 74503935, 74503935, 74746692, 85830975, 79181496,
           28697652, 42784200, 36134667, 28697652, 14086224, 7436772, 21523320, 0, 0],
    "WK": [0, 78732, 262440, 262440, 78732, 6640704, 27980316, 85559760, 257746680, 258096600, 258201576, 85830948,
           83964708, 23652000, 7436772, 9486720, 9381744, 7174332, 0, 0]
}

castles = [1, 1, 1, 1]  # WQ-WK-BQ-BK
possible_move_color = color(253, 0, 111)
cursor_color = color(0, 205, 16)
cursor_size = 2
COOLDOWN = 0.2
angle = 0
board_init = ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"] + ["WP" for i in range(8)] + ["" for i in range(8 * 4)] + ["BP" for i in range(8)] + ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"]
board = board_init
possible_moves = [[] for i in range(64)]
cursor_row = 0
cursor_col = 0
playing_color = "W"
selected_p = -1  # la pièce sélectionnée
played_moves = [(0, 0, "WR")]  # tableau de (from,to,type)

def is_up():
    return keydown(KEY_UP)
def is_down():
    return keydown(KEY_DOWN)
def is_right():
    return keydown(KEY_RIGHT)
def is_left():
    return keydown(KEY_LEFT)
def is_enter():
    return keydown(KEY_OK)

def getSqrIdx(col, row):
    return col + row * 8


def inBoard(col, row):
    return 7 >= col >= 0 and 7 >= row >= 0


def decimal_to_trinary(ligne):
    """Input: number lower than 3^19, returns the value in base 3, as a table"""
    l = []
    for n in range(19, -1, -1):
        if ligne >= (3 ** n):
            l += [1 + int(ligne >= 2 * (3 ** n))]
            ligne -= ((ligne >= 2 * (3 ** n)) + 1) * (3 ** n)
        else:
            l += [0]
    return l


def getColorAt(row, col, angle):
    return color(118 + 137 * ((row + col + 1 + angle) % 2), 67 + 188 * ((row + col + 1 + angle) % 2),
                 15 + 215 * ((row + col + 1 + angle) % 2))


def print_piece(type_, x, y, angle):
    """Input: piece pattern (base 3: 0= nothing, 2=white, 1=black), screen x and y, chessboard angle, prints the piece"""
    if type_ == [-1]:
        return
    if angle % 2 == 0:  # pieces facing up or down
        if angle == 0:  # up
            coef = 1
        else:  # down
            coef = -1
            x += 20
            y += 20
        for y1 in range(len(type_)):
            l = decimal_to_trinary(type_[y1])
            for x1 in range(len(l)):
                if l[x1] == 2:
                    set_pixel(x + coef * x1, y + coef * y1, color(255, 255, 255))
                elif l[x1] == 1:
                    set_pixel(x + coef * x1, y + coef * y1, color(0, 0, 0))
    if angle % 2 == 1:  # pieces facing right or left
        if angle == 1:  # right
            coef = 1
        else:  # left
            coef = -1
            x += 20
            y += 20
        for x1 in range(len(type_)):
            l = decimal_to_trinary(type_[x1])
            for y1 in range(len(l)):
                if l[y1] == 2:
                    set_pixel(x + coef * x1, y + coef * y1, color(255, 255, 255))
                elif l[y1] == 1:
                    set_pixel(x + coef * x1, y + coef * y1, color(0, 0, 0))

def square_outline(x,y,_color,size):
    fill_rect(x - 1, y - 1, 22, size, _color)
    fill_rect(x - 1, y - 1, size, 22, _color)
    fill_rect(x - 1, y + 21 - size, 22, size, _color)
    fill_rect(x + 21 - size, y - 1, size, 22, _color)
def outline(col, row, angle_, _color, size):
    x, y = getCoords(row, col, angle_)
    square_outline(x,y, _color, size)


def clear_piece(row, col, angle):
    if row > 7 or row < 0 or col > 7 or col < 0:
        return False
    x, y = getCoords(col, row, angle)
    fill_rect(x + 1, y + 1, 18, 18, getColorAt(col + 1 + angle, row, angle))


def print_board(angle):
    for i in range(8):
        for j in range(8):
            colo = getColorAt(i, j, angle)
            fill_rect(i * 22 + 72, j * 22 + 23, 22, 22, colo)


def getCoords(col, row, angle):
    if angle == 0:
        return row * 22 + 73, (7 - col) * 22 + 24
    elif angle == 1:
        return (7 - col) * 22 + 73, (7 - row) * 22 + 24
    if angle == 2:
        return (7 - row) * 22 + 73, col * 22 + 24
    elif angle == 3:
        return col * 22 + 73, row * 22 + 24


def move_piece(_from, _to, angle, _type):
    clear_piece(_from[0], _from[1], angle)
    x, y = getCoords(_to[1], _to[0], angle)
    clear_piece(_to[0], _to[1], angle)
    print_piece(pieces_imgs[_type], x, y, angle)


def print_cursor(col, row, angle_):
    if row > 7 or row < 0 or col > 7 or col < 0:
        return
    outline(col, row, angle_, cursor_color, cursor_size)


def highlight_square(col, row, angle_, piece_name):
    outline(col, row, angle_, possible_move_color, 1)
    # TODO: add different types depending on the type of the piece


def remove_cursor(col, row, angle_):
    global possible_moves
    if not inBoard(col, row):
        return
    _color = getColorAt(row, col + 1 + angle_, angle_)
    outline(col, row, angle_, _color, cursor_size)
    if selected_p != -1 and getSqrIdx(col, row) in possible_moves[selected_p]:
        highlight_square(col, row, angle_, "")


def remove_hsquares(old_selected, angle_):
    global possible_moves
    for e in possible_moves[old_selected]:
        if e != getSqrIdx(cursor_col, cursor_row):
            remove_cursor(getCol(e), getRow(e), angle_)


def move_cursor(_to, angle_):
    global cursor_row, cursor_col
    remove_cursor(cursor_col, cursor_row, angle_)
    print_cursor(_to[0], _to[1], angle_)
    cursor_row = _to[1]
    cursor_col = _to[0]


def getCol(sqr_idx):
    return sqr_idx % 8


def getRow(sqr_idx):
    return sqr_idx // 8


def getPieceColor(s, c_board):
    if c_board[s] == "":
        return ""
    return c_board[s][0]


def isEmpty(s, c_board):
    return c_board[s] == ""


def canAttack(sqr_idx, to, c_board):
    return getPieceColor(sqr_idx, c_board) != getPieceColor(to, c_board)


def oppositeColor(color):
    if color == "": return color
    if color == "W":
        return "B"
    else:
        return "W"


def getPieceType(s, c_board):
    if c_board[s] == "":
        return ""
    return c_board[s][1]


def print_possible_moves(idx, angle_):
    global board, possible_moves
    for case_ in possible_moves[idx]:
        highlight_square(getCol(case_), getRow(case_), angle_, board)



def gen_knight_moves(sqr_idx, c_board):
    moves = []
    col, row = getCol(sqr_idx), getRow(sqr_idx)
    for offset in [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [-2, 1], [2, -1], [-2, -1]]:
        offset[0] += col
        offset[1] += row
        if inBoard(offset[0], offset[1]):
            if canAttack(sqr_idx, getSqrIdx(offset[0], offset[1]), c_board):
                moves.append(getSqrIdx(offset[0], offset[1]))
    return moves


def gen_pawn_moves(sqr_idx, c_board, last_move):
    moves = []
    col = getCol(sqr_idx)
    row = getRow(sqr_idx)
    color = getPieceColor(sqr_idx, c_board)
    if color == "W":
        mult = 1
    else:
        mult = -1
    if (row < 7 and color == "W") or (row > 0 and color == "B"):
        # forward
        if isEmpty(getSqrIdx(col, row + 1 * mult), c_board):
            moves.append(getSqrIdx(col, row + 1 * mult))
            # double forward
            if row == (-5 * mult + 7) // 2 and isEmpty(getSqrIdx(col, row + 2 * mult), c_board):
                # PROBABLEMENT UNE ERREUR ICI
                moves.append(getSqrIdx(col, row + 2 * mult))
        # attacks
        if inBoard(col - 1, row + 1 * mult):  # left
            if getPieceColor(sqr_idx + 8 * mult-1, c_board) == oppositeColor(color):
                moves.append(sqr_idx + 8 * mult-1)
        if inBoard(col + 1, row + 1 * mult):  # right
            if getPieceColor(sqr_idx + 8 * mult+1, c_board) == oppositeColor(color):
                moves.append(sqr_idx +1+ 8 * mult)
        # en passant
        if last_move != []:
            if row == (mult + 7) // 2 == getRow(last_move[1]) and last_move[0] == last_move[1] + 16 * mult and c_board[
                last_move[1]] == oppositeColor(color) + "P":
                if col == getCol(last_move[1]) + 1 * mult:
                    moves.append(sqr_idx + 7 * mult)
                if col == getCol(last_move[1]) - 1 * mult:
                    moves.append(sqr_idx + 9 * mult)
    return moves

def can_king_go(color_, c_board, from_, to_):
    if is_king_in_check(color_, c_board):
        return False
    c_board[from_], c_board[to_] = c_board[to_], c_board[from_]
    return not is_king_in_check(color_, c_board)

def gen_king_moves(sqr_idx, c_board, wq_castle, wk_castle, bq_castle, bk_castle):
    moves = []
    col, row = getCol(sqr_idx), getRow(sqr_idx)
    for offset in [[-1, -1], [-1, 0], [-1, 1], [0, 1], [0, -1], [1, -1], [1, 0], [1, 1]]:
        offset[0] += col
        offset[1] += row
        if inBoard(offset[0], offset[1]):
            if canAttack(sqr_idx, getSqrIdx(offset[0], offset[1]), c_board):
                moves.append(getSqrIdx(offset[0], offset[1]))
    if getPieceColor(sqr_idx, c_board) == "W":
        if sqr_idx == 4:
            if wk_castle and isEmpty(5, c_board) and isEmpty(6, c_board) and can_king_go("W", c_board[:], 4, 5): moves.append(6)
            if wq_castle and isEmpty(3, c_board) and isEmpty(2, c_board) and isEmpty(1, c_board) and can_king_go("W", c_board[:], 4, 3): moves.append(2)
    else:
        if sqr_idx == 60:
            if bk_castle and isEmpty(61, c_board) and isEmpty(62, c_board) and can_king_go("B", c_board[:], 60, 61): moves.append(62)
            if bq_castle and isEmpty(59, c_board) and isEmpty(58, c_board) and isEmpty(57, c_board) and can_king_go("B", c_board[:], 60, 59): moves.append(58)
    return moves


def gen_rook_moves(sqr_idx, c_board):
    moves = []
    color = getPieceColor(sqr_idx, c_board)
    for tpe in range(2):
        for i in [-1, 1]:
            col, row = getCol(sqr_idx) + i * tpe, getRow(sqr_idx) + i * (1 - tpe)
            while inBoard(col, row):
                if not isEmpty(getSqrIdx(col, row), c_board):
                    if getPieceColor(getSqrIdx(col, row), c_board) != color:
                        moves.append(getSqrIdx(col, row))
                    break
                moves.append(getSqrIdx(col, row))
                col += i * tpe
                row += i * (1 - tpe)
    return moves


def gen_bishop_moves(sqr_idx, c_board):
    moves = []
    color = getPieceColor(sqr_idx, c_board)
    for x in [-1, 1]:
        for y in [-1, 1]:
            col, row = getCol(sqr_idx) + x, getRow(sqr_idx) + y
            while inBoard(col, row):
                if not isEmpty(getSqrIdx(col, row), c_board):
                    if getPieceColor(getSqrIdx(col, row), c_board) != color:
                        moves.append(getSqrIdx(col, row))
                    break
                moves.append(getSqrIdx(col, row))
                col += x
                row += y
    return moves


def gen_queen_moves(sqr_idx, c_board):
    return gen_rook_moves(sqr_idx, c_board) + gen_bishop_moves(sqr_idx, c_board)

def draw_promotion_cursor(idx,old_idx):
    square_outline(10, 50 + old_idx * 20, color(100,100,100), cursor_size)
    if idx!=-1:
        square_outline(10,50+idx*20,cursor_color,cursor_size)


def promotion(color,angle):
    possibilities = ["Q","R","B","N"]
    idx=0
    fill_rect(5,45,30,90,(100,100,100))
    for piece in range(len(possibilities)):
        print_piece(pieces_imgs[color+possibilities[piece]],10,50+20*piece,angle)
    while not is_enter():
        idx1=(idx+is_down()-is_up())%len(possibilities)
        if idx1!=idx:
            draw_promotion_cursor(idx1,idx)
            idx=idx1
            sleep(COOLDOWN)
    fill_rect(5,45,30,90,(255,255,255))
    return color+possibilities[idx]

def play_move(c_board, selected, cursor_c, cursor_r, angle,
              graphic):  # graphic = boolean qui fait la partie graphique ou non
    global castles, played_moves


    from_ = c_board[selected]
    to = c_board[getSqrIdx(cursor_c, cursor_r)]

    if graphic:
        for sq, i in ((0, 0), (7, 1), (56, 2), (63, 3)):
            if selected == sq or getSqrIdx(cursor_c, cursor_r) == sq:
                castles[i] = 0
                
    #PROMOTION
    trans = from_
    if len(from_)==2 and from_[1]=="P" and cursor_r==(7*(from_[0]=="W")) and graphic :
        trans=promotion(from_[0],angle)
        c_board[selected]=trans

    if graphic:
        move_piece((getCol(selected), getRow(selected)), (cursor_c, cursor_r), angle,trans)

    # EN PASSANT
    if len(from_) == 2 and from_[1] == "P" and len(to) == 0 and getCol(selected) != cursor_c:
        c_board[getSqrIdx(cursor_c, getRow(selected))] = ""
        if graphic:
            clear_piece(cursor_c, getRow(selected), angle)
    # ROQUE
    if len(from_) == 2 and from_[1] == "K":
        if graphic:
            base = 0 if from_[0] == "W" else 2
            castles[base] = 0
            castles[base + 1] = 0
        if abs(cursor_c - getCol(selected)) >= 2:
            rook_col = 7 if cursor_c > getCol(selected) else 0
            from_rook_pos = (rook_col, getRow(selected))
            to_rook_pos = (int((getCol(selected) + cursor_c) / 2), cursor_r)
            rook_type = "W" * (cursor_r == 0) + "B" * (cursor_r == 7) + "R"
            if graphic:
                move_piece(from_rook_pos, to_rook_pos, angle, rook_type)
            c_board[getSqrIdx(from_rook_pos[0], from_rook_pos[1])], c_board[
                getSqrIdx(to_rook_pos[0], to_rook_pos[1])] = "", c_board[getSqrIdx(from_rook_pos[0], from_rook_pos[1])]

    c_board[getSqrIdx(cursor_c, cursor_r)] = c_board[selected]
    c_board[selected] = ""


    return c_board


def is_king_in_check(color, c_board):
    if color == "":
        return False
    sqr_idx = c_board.index(color + "K")
    opponentColor = oppositeColor(color)
    # knight checks
    moves = gen_knight_moves(sqr_idx, c_board)
    for move in moves:
        if c_board[move] == opponentColor + "N":
            return True
    # bishop or queen checks
    moves = gen_bishop_moves(sqr_idx, c_board)
    for move in moves:
        if c_board[move] == opponentColor + "B" or c_board[move] == opponentColor + "Q":
            return True
    # rook checks
    moves = gen_rook_moves(sqr_idx, c_board)
    for move in moves:
        if c_board[move] == opponentColor + "R" or c_board[move] == opponentColor + "Q":
            return True
    # king checks
    moves = gen_king_moves(sqr_idx, c_board, 0, 0, 0, 0)
    for move in moves:
        if c_board[move] == opponentColor + "K":
            return True
    # pawn checks
    if color == "W":
        mult = 1
    else:
        mult = -1
    col = getCol(sqr_idx)
    row = getRow(sqr_idx)
    if inBoard(col - 1, row + 1 * mult):  # left
        if c_board[sqr_idx + 7 * mult] == opponentColor + "P":
            return True
    if inBoard(col + 1, row + 1 * mult):  # right
        if c_board[sqr_idx + 9 * mult] == opponentColor + "P":
            return True
    return False


def find_possible_moves(c_board):
    global castles
    moves = []
    for idx in range(len(c_board)):
        piece = getPieceType(idx, c_board)
        color_ = getPieceColor(idx, c_board)
        cu = []
        if piece == "":
            moves.append([])
            continue
        elif piece == "R":
            cu = gen_rook_moves(idx, c_board)
        elif piece == "N":
            cu = gen_knight_moves(idx, c_board)
        elif piece == "P":
            cu = gen_pawn_moves(idx, c_board, [played_moves[-1][0], played_moves[-1][1]])
        elif piece == "B":
            cu = gen_bishop_moves(idx, c_board)
        elif piece == "Q":
            cu = gen_queen_moves(idx, c_board)
        elif piece == "K":
            cu = gen_king_moves(idx, c_board, castles[0], castles[1], castles[2], castles[3])
        moves.append(
            [i for i in cu if not (is_king_in_check(color_, play_move(c_board[:], idx, getCol(i), getRow(i), 0, False)))])
    return moves


def change_playing_color(angle):
    global playing_color, possible_moves
    if playing_color == "W":
        playing_color = "B"
        move_cursor((4, 4), angle)
    elif playing_color == "B":
        playing_color = "W"
        move_cursor((3, 3), angle)
    possible_moves = find_possible_moves(board)

def can_move(color,possible_moves_,c_board):
    for i in range(len(possible_moves_)):
        if getPieceColor(i,c_board)==color and len(possible_moves_[i])!=0:
            return True
    return False


ok_pressed = 0
move_cd = 0


def input_engine(angle):
    global cursor_row, cursor_col, move_cd, COOLDOWN, ok_pressed, playing_color, selected_p, possible_moves, played_moves, board
    if is_enter() and ok_pressed == 0:
        ok_pressed = 1
        piece__ = board[getSqrIdx(cursor_col, cursor_row)]
        if selected_p != -1 and getSqrIdx(cursor_col, cursor_row) in possible_moves[selected_p]:
            board = play_move(board, selected_p, cursor_col, cursor_row, angle, True)
            selected_old = selected_p
            selected_p = -1
            remove_hsquares(selected_old, angle)
            played_moves += [(selected_old, getSqrIdx(cursor_col, cursor_row), board[selected_p])]
            change_playing_color(angle)
            if not can_move(playing_color, possible_moves, board):
                return True

        else:
            sel_old = selected_p
            selected_p = -1
            remove_hsquares(sel_old, angle)
            if piece__ != "" and piece__[0] == playing_color:
                selected_p = getSqrIdx(cursor_col, cursor_row)
                print_possible_moves(selected_p, angle)

    else:
        ok_pressed = 0
    if move_cd + COOLDOWN > monotonic():
        return
    right_left = int((is_right() - is_left()) * 2 * (int(angle < 2) - 0.5))
    up_down = int((is_up() - is_down()) * 2 * (int(angle < 2) - 0.5))
    if angle % 2 == 1:
        right_left, up_down = up_down, -right_left
    if right_left != 0 and 7 >= cursor_col + right_left >= 0:
        move_cursor((cursor_col + right_left, cursor_row), angle)
        move_cd = monotonic()
    if up_down != 0 and 7 >= cursor_row + up_down >= 0:
        move_cursor((cursor_col, cursor_row + up_down), angle)
        move_cd = monotonic()

def game_ends(playing):
    if is_king_in_check(playing,board):
        draw_string((playing=="B")*"WHITE"+(playing=="W")*"BLACK"+" WON",115,50)
        draw_string("by checkmate",100,100)
    else:
        draw_string("DRAW",140,50)
        draw_string("by stalemate",100,100)


    return

def init():
    global board, board_init, angle,possible_moves
    board = board_init
    print_board(angle)
    for e in range(len(board)):
        col = getCol(e)
        row = getRow(e)
        co = getCoords(row, col, angle)
        type_ = pieces_imgs[board[e]]
        print_piece(type_, co[0], co[1], angle)
    print_cursor(0, 0, angle)
    possible_moves = find_possible_moves(board)


import time
init()
start = time.monotonic()
#while time.monotonic() < 120 + start:
while True:
    if input_engine(angle):
        game_ends(playing_color)
        break