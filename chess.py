import pygame
import sys

pygame.init()
WIDTH = 600
HEIGHT = 600
BOARD_SIZE = 600
CAPTURED_AREA_WIDTH = 250  # Adjusted for labels and pieces to fit
STATUS_BAR_HEIGHT = 100    # Increased for timers and messages

screen = pygame.display.set_mode([WIDTH + CAPTURED_AREA_WIDTH, HEIGHT + STATUS_BAR_HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font(None, 24)
medium_font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 40)
timer = pygame.time.Clock()
fps = 60

# Initialize game variables
def initialize_game_variables():
    global white_pieces_list, white_locations, white_can_castle_kingside, white_can_castle_queenside
    global black_pieces_list, black_locations, black_can_castle_kingside, black_can_castle_queenside
    global captured_pieces_white, captured_pieces_black, turn_step, selection, valid_moves
    global en_passant_square, en_passant_target, in_check, winner, game_over
    global white_time, black_time, last_move_time

    white_pieces_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                         'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    white_can_castle_kingside = True
    white_can_castle_queenside = True

    black_pieces_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                         'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    black_can_castle_kingside = True
    black_can_castle_queenside = True

    captured_pieces_white = []
    captured_pieces_black = []
    turn_step = 0
    selection = None
    valid_moves = []
    en_passant_square = None
    en_passant_target = None
    in_check = False
    winner = ''
    game_over = False

    white_time = initial_time * 60 if time_controls_enabled else None
    black_time = initial_time * 60 if time_controls_enabled else None
    last_move_time = pygame.time.get_ticks()

# Load images
# Ensure that the image files are correctly named and placed in the 'assets' folder
black_queen = pygame.image.load('assets/black queen.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))
black_queen_small = pygame.transform.scale(black_queen, (30, 30))
black_king = pygame.image.load('assets/black king.png')
black_king = pygame.transform.scale(black_king, (60, 60))
black_king_small = pygame.transform.scale(black_king, (30, 30))
black_rook = pygame.image.load('assets/black rook.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))
black_rook_small = pygame.transform.scale(black_rook, (30, 30))
black_bishop = pygame.image.load('assets/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))
black_bishop_small = pygame.transform.scale(black_bishop, (30, 30))
black_knight = pygame.image.load('assets/black knight.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))
black_knight_small = pygame.transform.scale(black_knight, (30, 30))
black_pawn = pygame.image.load('assets/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (50, 50))
black_pawn_small = pygame.transform.scale(black_pawn, (30, 30))
white_queen = pygame.image.load('assets/white queen.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))
white_queen_small = pygame.transform.scale(white_queen, (30, 30))
white_king = pygame.image.load('assets/white king.png')
white_king = pygame.transform.scale(white_king, (60, 60))
white_king_small = pygame.transform.scale(white_king, (30, 30))
white_rook = pygame.image.load('assets/white rook.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))
white_rook_small = pygame.transform.scale(white_rook, (30, 30))
white_bishop = pygame.image.load('assets/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))
white_bishop_small = pygame.transform.scale(white_bishop, (30, 30))
white_knight = pygame.image.load('assets/white knight.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))
white_knight_small = pygame.transform.scale(white_knight, (30, 30))
white_pawn = pygame.image.load('assets/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (50, 50))
white_pawn_small = pygame.transform.scale(white_pawn, (30, 30))
white_images = [white_pawn, white_rook, white_knight, white_bishop, white_queen, white_king]
small_white_images = [white_pawn_small, white_rook_small, white_knight_small, white_bishop_small,
                      white_queen_small, white_king_small]
black_images = [black_pawn, black_rook, black_knight, black_bishop, black_queen, black_king]
small_black_images = [black_pawn_small, black_rook_small, black_knight_small, black_bishop_small,
                      black_queen_small, black_king_small]
piece_list = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

# Time controls
time_controls_enabled = False
initial_time = 5  # default 5 minutes
increment = 0

# Other game variables
counter = 0  # For check flashing effect

# Initialize game variables
initialize_game_variables()

# Function to reset the game
def reset_game():
    global time_controls_enabled
    time_controls_enabled = False
    initialize_game_variables()
    update_options()

# Function to start game with time
def start_game_with_time():
    global time_controls_enabled
    time_controls_enabled = True
    get_time_controls()
    initialize_game_variables()
    update_options()

# Function to get custom time controls
def get_time_controls():
    global initial_time, increment
    # Display a styled menu to enter time controls
    initial_time = 5  # Default values
    increment = 0
    input_box_time = pygame.Rect(350, 220, 140, 40)
    input_box_increment = pygame.Rect(350, 280, 140, 40)
    color_inactive = pygame.Color('gray')
    color_active = pygame.Color('dodgerblue')
    color_time = color_inactive
    color_increment = color_inactive
    active_time = False
    active_increment = False
    text_time = ''
    text_increment = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_time.collidepoint(event.pos):
                    active_time = True
                    active_increment = False
                elif input_box_increment.collidepoint(event.pos):
                    active_increment = True
                    active_time = False
                else:
                    active_time = False
                    active_increment = False
                color_time = color_active if active_time else color_inactive
                color_increment = color_active if active_increment else color_inactive
            if event.type == pygame.KEYDOWN:
                if active_time:
                    if event.key == pygame.K_RETURN:
                        active_time = False
                        color_time = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_time = text_time[:-1]
                    else:
                        if event.unicode.isdigit():
                            text_time += event.unicode
                if active_increment:
                    if event.key == pygame.K_RETURN:
                        active_increment = False
                        color_increment = color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        text_increment = text_increment[:-1]
                    else:
                        if event.unicode.isdigit():
                            text_increment += event.unicode
                if event.key == pygame.K_RETURN and not active_time and not active_increment:
                    done = True

        screen.fill((30, 30, 30))  # Dark background
        prompt_text = big_font.render('Enter Time Controls', True, 'white')
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 150))
        time_text = medium_font.render('Initial Time (min):', True, 'white')
        screen.blit(time_text, (150, 225))
        increment_text = medium_font.render('Increment (sec):', True, 'white')
        screen.blit(increment_text, (150, 285))

        # Render the current text.
        txt_surface_time = medium_font.render(text_time, True, 'white')
        txt_surface_increment = medium_font.render(text_increment, True, 'white')
        # Blit the input boxes and text.
        pygame.draw.rect(screen, color_time, input_box_time, 2)
        pygame.draw.rect(screen, color_increment, input_box_increment, 2)
        screen.blit(txt_surface_time, (input_box_time.x + 5, input_box_time.y + 5))
        screen.blit(txt_surface_increment, (input_box_increment.x + 5, input_box_increment.y + 5))

        pygame.display.flip()
        timer.tick(30)
    # Convert text inputs to integers
    initial_time = int(text_time) if text_time.isdigit() else 5
    increment = int(text_increment) if text_increment.isdigit() else 0

# Rest of the functions remain the same with necessary adjustments
# Draw main game board
def draw_board():
    square_size = BOARD_SIZE // 8
    colors = [(240, 217, 181), (181, 136, 99)]  # Light and dark squares
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
    # Draw status bar
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, HEIGHT, WIDTH + CAPTURED_AREA_WIDTH, STATUS_BAR_HEIGHT))
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    status_surface = big_font.render(status_text[turn_step], True, 'white')
    screen.blit(status_surface, (10, HEIGHT + 5))
    # Draw labels for captured pieces
    captured_white_label = medium_font.render('Captured White Pieces:', True, 'white')
    captured_black_label = medium_font.render('Captured Black Pieces:', True, 'white')
    screen.blit(captured_black_label, (WIDTH + 10, 10))
    screen.blit(captured_white_label, (WIDTH + 10, HEIGHT // 2 + 10))

def draw_pieces():
    square_size = BOARD_SIZE // 8
    for i in range(len(white_pieces_list)):
        piece = white_pieces_list[i]
        index = piece_list.index(piece)
        x, y = white_locations[i]
        img = white_images[index]
        img_rect = img.get_rect(center=(x * square_size + square_size // 2, y * square_size + square_size // 2))
        screen.blit(img, img_rect)
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'yellow', [x * square_size, y * square_size, square_size, square_size], 3)

    for i in range(len(black_pieces_list)):
        piece = black_pieces_list[i]
        index = piece_list.index(piece)
        x, y = black_locations[i]
        img = black_images[index]
        img_rect = img.get_rect(center=(x * square_size + square_size // 2, y * square_size + square_size // 2))
        screen.blit(img, img_rect)
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'yellow', [x * square_size, y * square_size, square_size, square_size], 3)

def draw_restart_button():
    button_rect = pygame.Rect(WIDTH + 10, HEIGHT - 90, CAPTURED_AREA_WIDTH - 20, 30)
    pygame.draw.rect(screen, (70, 70, 70), button_rect)
    restart_text = medium_font.render('Restart Game', True, 'white')
    text_rect = restart_text.get_rect(center=button_rect.center)
    screen.blit(restart_text, text_rect)
    return button_rect

def draw_play_with_time_button():
    button_rect = pygame.Rect(WIDTH + 10, HEIGHT - 50, CAPTURED_AREA_WIDTH - 20, 30)
    pygame.draw.rect(screen, (70, 70, 70), button_rect)
    play_text = medium_font.render('Play with Time', True, 'white')
    text_rect = play_text.get_rect(center=button_rect.center)
    screen.blit(play_text, text_rect)
    return button_rect

def draw_timers():
    if time_controls_enabled:
        white_timer_text = medium_font.render(f'White Time: {int(white_time // 60)}:{int(white_time % 60):02d}', True, 'white')
        black_timer_text = medium_font.render(f'Black Time: {int(black_time // 60)}:{int(black_time % 60):02d}', True, 'white')
        screen.blit(white_timer_text, (WIDTH + 10, HEIGHT + 5))
        screen.blit(black_timer_text, (WIDTH + 10, HEIGHT + 35))

def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        y_position = HEIGHT // 2 + 40 + i * 35
        screen.blit(small_black_images[index], (WIDTH + 10, y_position))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        y_position = 40 + i * 35
        screen.blit(small_white_images[index], (WIDTH + 10, y_position))

def draw_check():
    global counter
    counter = (counter + 1) % 30
    square_size = BOARD_SIZE // 8
    if turn_step < 2:
        if is_king_in_check(white_pieces_list, white_locations, 'white', black_pieces_list, black_locations):
            king_index = white_pieces_list.index('king')
            king_position = white_locations[king_index]
            if counter < 15:
                pygame.draw.rect(screen, 'red', [king_position[0] * square_size, king_position[1] * square_size, square_size, square_size], 5)
    else:
        if is_king_in_check(black_pieces_list, black_locations, 'black', white_pieces_list, white_locations):
            king_index = black_pieces_list.index('king')
            king_position = black_locations[king_index]
            if counter < 15:
                pygame.draw.rect(screen, 'red', [king_position[0] * square_size, king_position[1] * square_size, square_size, square_size], 5)

def draw_valid(moves):
    square_size = BOARD_SIZE // 8
    for move in moves:
        pygame.draw.circle(screen, (0, 255, 0), (move[0] * square_size + square_size // 2, move[1] * square_size + square_size // 2), 10)

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

# Functions for checking moves and game logic
def update_options():
    global black_options, white_options
    black_options = check_options(black_pieces_list, black_locations, 'black', white_pieces_list, white_locations,
                                  black_can_castle_kingside, black_can_castle_queenside)
    white_options = check_options(white_pieces_list, white_locations, 'white', black_pieces_list, black_locations,
                                  white_can_castle_kingside, white_can_castle_queenside)

def check_options(pieces, locations, color, opponent_pieces, opponent_locations, can_castle_kingside, can_castle_queenside):
    moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves = check_pawn(location, color, locations, opponent_locations)
        elif piece == 'rook':
            moves = check_rook(location, color, locations, opponent_locations)
        elif piece == 'knight':
            moves = check_knight(location, color, locations)
        elif piece == 'bishop':
            moves = check_bishop(location, color, locations, opponent_locations)
        elif piece == 'queen':
            moves = check_queen(location, color, locations, opponent_locations)
        elif piece == 'king':
            moves = check_king(location, color, locations, opponent_locations, can_castle_kingside, can_castle_queenside)
        # Filter out moves that would put own king in check
        valid_moves = []
        for move in moves:
            # Simulate the move
            temp_pieces = pieces.copy()
            temp_locations = locations.copy()
            temp_locations[i] = move
            temp_opponent_pieces = opponent_pieces.copy()
            temp_opponent_locations = opponent_locations.copy()
            # Remove captured piece in simulation
            if move in opponent_locations:
                idx = opponent_locations.index(move)
                temp_opponent_pieces.pop(idx)
                temp_opponent_locations.pop(idx)
            if not is_king_in_check(temp_pieces, temp_locations, color, temp_opponent_pieces, temp_opponent_locations):
                valid_moves.append(move)
        moves_list.append(valid_moves)
    return moves_list

def is_king_in_check(pieces, locations, color, opponent_pieces, opponent_locations):
    king_index = pieces.index('king')
    king_position = locations[king_index]
    opponent_options = get_all_opponent_moves(opponent_pieces, opponent_locations, 'black' if color == 'white' else 'white', pieces, locations)
    for moves in opponent_options:
        if king_position in moves:
            return True
    return False

def get_all_opponent_moves(pieces, locations, color, opponent_pieces, opponent_locations):
    moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves = check_pawn(location, color, locations, opponent_locations)
        elif piece == 'rook':
            moves = check_rook(location, color, locations, opponent_locations)
        elif piece == 'knight':
            moves = check_knight(location, color, locations)
        elif piece == 'bishop':
            moves = check_bishop(location, color, locations, opponent_locations)
        elif piece == 'queen':
            moves = check_queen(location, color, locations, opponent_locations)
        elif piece == 'king':
            moves = check_king(location, color, locations, opponent_locations, False, False)
        moves_list.append(moves)
    return moves_list

def is_square_under_attack(square, color):
    if color == 'white':
        opponent_pieces = black_pieces_list
        opponent_locations = black_locations
        own_pieces = white_pieces_list
        own_locations = white_locations
    else:
        opponent_pieces = white_pieces_list
        opponent_locations = white_locations
        own_pieces = black_pieces_list
        own_locations = black_locations
    opponent_options = get_all_opponent_moves(opponent_pieces, opponent_locations, 'black' if color == 'white' else 'white', own_pieces, own_locations)
    for moves in opponent_options:
        if square in moves:
            return True
    return False

def check_king(position, color, friends_list, enemies_list, can_castle_kingside, can_castle_queenside):
    moves_list = []
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for dx, dy in targets:
        target = (position[0] + dx, position[1] + dy)
        if 0 <= target[0] <= 7 and 0 <= target[1] <= 7 and target not in friends_list:
            moves_list.append(target)
    # Castling
    if color == 'white' and position == (4, 7):
        if can_castle_kingside:
            if (5, 7) not in friends_list + enemies_list and (6, 7) not in friends_list + enemies_list:
                if not is_square_under_attack((4, 7), 'white') and not is_square_under_attack((5, 7), 'white') and not is_square_under_attack((6, 7), 'white'):
                    moves_list.append((6, 7))  # Kingside castling move
        if can_castle_queenside:
            if (1, 7) not in friends_list + enemies_list and (2, 7) not in friends_list + enemies_list and (3, 7) not in friends_list + enemies_list:
                if not is_square_under_attack((4, 7), 'white') and not is_square_under_attack((3, 7), 'white') and not is_square_under_attack((2, 7), 'white'):
                    moves_list.append((2, 7))  # Queenside castling move
    elif color == 'black' and position == (4, 0):
        if can_castle_kingside:
            if (5, 0) not in friends_list + enemies_list and (6, 0) not in friends_list + enemies_list:
                if not is_square_under_attack((4, 0), 'black') and not is_square_under_attack((5, 0), 'black') and not is_square_under_attack((6, 0), 'black'):
                    moves_list.append((6, 0))  # Kingside castling move
        if can_castle_queenside:
            if (1, 0) not in friends_list + enemies_list and (2, 0) not in friends_list + enemies_list and (3, 0) not in friends_list + enemies_list:
                if not is_square_under_attack((4, 0), 'black') and not is_square_under_attack((3, 0), 'black') and not is_square_under_attack((2, 0), 'black'):
                    moves_list.append((2, 0))  # Queenside castling move
    return moves_list

def check_queen(position, color, friends_list, enemies_list):
    moves_list = check_bishop(position, color, friends_list, enemies_list)
    moves_list += check_rook(position, color, friends_list, enemies_list)
    return moves_list

def check_bishop(position, color, friends_list, enemies_list):
    moves_list = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for dx, dy in directions:
        x, y = position
        while True:
            x += dx
            y += dy
            if 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) in friends_list:
                    break
                moves_list.append((x, y))
                if (x, y) in enemies_list:
                    break
            else:
                break
    return moves_list

def check_rook(position, color, friends_list, enemies_list):
    moves_list = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        x, y = position
        while True:
            x += dx
            y += dy
            if 0 <= x <= 7 and 0 <= y <= 7:
                if (x, y) in friends_list:
                    break
                moves_list.append((x, y))
                if (x, y) in enemies_list:
                    break
            else:
                break
    return moves_list

def check_knight(position, color, friends_list):
    moves_list = []
    # 8 squares to check for knights
    targets = [(2, 1), (1, 2), (-1, 2), (-2, 1),
               (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for dx, dy in targets:
        x, y = position[0] + dx, position[1] + dy
        if 0 <= x <= 7 and 0 <= y <= 7 and (x, y) not in friends_list:
            moves_list.append((x, y))
    return moves_list

def check_pawn(position, color, friend_locations, enemy_locations):
    moves_list = []
    if color == 'white':
        direction = -1  # Moving up the board
        start_row = 6
        opponent_pawns = [i for i, p in enumerate(black_pieces_list) if p == 'pawn']
        opponent_locations = black_locations
    else:
        direction = 1  # Moving down the board
        start_row = 1
        opponent_pawns = [i for i, p in enumerate(white_pieces_list) if p == 'pawn']
        opponent_locations = white_locations

    # Move forward one square
    forward_one = (position[0], position[1] + direction)
    if forward_one not in friend_locations + enemy_locations and 0 <= forward_one[1] <= 7:
        moves_list.append(forward_one)
        # Move forward two squares from starting position
        if position[1] == start_row:
            forward_two = (position[0], position[1] + 2 * direction)
            if forward_two not in friend_locations + enemy_locations:
                moves_list.append(forward_two)

    # Captures
    for dx in [-1, 1]:
        capture = (position[0] + dx, position[1] + direction)
        if 0 <= capture[0] <= 7:
            if capture in enemy_locations:
                moves_list.append(capture)
            elif capture == en_passant_square:
                moves_list.append(capture)
    return moves_list

# Function to handle pawn promotion
def handle_pawn_promotion(color, selection, click_coords):
    promotion_pieces = ['queen', 'rook', 'bishop', 'knight']
    # Display a simple menu for selection
    selected_piece = None
    menu_open = True
    while menu_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for idx, piece in enumerate(promotion_pieces):
                    rect = pygame.Rect(200 + idx * 100, 250, 80, 80)
                    if rect.collidepoint(mx, my):
                        selected_piece = piece
                        menu_open = False
        # Draw promotion menu
        pygame.draw.rect(screen, (30, 30, 30), (150, 200, 400, 200))
        prompt_text = big_font.render(f"Promote to:", True, 'white')
        screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, 210))
        for idx, piece in enumerate(promotion_pieces):
            pygame.draw.rect(screen, (70, 70, 70), (200 + idx * 100, 250, 80, 80))
            piece_index = piece_list.index(piece)
            if color == 'white':
                img = white_images[piece_index]
            else:
                img = black_images[piece_index]
            img_rect = img.get_rect(center=(240 + idx * 100, 290))
            screen.blit(img, img_rect)
        pygame.display.flip()
    if color == 'white':
        white_pieces_list[selection] = selected_piece
    else:
        black_pieces_list[selection] = selected_piece

# Main game loop
update_options()
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    restart_button_rect = draw_restart_button()
    play_with_time_button_rect = draw_play_with_time_button()
    draw_timers()
    if selection is not None:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # Update timers
    if time_controls_enabled and not game_over:
        current_time = pygame.time.get_ticks()
        time_elapsed = (current_time - last_move_time) / 1000
        if turn_step < 2:
            white_time -= time_elapsed
            if white_time <= 0:
                winner = 'Black'
                game_over = True
        else:
            black_time -= time_elapsed
            if black_time <= 0:
                winner = 'White'
                game_over = True
        last_move_time = current_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(mx, my):
                reset_game()
            elif play_with_time_button_rect.collidepoint(mx, my):
                start_game_with_time()
            elif event.button == 1 and not game_over:
                x_coord = event.pos[0] // (BOARD_SIZE // 8)
                y_coord = event.pos[1] // (BOARD_SIZE // 8)
                click_coords = (x_coord, y_coord)
                if x_coord >= 8 or y_coord >= 8:
                    continue  # Ignore clicks outside the board
                if turn_step <= 1:
                    if click_coords in white_locations:
                        idx = white_locations.index(click_coords)
                        selection = idx
                        turn_step = 1
                    elif selection is not None and click_coords in valid_moves:
                        # Move the selected piece
                        orig_pos = white_locations[selection]
                        white_locations[selection] = click_coords
                        # Handle en passant
                        if white_pieces_list[selection] == 'pawn':
                            if click_coords == en_passant_square:
                                captured_idx = black_locations.index(en_passant_target)
                                captured_pieces_white.append(black_pieces_list[captured_idx])
                                black_pieces_list.pop(captured_idx)
                                black_locations.pop(captured_idx)
                            # Set en passant square
                            if abs(click_coords[1] - orig_pos[1]) == 2:
                                en_passant_square = (click_coords[0], click_coords[1] + 1)
                                en_passant_target = click_coords
                            else:
                                en_passant_square = None
                        else:
                            en_passant_square = None
                        # Update castling rights
                        if white_pieces_list[selection] == 'king':
                            white_can_castle_kingside = False
                            white_can_castle_queenside = False
                            # Handle castling move
                            if abs(click_coords[0] - orig_pos[0]) == 2:
                                if click_coords[0] == 6:
                                    # Kingside castling
                                    rook_idx = white_locations.index((7, 7))
                                    white_locations[rook_idx] = (5, 7)
                                else:
                                    # Queenside castling
                                    rook_idx = white_locations.index((0, 7))
                                    white_locations[rook_idx] = (3, 7)
                        elif white_pieces_list[selection] == 'rook':
                            if orig_pos == (0, 7):
                                white_can_castle_queenside = False
                            elif orig_pos == (7, 7):
                                white_can_castle_kingside = False
                        if click_coords in black_locations:
                            captured_idx = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces_list[captured_idx])
                            black_pieces_list.pop(captured_idx)
                            black_locations.pop(captured_idx)
                        # Pawn promotion
                        if white_pieces_list[selection] == 'pawn' and click_coords[1] == 0:
                            handle_pawn_promotion('white', selection, click_coords)
                        # Update options
                        update_options()
                        # Apply increment
                        if time_controls_enabled:
                            white_time += increment
                        # Check for check or checkmate
                        in_check = is_king_in_check(black_pieces_list, black_locations, 'black', white_pieces_list, white_locations)
                        if in_check:
                            if all(len(moves) == 0 for moves in black_options):
                                winner = 'White'
                                game_over = True
                        else:
                            if all(len(moves) == 0 for moves in black_options):
                                winner = 'Draw'
                                game_over = True
                        turn_step = 2
                        selection = None
                        valid_moves = []
                        last_move_time = pygame.time.get_ticks()
                else:
                    if click_coords in black_locations:
                        idx = black_locations.index(click_coords)
                        selection = idx
                        turn_step = 3
                    elif selection is not None and click_coords in valid_moves:
                        # Move the selected piece
                        orig_pos = black_locations[selection]
                        black_locations[selection] = click_coords
                        # Handle en passant
                        if black_pieces_list[selection] == 'pawn':
                            if click_coords == en_passant_square:
                                captured_idx = white_locations.index(en_passant_target)
                                captured_pieces_black.append(white_pieces_list[captured_idx])
                                white_pieces_list.pop(captured_idx)
                                white_locations.pop(captured_idx)
                            # Set en_passant square
                            if abs(click_coords[1] - orig_pos[1]) == 2:
                                en_passant_square = (click_coords[0], click_coords[1] - 1)
                                en_passant_target = click_coords
                            else:
                                en_passant_square = None
                        else:
                            en_passant_square = None
                        # Update castling rights
                        if black_pieces_list[selection] == 'king':
                            black_can_castle_kingside = False
                            black_can_castle_queenside = False
                            # Handle castling move
                            if abs(click_coords[0] - orig_pos[0]) == 2:
                                if click_coords[0] == 6:
                                    # Kingside castling
                                    rook_idx = black_locations.index((7, 0))
                                    black_locations[rook_idx] = (5, 0)
                                else:
                                    # Queenside castling
                                    rook_idx = black_locations.index((0, 0))
                                    black_locations[rook_idx] = (3, 0)
                        elif black_pieces_list[selection] == 'rook':
                            if orig_pos == (0, 0):
                                black_can_castle_queenside = False
                            elif orig_pos == (7, 0):
                                black_can_castle_kingside = False
                        if click_coords in white_locations:
                            captured_idx = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces_list[captured_idx])
                            white_pieces_list.pop(captured_idx)
                            white_locations.pop(captured_idx)
                        # Pawn promotion
                        if black_pieces_list[selection] == 'pawn' and click_coords[1] == 7:
                            handle_pawn_promotion('black', selection, click_coords)
                        # Update options
                        update_options()
                        # Apply increment
                        if time_controls_enabled:
                            black_time += increment
                        # Check for check or checkmate
                        in_check = is_king_in_check(white_pieces_list, white_locations, 'white', black_pieces_list, black_locations)
                        if in_check:
                            if all(len(moves) == 0 for moves in white_options):
                                winner = 'Black'
                                game_over = True
                        else:
                            if all(len(moves) == 0 for moves in white_options):
                                winner = 'Draw'
                                game_over = True
                        turn_step = 0
                        selection = None
                        valid_moves = []
                        last_move_time = pygame.time.get_ticks()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                reset_game()

    if winner != '':
        pygame.draw.rect(screen, 'black', [100, 200, 400, 100])
        if winner == 'Draw':
            game_over_text = big_font.render(f'Game Drawn!', True, 'white')
        else:
            game_over_text = big_font.render(f'{winner} won the game!', True, 'white')
        restart_text = medium_font.render('Press ENTER to Restart!', True, 'white')
        screen.blit(game_over_text, (150, 220))
        screen.blit(restart_text, (180, 260))
    pygame.display.flip()
pygame.quit()
