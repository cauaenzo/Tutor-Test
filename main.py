import pgzrun
import random
from pygame import Rect

# --- CONFIGURAÇÕES ---
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32
FPS = 30

# Cores
COLOR_FLOOR = (139, 69, 19)  # Marrom
COLOR_HERO = [(0, 0, 255), (0, 0, 200)]  # Azul, animação 2 frames
COLOR_ENEMY = [(255, 0, 0), (200, 0, 0)]  # Vermelho, animação 2 frames
COLOR_BULLET = (255, 255, 0)  # Amarelo para tiro
COLOR_BUTTON = (100, 100, 100)
COLOR_BUTTON_HOVER = (150, 150, 150)
COLOR_TEXT = (255, 255, 255)

# Música e sons
music_on = True

# --- CLASSES ---

class AnimatedSprite:
    def __init__(self, x, y, color_frames):
        self.x = x
        self.y = y
        self.color_frames = color_frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_delay = 10
    
    def update_animation(self):
        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.color_frames)
    
    def draw(self, screen):
        screen.draw.filled_rect(Rect(self.x, self.y, TILE_SIZE, TILE_SIZE), self.color_frames[self.frame_index])

class Hero(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(x, y, COLOR_HERO)
        self.speed = 4
        self.last_dx = 1  # Direção padrão para direita
        self.last_dy = 0
    
    def move(self, dx, dy):
        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy
        
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if 0 <= new_x <= WIDTH - TILE_SIZE:
            self.x = new_x
        if 0 <= new_y <= HEIGHT - TILE_SIZE:
            self.y = new_y
    
    def update(self):
        self.update_animation()

class Enemy(AnimatedSprite):
    def __init__(self, x, y, territory_rect):
        super().__init__(x, y, COLOR_ENEMY)
        self.territory = territory_rect
        self.speed = 2
        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
    
    def update(self):
        dx, dy = self.direction
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        if not self.territory.contains(Rect(new_x, new_y, TILE_SIZE, TILE_SIZE)):
            self.direction = (-dx, -dy)
            new_x = self.x + self.direction[0] * self.speed
            new_y = self.y + self.direction[1] * self.speed
        
        self.x = new_x
        self.y = new_y
        self.update_animation()

class Bullet:
    SPEED = 10
    SIZE = 8
    def __init__(self, x, y, dx, dy):
        self.x = x + TILE_SIZE//2 - self.SIZE//2
        self.y = y + TILE_SIZE//2 - self.SIZE//2
        self.dx = dx
        self.dy = dy
        self.active = True
    
    def update(self):
        self.x += self.dx * self.SPEED
        self.y += self.dy * self.SPEED
        # Desativa se sair da tela
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.active = False
    
    def draw(self):
        screen.draw.filled_rect(Rect(self.x, self.y, self.SIZE, self.SIZE), COLOR_BULLET)
    
    def get_rect(self):
        return Rect(self.x, self.y, self.SIZE, self.SIZE)

class Button:
    def __init__(self, rect, text, callback):
        self.rect = rect
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def draw(self):
        color = COLOR_BUTTON_HOVER if self.hovered else COLOR_BUTTON
        screen.draw.filled_rect(self.rect, color)
        screen.draw.textbox(self.text, self.rect, color=COLOR_TEXT, align='center')
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
    
    def click(self):
        if self.callback:
            self.callback()

# --- FUNÇÕES DO JOGO ---

def start_game():
    global game_state, enemies, bullets, score
    game_state = 'playing'
    score = 0
    hero.x = WIDTH//2
    hero.y = HEIGHT//2
    enemies.clear()
    for _ in range(5):
        tx = random.randint(0, (WIDTH - TILE_SIZE) // TILE_SIZE) * TILE_SIZE
        ty = random.randint(0, (HEIGHT - TILE_SIZE) // TILE_SIZE) * TILE_SIZE
        territory = Rect(max(tx - 64, 0), max(ty - 64, 0), 128, 128)
        enemies.append(Enemy(tx, ty, territory))
    bullets.clear()

def toggle_sound():
    global music_on
    music_on = not music_on
    if music_on:
        music.unpause()
        button_sound.text = "Sound On"
    else:
        music.pause()
        button_sound.text = "Sound Off"

def quit_game():
    exit()

def voltar_menu():
    global game_state
    game_state = 'menu'

# --- VARIÁVEIS GLOBAIS ---

game_state = 'menu'
hero = Hero(WIDTH//2, HEIGHT//2)
enemies = []
bullets = []
score = 0

button_start = Button(Rect(WIDTH//2 - 100, 150, 200, 50), 'Start Game', start_game)
button_sound = Button(Rect(WIDTH//2 - 100, 220, 200, 50), 'Sound On', toggle_sound)
button_quit = Button(Rect(WIDTH//2 - 100, 290, 200, 50), 'Quit', quit_game)
menu_buttons = [button_start, button_sound, button_quit]

button_back = Button(Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50), 'Voltar', voltar_menu)

def draw():
    screen.clear()
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            screen.draw.filled_rect(Rect(x, y, TILE_SIZE, TILE_SIZE), COLOR_FLOOR)
    
    if game_state == 'menu':
        for button in menu_buttons:
            button.draw()
        screen.draw.text(f"Score: {score}", (10,10), color=COLOR_TEXT)
    elif game_state == 'playing':
        hero.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw()
        screen.draw.text(f"Score: {score}", (10,10), color=COLOR_TEXT)
    elif game_state == 'won':
        texto = "VOCÊ VENCEU!"
        fontsize = 60
        w, h = screen.surface.get_size()
        screen.draw.text(
            texto,
            center=(w//2, h//2),
            fontsize=fontsize,
            color="yellow",
            shadow=(1,1)
        )
        button_back.draw()

def update_hero_movement():
    if game_state != 'playing':
        return
    dx = dy = 0
    if keyboard.left:
        dx = -1
    elif keyboard.right:
        dx = 1
    if keyboard.up:
        dy = -1
    elif keyboard.down:
        dy = 1
    hero.move(dx, dy)

def check_collisions():
    global game_state, score
    hero_rect = Rect(hero.x, hero.y, TILE_SIZE, TILE_SIZE)
    # Checar colisão herói-inimigo
    for enemy in enemies:
        enemy_rect = Rect(enemy.x, enemy.y, TILE_SIZE, TILE_SIZE)
        if hero_rect.colliderect(enemy_rect):
            game_state = 'menu'  # game over
    
    # Checar colisão tiros-inimigos
    for bullet in bullets:
        bullet_rect = bullet.get_rect()
        for enemy in enemies:
            enemy_rect = Rect(enemy.x, enemy.y, TILE_SIZE, TILE_SIZE)
            if bullet_rect.colliderect(enemy_rect):
                if bullet in bullets:
                    bullet.active = False
                if enemy in enemies:
                    enemies.remove(enemy)
                score += 10
                break

def update():
    global game_state
    update_hero_movement()
    if game_state == 'playing':
        hero.update()
        for enemy in enemies:
            enemy.update()
        for bullet in bullets:
            bullet.update()
        bullets[:] = [b for b in bullets if b.active]
        check_collisions()

        # Verificar vitória
        if len(enemies) == 0:
            game_state = 'won'

def on_key_down(key):
    global game_state
    if game_state == 'playing':
        if key == keys.ESCAPE:
            game_state = 'menu'
        if key == keys.SPACE:
            dx = hero.last_dx
            dy = hero.last_dy
            if dx != 0 or dy != 0:
                bullets.append(Bullet(hero.x, hero.y, dx, dy))
    elif game_state == 'won':
        if key == keys.ESCAPE:
            game_state = 'menu'

def on_mouse_move(pos):
    if game_state == 'menu':
        for button in menu_buttons:
            button.check_hover(pos)
    elif game_state == 'won':
        button_back.check_hover(pos)

def on_mouse_down(pos):
    if game_state == 'menu':
        for button in menu_buttons:
            if button.hovered:
                button.click()
    elif game_state == 'won':
        if button_back.hovered:
            button_back.click()

# --- Música ---

try:
    if music_on:
        music.set_volume(0.5)  # Ajusta volume entre 0.0 e 1.0
        music.play('robot_city')  # arquivo 'music/robot_city.mp3' - sem extensão
except Exception as e:
    print("Could not play music:", e)

pgzrun.go()
