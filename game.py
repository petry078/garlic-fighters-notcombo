# Imports
import pgzrun
from random import randint

# Constants
TITLE = "Garlic Fighters Notcombo"
WIDTH = 600
HEIGHT = 400

# Actors
bg = Actor("background_image", (WIDTH // 2, HEIGHT // 2))

# Vampire animation frames
vampire_frames = ["vampire_a", "vampire_b"]  # Add all frames here
vampire = Actor(vampire_frames[0])  # Start with the first frame

# Animation control variables
vampire_frame_index = 0
vampire_frame_delay = 60  # Delay in frames (1 second if running at 60 FPS)

# Global variables
velocity = 5
enemies = []
timer = 0
enemy_interval = 0.5
over = False
music_on = True
game_started = False

# Buttons
start_button = Rect((WIDTH // 2 - 50, HEIGHT // 2 - 60), (100, 30))
toggle_music_button = Rect((WIDTH // 2 - 50, HEIGHT // 2), (100, 30))
exit_button = Rect((WIDTH // 2 - 50, HEIGHT // 2 + 60), (100, 30))

# Start function
def start():
    global timer, velocity, enemy_interval, over, game_started
    vampire.pos = (WIDTH // 2, HEIGHT // 2)
    over = False
    timer = 0
    velocity = 5
    enemy_interval = 1.0
    enemies.clear()
    game_started = True
    clock.schedule_interval(increment_timer, 1.0)
    clock.schedule_interval(spawn_enemy, enemy_interval)
    clock.schedule_interval(speed_up, 1.0)
    spawn_enemy()

# Toggle music function
def toggle_music():
    global music_on
    if music_on:
        music.stop()
    else:
        music.play("background_music")
    music_on = not music_on

# Music
music.play("freaky_halloween")

# Make enemies faster
def speed_up():
    global enemy_interval
    enemy_interval -= enemy_interval * 0.05
    clock.unschedule(spawn_enemy)
    clock.schedule_interval(spawn_enemy, enemy_interval)

# Game over function
def game_over():
    global over
    over = True
    clock.schedule_unique(start, 3.5)
    clock.unschedule(increment_timer)
    clock.unschedule(spawn_enemy)
    clock.unschedule(speed_up)
    enemies.clear()
    clock.schedule_unique(game_over_sound, sounds.eep.get_length())

# Play Game over sound
def game_over_sound():
    sounds.gameover.play()

# Counter increment
def increment_timer():
    global timer
    timer += 1

# Creates new enemies
def spawn_enemy():
    enemy = Actor("enemy")
    enemy.x = randint(0, 1) * WIDTH
    enemy.y = randint(100, HEIGHT - 100)
    if enemy.x == 0:
        enemy.velocity_x = randint(2, 6)
    else:
        enemy.velocity_x = randint(-6, -2)
    enemy.velocity_y = randint(-6, 6)
    enemies.append(enemy)

# Draw function
def draw():
    screen.clear()
    if game_started:
        bg.draw()
        vampire.draw()
        for enemy in enemies:
            enemy.draw()
        screen.draw.text(f"Time: {timer}", midtop=(WIDTH // 2, 10))
        if over:
            screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2))
    else:
        screen.draw.text(TITLE, center=(WIDTH // 2, HEIGHT // 2 - 100), fontsize=50)
        screen.draw.filled_rect(start_button, "green")
        screen.draw.text("Start", center=start_button.center, fontsize=30)
        screen.draw.filled_rect(toggle_music_button, "blue")
        screen.draw.text("Music", center=toggle_music_button.center, fontsize=30)
        screen.draw.filled_rect(exit_button, "red")
        screen.draw.text("Exit", center=exit_button.center, fontsize=30)

# Update game frame
def update():
    global vampire_frame_index, vampire_frame_delay
    if game_started:
        if keyboard.LEFT and vampire.left > 0:
            vampire.x -= velocity
            vampire.image = "vampire_left"
        elif keyboard.RIGHT and vampire.right < WIDTH:
            vampire.x += velocity
            vampire.image = "vampire_right"
        elif keyboard.UP and vampire.top > 0:
            vampire.y -= velocity
        elif keyboard.DOWN and vampire.bottom < HEIGHT:
            vampire.y += velocity

        # Update vampire animation frames with 1-second delay
        if vampire_frame_delay == 0:
            vampire_frame_index = (vampire_frame_index + 1) % len(vampire_frames)
            vampire.image = vampire_frames[vampire_frame_index]
            vampire_frame_delay = 60  # Reset delay (1 second at 60 FPS)
        else:
            vampire_frame_delay -= 1

        for enemy in enemies:
            enemy.x += enemy.velocity_x
            enemy.y += enemy.velocity_y
            enemy.angle += 5
            if (
                enemy.top > HEIGHT
                or enemy.bottom < 0
                or enemy.left > WIDTH
                or enemy.right < 0
            ):
                enemies.remove(enemy)

        # Collision detection
        for enemy in enemies:
            if vampire.colliderect(enemy):
                enemies.remove(enemy)
                sounds.eep.play()
                if not over:
                    game_over()

# Change vampire image back to idle on key release
def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        vampire.image = vampire_frames[vampire_frame_index]  # Go back to animated frames

# Handle mouse clicks
def on_mouse_down(pos):
    if start_button.collidepoint(pos):
        start()
    elif toggle_music_button.collidepoint(pos):
        toggle_music()
    elif exit_button.collidepoint(pos):
        quit()

# Start with menu screen
pgzrun.go()
