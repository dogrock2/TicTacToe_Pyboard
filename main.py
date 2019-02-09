import lcd160cr
import time

lcd = lcd160cr.LCD160CR('X')

player1_score = 0
player2_score = 0
msg = 'Player 1 turn'
touch_cnt = 0
touch_flg = 0
player1_turn = True
touch_coor = ((0,5,35,10,40),(1,45,80,10,40),(2,90,120,10,40),(3,5,35,50,75),(4,45,80,50,75),(5,90,1202,50,75),(6,5,35,85,115),(7,45,80,85,115),(8,90,120,85,115))
circle_coor = ((20,25),(63,25),(105,25),(20,63),(63,63),(105,63),(20,99),(63,99),(105,99))
x_coor = (((5,15,36,40),(36,15,5,40)),((45,15,80,40),(80,15,45,40)),((89,15,121,40),(121,15,89,40)),((5,50,36,75),(36,50,5,75)),((45,50,80,75),(80,50,45,75)),((89,50,121,75),(121,50,89,75)),((5,85,36,110),(36,85,5,110)),((45,85,80,110),(80,85,45,110)),((89,85,121,110),(121,85,89,110)))
positions = [False,False,False,False,False,False,False,False,False]
x_used = []
o_used = []
pos_set = ['n','n','n','n','n','n','n','n','n']
to_reset = False

def draw_static(ply1, ply2, mesg):    
    global x_used
    global o_used
    global circle_coor
    global x_coor
    lcd.erase()
    lcd.set_pos(41,1)
    lcd.write("TIC TAC TOE") #Display Title
    lcd.set_pos(0,0)
    lcd.line(40,10,40,115) #Draws the left vertical line
    lcd.line(85,10,85,115) #Draws the right vertical line
    lcd.line(3,45,123,45)  #Draws the top horizontal line
    lcd.line(3,80,123,80)  #Draws the bottom horizontal line
    lcd.set_pos(39,124)
    lcd.write(mesg) #Display message
    lcd.set_pos(5,139)
    lcd.write('PLAYER 1: '+str(ply1))  #Display player 1 score
    lcd.set_pos(5,148)
    lcd.write('PLAYER 2: '+str(ply2))  #Display player 2 score
    for i in x_used:
        draw_x(x_coor[i][0],x_coor[i][1])
    for y in o_used:
        draw_circle(*circle_coor[y])


def draw_x(coor1,coor2):
    lcd.line(*coor1)
    lcd.line(*coor2)

def draw_circle(x, y):
        
        x = int(x)
        y = int(y)
        radius = 13
        
        f = 1 - radius
        val_x = 1
        val_y = -2 * radius
        x1 = 0
        y1 = radius

        lcd.dot(x, y + radius)
        lcd.dot(x, y - radius)
        lcd.dot(x + radius, y)
        lcd.dot(x - radius, y)

        while x1 < y1:
            if f >= 0:
                y1 -= 1
                val_y += 2
                f += val_y
            x1 += 1
            val_x += 2
            f += val_x
            lcd.dot(x + x1, y + y1)
            lcd.dot(x - x1, y + y1)
            lcd.dot(x + x1, y - y1)
            lcd.dot(x - x1, y - y1)
            lcd.dot(x + y1, y + x1)
            lcd.dot(x - y1, y + x1)
            lcd.dot(x + y1, y - x1)
            lcd.dot(x - y1, y - x1)

lcd.erase()
draw_static(player1_score, player2_score, msg)

def reset():
    global player1_score
    global player2_score
    global player1_turn
    global touch_cnt
    global to_reset
    global positions
    global x_used
    global o_used
    global pos_set
    
    msg = 'Player 1 turn'
    touch_cnt = 0
    player1_turn = True
    positions = [False,False,False,False,False,False,False,False,False]
    x_used = []
    o_used = []
    pos_set = ['n','n','n','n','n','n','n','n','n']
    to_reset = False
    draw_static(player1_score, player2_score, msg)


def check_winner():
    global pos_set
    global touch_cnt
    combo1 = (1,4,7,1,2,3,3,1)
    combo2 = (2,5,8,4,5,6,5,5)
    combo3 = (3,6,9,7,8,9,7,9)

    for i in range(8):
        if pos_set[combo1[i]-1] == 'x' and pos_set[combo2[i]-1] == 'x' and pos_set[combo3[i]-1] == 'x':
            return 1
        if pos_set[combo1[i]-1] == 'o' and pos_set[combo2[i]-1] == 'o' and pos_set[combo3[i]-1] == 'o':
            return 2
        if touch_cnt > 8:
            return 3    

    return 0


def draw_touch(pos):
    global player1_turn
    global player1_score
    global player2_score
    global pos_set
    global touch_cnt
    global to_reset
    
    if player1_turn and not positions[pos]:
        touch_cnt += 1
        positions[pos] = True
        x_used.append(pos)
        pos_set[pos] = 'x'
        player1_turn = not player1_turn
        chk_winner = check_winner()
        if chk_winner == 1:
            msg = 'Player 1 wins'
            player1_score += 1
            to_reset = True
        elif chk_winner == 3:
            msg = 'Game Tied!'
            to_reset = True
        else:
            msg = 'Player 2 turn'        
        draw_static(player1_score, player2_score, msg) 
    elif not player1_turn and not positions[pos]:
        touch_cnt += 1 
        positions[pos] = True
        o_used.append(pos)
        pos_set[pos] = 'o'
        player1_turn = not player1_turn
        chk_winner = check_winner()
        if chk_winner == 2:
            msg = 'Player 2 wins'
            player2_score += 1
            to_reset = True
        elif chk_winner == 3:
            msg = 'Game Tied!'
            to_reset = True
        else:
            msg = 'Player 1 turn'         
        draw_static(player1_score, player2_score, msg) 

    

while True:

    touched, x, y = lcd.get_touch()

    if touched and touch_flg == 0:
        if to_reset:
            reset()
        else:
            touch_flg += 1
            for coors in touch_coor:
                if (x >= coors[1] and x <= coors[2]) and (y >= coors[3] and y <= coors[4]):  
                    draw_touch(coors[0])
    
    if touched == False and touch_flg > 0:
        touch_flg = 0    
    
    time.sleep_ms(50)


