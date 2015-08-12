# Implementation of classic arcade game Pong

# requires SimpleGUICS2Pygame module

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = 200
paddle1_vel = 0
paddle2_pos = 200
paddle2_vel = 0
ball_vel = [0,0]
ball_pos = [0,0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300,200]
    if direction == RIGHT:
        ball_vel = [random.randrange(2,4), -(random.randrange(1,3))]
    else:
        ball_vel = [-(random.randrange(2,4)), -(random.randrange(1,3))]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0 
    score2 = 0
    paddle1_pos = 200
    paddle2_pos = 200
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball    
    if ball_pos[0] >= (((WIDTH -1) - PAD_WIDTH) - BALL_RADIUS):
        if ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle2_pos - HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] * 1.1)
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT) and ball_pos[1] >= (paddle1_pos - HALF_PAD_HEIGHT):
            ball_vel[0] = -(ball_vel[0] * 1.1)
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    if ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS) or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1,'White', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel - HALF_PAD_HEIGHT) > 0 and (paddle1_pos + paddle1_vel + HALF_PAD_HEIGHT) < (HEIGHT - 1):
        paddle1_pos = paddle1_pos + paddle1_vel
    if (paddle2_pos + paddle2_vel - HALF_PAD_HEIGHT) > 0 and (paddle2_pos + paddle2_vel + HALF_PAD_HEIGHT) < (HEIGHT - 1):
        paddle2_pos = paddle2_pos + paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([(0,(paddle1_pos+HALF_PAD_HEIGHT)),((PAD_WIDTH-1),(paddle1_pos+HALF_PAD_HEIGHT)),((PAD_WIDTH-1),(paddle1_pos-HALF_PAD_HEIGHT)),(0,(paddle1_pos-HALF_PAD_HEIGHT))],4,'White', 'White')
    canvas.draw_polygon([(((WIDTH+1)-PAD_WIDTH),(paddle2_pos+HALF_PAD_HEIGHT)),((WIDTH),(paddle2_pos+HALF_PAD_HEIGHT)),((WIDTH),(paddle2_pos-HALF_PAD_HEIGHT)),(((WIDTH+1)-PAD_WIDTH),(paddle2_pos-HALF_PAD_HEIGHT))],4,'White', 'White')
    
    # draw scores
    canvas.draw_text(str(score1),[WIDTH/3,40] , 30, 'White', 'monospace')
    canvas.draw_text(str(score2),[(WIDTH/3)*2,40] , 30, 'White', 'monospace')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 3
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += 3
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += 3
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += 3
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel -= 3
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel += 3
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel -= 3

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('New Game', new_game, 100)


# start frame
new_game()
frame.start()

# There we go, a rendition of Allan Alcorn's arcade classic, Pong.
# If you're interested, check out possibly the earliest arcade-style game, Spacewar! at http://spacewar.oversigma.com/