import simplegui
import random

global turn
turn = 0

def new_game():
    global card_deck, exposed, pos_2, pos_1, state, click_1, click_2, turn
    pos_1 = [0,0]
    pos_2 = [0,0]
    state = 0
    first = 0
    turn = 0
    text = "Turns: "+str(turn)
    label.set_text(text)
    click_1 = 99
    click_2 = 99
    card_deck = range(8)+range(8) 
    random.shuffle(card_deck)
    
    exposed = []
    for i in range(len(card_deck)):
        exposed.append('FALSE')
    
    
def reset():
    global card_deck, exposed, pos_2, pos_1, state, click_1, click_2
    pos_1 = [0,0]
    pos_2 = [0,0]
    state = 0
    first = 0
    for i in range(len(card_deck)):
        if exposed[i] == 'TRUE':
            exposed[i] = 'FALSE'
            
    if card_deck[click_1] == card_deck[click_2]:
        exposed[click_1] = 'DONE'
        exposed[click_2] = 'DONE'
        
    click_1 = 99
    click_2 = 99  

     
def mouseclick(pos):
    global card_deck, exposed, pos_1, pos_2, state, first, turn, click_1, click_2
    
    for i in range(len(card_deck)):
            if (pos[0] <= 50*i+50 and pos[1] <= 100 and pos[0] >= 50*i and pos[1] >= 0):
                if exposed[i] <> 'FALSE':
                    return
           
    if state == 0:
        state = 1
        first = 1
        pos_1 = pos
    elif state == 1:
        state = 2
        first = 0
        pos_2 = pos
        turn += 1
        text = "Turns: "+str(turn)
        label.set_text(text)
    else:
        reset()
        state = 1
        pos_1 = pos
        
    if state == 0:
        for j in range(len(card_deck)):
            canvas.draw_polygon(([50*j,0],[50*j+50,0],[50*j+50,100],[50*j,100]),
                                0.5,"Black","Green")
    if state == 1:
        for i in range(len(card_deck)):
            if (pos_1[0] <= 50*i+50 and pos_1[1] <= 100 and pos_1[0] >= 50*i and pos_1[1] >= 0):
                click_1 = i
                if exposed[i] == 'FALSE':
                    exposed[i] = 'TRUE'
                
    if state == 2:
        for i in range(len(card_deck)):
            if (pos_2[0] <= 50*i+50 and pos_2[1] <= 100 and pos_2[0] >= 50*i and pos_2[1] >= 0):
                click_2 = i
                if exposed[i] == 'FALSE':
                    exposed[i] = 'TRUE'
                        
def draw(canvas):
    global card_deck, exposed, pos_1, pos_2, state, click_1, click_2
                   
    for j in range(len(card_deck)):
        if (exposed[j] == 'FALSE'):
            canvas.draw_polygon(([50*j,0],[50*j+50,0],[50*j+50,100],[50*j,100]),0.5,"Black","Green")
        else:
            canvas.draw_text(str(card_deck[j]),[50*j+15,60],30,"White")

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("")

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()