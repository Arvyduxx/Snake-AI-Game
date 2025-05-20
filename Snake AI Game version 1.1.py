import tkinter as tk
import random

# Game settings
snake_size = 20
canvas_width = 400
canvas_height = 400
initial_speed = 150  # Initial speed of the snake
speed = initial_speed
score = 0
high_score = 0  # Initialize high score
direction = "Right"
snake = [(20, 20), (20, 19), (20, 18)]  # Initial snake position
food_position = None
game_over = False
mode = "Classic"  # Start in Classic Mode

# Initialize the game window with custom title
root = tk.Tk()
root.title("Snake AI Game")  # Change window title to "Snake AI Game"
root.config(bg="black")


# Create the canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# Create score and high score labels with black background and red text
score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), fg="red", bg="black")
score_label.pack()

high_score_label = tk.Label(root, text="High Score: 0", font=("Arial", 14), fg="red", bg="black")
high_score_label.pack()


# Create the food
def create_food():
    global food_position
    food_position = (random.randint(0, (canvas_width - snake_size) // snake_size) * snake_size,
                     random.randint(0, (canvas_height - snake_size) // snake_size) * snake_size)
    canvas.create_rectangle(food_position[0], food_position[1], food_position[0] + snake_size, food_position[1] + snake_size, fill="red", tags="food")

# Draw the snake
def draw_snake():
    canvas.delete("snake")
    for segment in snake:
        canvas.create_rectangle(segment[0], segment[1], segment[0] + snake_size, segment[1] + snake_size, fill="green", tags="snake")

# Update the score
def update_score():
    score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), fg="red", bg="black")  # Set score label text to red and background to black
high_score_label = tk.Label(root, text="High Score: 0", font=("Arial", 14), fg="red", bg="black")  # High score label with red text


# Move the snake
def move_snake():
    global game_over, score, food_position, speed, canvas_width, canvas_height, high_score
    if game_over:
        return

    head = snake[0]
    if direction == "Up":
        new_head = (head[0], head[1] - snake_size)
    elif direction == "Down":
        new_head = (head[0], head[1] + snake_size)
    elif direction == "Left":
        new_head = (head[0] - snake_size, head[1])
    elif direction == "Right":
        new_head = (head[0] + snake_size, head[1])

    # Hard Mode behavior - shrinking canvas and increasing speed
    if mode == "Hard":
        # Check for collision with walls (borders)
        if new_head[0] < 0 or new_head[0] >= canvas_width or new_head[1] < 0 or new_head[1] >= canvas_height:
            game_over = True
            canvas.create_text(canvas_width // 2, canvas_height // 2, text="Game Over", fill="white", font=("Arial", 24))
            return

    # In Unlimited Mode, the snake doesn't die when it hits the wall
    if mode == "Unlimited":
        if new_head[0] < 0:
            new_head = (canvas_width - snake_size, new_head[1])
        elif new_head[0] >= canvas_width:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], canvas_height - snake_size)
        elif new_head[1] >= canvas_height:
            new_head = (new_head[0], 0)

    # In Classic Mode, the snake dies if it hits the border
    if mode == "Classic":
        if new_head[0] < 0 or new_head[0] >= canvas_width or new_head[1] < 0 or new_head[1] >= canvas_height:
            game_over = True
            canvas.create_text(canvas_width // 2, canvas_height // 2, text="Game Over", fill="white", font=("Arial", 24))
            return

    # Move the snake
    snake.insert(0, new_head)

    # Check if the snake eats food
    if new_head == food_position:
        score += 10
        update_score()
        canvas.delete("food")  # Remove the food from the canvas
        create_food()  # Spawn new food at a random position
        
        # In Hard Mode: Increase the speed of the snake
        speed = max(50, speed - 5)  # Speed can't go below 50ms
        
        # In Hard Mode: Shrink the borders by 15px on each side
        if mode == "Hard":
            canvas_width = max(200, canvas_width - 15)
            canvas_height = max(200, canvas_height - 15)
            canvas.config(width=canvas_width, height=canvas_height)

        # Update high score if needed
        if score > high_score:
            high_score = score
            update_score()

    else:
        # Remove the tail if snake hasn't eaten food
        snake.pop()

    draw_snake()

# Change direction based on key press
def change_direction(event):
    global direction
    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"

# Restart the game
def restart_game():
    global score, snake, direction, game_over, food_position, mode, speed, canvas_width, canvas_height
    score = 0
    snake = [(20, 20), (20, 19), (20, 18)]
    direction = "Right"
    game_over = False
    speed = initial_speed  # Reset speed to initial speed on restart
    canvas_width = 400
    canvas_height = 400
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.delete("all")
    score_label.config(text="Score: 0")
    create_food()
    draw_snake()
    game_loop()

# Set game mode
def set_mode(selected_mode):
    global mode, score, snake, direction, food_position, game_over, speed, canvas_width, canvas_height
    mode = selected_mode
    score = 0
    snake.clear()
    snake.extend([(20, 20), (20, 19), (20, 18)])
    direction = "Right"
    game_over = False
    speed = initial_speed  # Reset speed to initial speed when changing mode
    canvas_width = 400
    canvas_height = 400
    canvas.config(width=canvas_width, height=canvas_height)
    canvas.delete("all")
    score_label.config(text="Score: 0")
    create_food()
    draw_snake()
    game_loop()

# Game loop (move the snake every 'speed' ms)
def game_loop():
    if not game_over:
        move_snake()
        root.after(speed, game_loop)

# Set up the game
create_food()
draw_snake()
root.bind("<KeyPress>", change_direction)

# Buttons for mode selection
classic_button = tk.Button(root, text="Classic Mode", font=("Courier New", 12), command=lambda: set_mode("Classic"))
classic_button.pack()

unlimited_button = tk.Button(root, text="Unlimited Mode", font=("Courier New", 12), command=lambda: set_mode("Unlimited"))
unlimited_button.pack()

hard_button = tk.Button(root, text="Hard Mode", font=("Courier New", 12), command=lambda: set_mode("Hard"))
hard_button.pack()

# Restart button
restart_button = tk.Button(root, text="Restart", font=("Courier New", 12), command=restart_game)
restart_button.pack()

# Start the game loop
game_loop()

# Run the Tkinter event loop
root.mainloop()

