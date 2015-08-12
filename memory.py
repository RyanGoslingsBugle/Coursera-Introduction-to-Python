# implementation of card game - Memory

# requires SimpleGUICS2Pygame module

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

CARD_LIST = []
exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
game_state = 0
check1 = 0
check2 = 0
turn_count = 0

# helper function to initialize globals
def new_game():
    global CARD_LIST, game_state, exposed, turn_count
    CARD_LIST = (range(8))
    CARD_LIST.extend(range(8))
    random.shuffle(CARD_LIST)
    game_state = 0
    turn_count = 0
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global game_state, check1, check2, turn_count
    clicked_card = pos[0] / 50
    if game_state == 0:
        if exposed[clicked_card] == False:
            exposed[clicked_card] = True
            check1 = clicked_card
            game_state = 1
    elif game_state == 1:
        if exposed[clicked_card] == False:
            exposed[clicked_card] = True
            check2 = clicked_card
            game_state = 2
            turn_count += 1
    else:
        if exposed[clicked_card] == False:
            exposed[clicked_card] = True
            if CARD_LIST[check1] != CARD_LIST[check2]:
                exposed[check1] = False
                exposed[check2] = False
            check1 = clicked_card
            game_state = 1
        
# cards are logically 50x100 pixels in size  
def draw(canvas):
    global exposed
    count = 0
    for card_number in CARD_LIST:
        if exposed[count]:
            canvas.draw_text(str(card_number),[(count * 50 + 25),50],20,"White")
        else:
            canvas.draw_polygon([[count * 50, 0],
                                 [count * 50 + 50, 0],
                                 [count * 50 + 50, 100], 
                                 [count * 50, 100]], 1, "Black", "Green")
        count += 1
    label.set_text('Turns = ' + str(turn_count))
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric