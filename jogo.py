import pgzrun
import time
from random import randint

WIDTH = 800
HEIGHT = 600

# Player
player_frames = [f"hero_run{i}" for i in range(1, 7)]
player = Actor(player_frames[0])
player.x = WIDTH // 2
player.y = HEIGHT - 300
player.vx = 5
player_frame = 0
player_timer = 0

# Pulo
player.vy = 0
player_on_ground = True
gravity = 0.8
jump_strength = -15

# Botões do menu
start_button = Actor("start_btn")
sound_button = Actor("sound_on")
exit_button = Actor("exit_btn")
menu_spacing = 90
start_button.pos = (WIDTH // 2, HEIGHT // 2 - menu_spacing)
sound_button.pos = (WIDTH // 2, HEIGHT // 2)
exit_button.pos = (WIDTH // 2, HEIGHT // 2 + menu_spacing)

# Estados
game_started = False
game_over = False
start_time = 0
end_time = 0
enemies = []
hits = 0
sound_on = True


class Enemy:
    def __init__(self, x, y, direction=1):
        self.x = x
        self.y = y
        self.vx = 2 * direction
        self.timer = 0
        self.frames = [f"enemy1_idle{i}" for i in range(1, 3)]
        self.current_frame = 0

    def update(self):
        self.x += self.vx
        if self.x > WIDTH - 40 or self.x < 40:
            self.vx *= -1
        self.animate()

    def animate(self):
        self.timer += 1
        if self.timer % 15 == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self):
        Actor(self.frames[self.current_frame], (self.x, self.y)).draw()

    def get_rect(self):
        return Rect(self.x - 20, self.y - 20, 40, 40)


def start_game():
    global game_started, game_over, start_time, end_time, enemies, hits, player_on_ground
    game_started = True
    game_over = False
    start_time = time.time()
    enemies.clear()
    enemy_y = 300
    for i in range(3):
        x = 100 + i * 250
        direction = 1 if i % 2 == 0 else -1
        enemies.append(Enemy(x, enemy_y, direction))
    hits = 0
    player.y = HEIGHT - 300
    player.vy = 0
    player_on_ground = True
    if sound_on:
        music.play("bg_music")


def update():
    if game_started and not game_over:
        update_player()
        for enemy in enemies:
            enemy.update()
        check_collisions()


def update_player():
    global player_frame, player_timer, player_on_ground

    if keyboard.left:
        player.x -= player.vx
    if keyboard.right:
        player.x += player.vx

    if keyboard.left or keyboard.right:
        player_timer += 1
        if player_timer % 5 == 0:
            player_frame = (player_frame + 1) % len(player_frames)
        player.image = player_frames[player_frame]
    else:
        player.image = player_frames[0]

    player.y += player.vy
    player.vy += gravity

    ground_y = HEIGHT - 300
    if player.y >= ground_y:
        player.y = ground_y
        player.vy = 0
        player_on_ground = True
    else:
        player_on_ground = False

    if keyboard.space and player_on_ground:
        player.vy = jump_strength
        player_on_ground = False
        if sound_on:
            sounds.jump.play()


def check_collisions():
    global hits, game_over, game_started, end_time
    player_rect = Rect(player.x - 20, player.y - 20, 40, 40)
    for enemy in enemies:
        if player_rect.colliderect(enemy.get_rect()):
            hits += 1
            if sound_on:
                sounds.hit.play()
            break

    if hits >= 10:
        game_over = True
        game_started = False
        end_time = time.time()
        music.stop()


def draw():
    screen.clear()
    screen.blit("background", (0, 0))
    if game_started:
        draw_game()
    elif game_over:
        draw_game_over()
    else:
        draw_menu()


def draw_game():
    player.draw()
    for enemy in enemies:
        enemy.draw()
    elapsed = int(time.time() - start_time)
    screen.draw.text(f"Tempo: {elapsed}s", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Atingido: {hits}/10", (10, 90), fontsize=30, color="red")


def draw_game_over():
    duration = int(end_time - start_time)
    screen.draw.text("FIM DE JOGO", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=60, color="red")
    screen.draw.text(f"Tempo de sobrevivência: {duration} segundos", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text("Clique para voltar ao menu", center=(WIDTH // 2, HEIGHT // 2 + 120), fontsize=30, color="gray")


def draw_menu():
    screen.draw.text("Bem-vindo ao Jogo!", center=(WIDTH // 2, 100), fontsize=60, color="orange")
    start_button.draw()
    sound_button.draw()
    exit_button.draw()


def on_mouse_down(pos):
    global sound_on
    if not game_started and not game_over:
        if start_button.collidepoint(pos):
            start_game()
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play("bg_music")
                sound_button.image = "sound_on"
            else:
                music.stop()
                sound_button.image = "sound_off"
        elif exit_button.collidepoint(pos):
            exit()
    elif game_over:
        # Voltar ao menu depois do fim de jogo
        reset_to_menu()


def reset_to_menu():
    global game_over
    game_over = False


pgzrun.go()
