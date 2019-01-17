import lcd160cr

lcd = lcd160cr.LCD160CR('X')

player1_score = 0
player2_score = 0
msg = ''

def draw_static(ply1, ply2, mesg):    
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

lcd.erase()
draw_static(player1_score, player2_score, msg)

touched = False
touch_cnt = 0
test_cnt = 0

while True:
    touched = lcd.is_touched()
    if touched == True and touch_cnt == 0:
        msg = 'LCD touched'
        touch_cnt += 1
    
    if touched == False and touch_cnt > 0:
        touch_cnt = 0
        test_cnt += 1
        draw_static(test_cnt, player2_score, msg)

# X = 0-128
# Y = 0 - 160

#line1 =    lcd.line(40,10,40,115)
#line2 =    lcd.line(85,10,85,115)

#line3 =    lcd.line(3,45,123,45)
#line4 =    lcd.line(3,80,123,80)


