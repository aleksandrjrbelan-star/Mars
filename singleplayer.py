import pygame as pg
import json
import math
import os
from random import randint, uniform
from data.config import *
import data.modules.imports as impt

difficulty_settings = {
    "easy": {"o2_loss_speed": 0.055, "o2_recovery_speed": 0.1, "hunger_loss_speed": 0.005, "minerals_per_day": 42,"o2_hp_loss_speed": 0.05, "hunger_hp_loss_speed": 0.02},
    "medium": {"o2_loss_speed": 0.1, "o2_recovery_speed": 0.2, "hunger_loss_speed": 0.01, "minerals_per_day": 21,"o2_hp_loss_speed": 0.30, "hunger_hp_loss_speed": 0.25},
    "hard": {"o2_loss_speed": 0.2, "o2_recovery_speed": 0.2, "hunger_loss_speed": 0.02, "minerals_per_day": 11,"o2_hp_loss_speed": 0.50, "hunger_hp_loss_speed": 0.25},
}
pg.init()
pg.mixer.init()

# --- Функції ---
fade_surface = pg.Surface((WEIGHT, HEIGHT))
fade_surface.fill(BLACK)
is_transitioning = False
last_menu_track = None
menu_music = [
    "data/sounds/bg_music/bg_menu1.mp3",
    "data/sounds/bg_music/bg_menu2.mp3",
    "data/sounds/bg_music/bg_menu3.mp3",
    "data/sounds/bg_music/bg_menu4.ogg",
]
SETTINGS_PATH = "data/settings/settings.json"


def load_settings():
    default_settings = {
        "difficult": "none",
        "music_loud": 0.50,
        "sounds_loud": 0.50,
        'portrait': "none",
        "fullscreen": False,
    }

    if not os.path.exists(SETTINGS_PATH):
        return default_settings

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return default_settings
            data = json.loads(content)
            if not isinstance(data, dict):
                return default_settings
    except (json.JSONDecodeError, OSError):
        return default_settings

    default_settings.update(data)
    return default_settings

def save_settings():
    settings_data["music_loud"] = round(music_loud, 2)
    settings_data["sounds_loud"] = round(sounds_loud, 2)
    settings_data["fullscreen"] = is_fullscreen
    settings_data["difficult"] = selected_difficulty
    settings_data["portrait"] = selected_portrait

    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings_data, file)

def make_save():
    pass

def load_save():
    pass

def save_selected_difficulty():
    settings_data["difficult"] = selected_difficulty
    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings_data, file)

def save_selected_portrait():
    settings_data["portrait"] = selected_portrait
    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings_data, file)

def play_random_menu_music():
    global last_menu_track, menu_music, music_loud

    track = menu_music[randint(0, len(menu_music) - 1)]

    while track == last_menu_track and len(menu_music) > 1:
        track = menu_music[randint(0, len(menu_music) - 1)]

    last_menu_track = track

    pg.mixer.music.load(track)
    pg.mixer.music.set_volume(music_loud)
    pg.mixer.music.play()

def fade_to_black(draw_scene, no=False):
    global fade_surface, is_transitioning
    is_transitioning = True
    fade_surface.fill(BLACK)
    draw_scene()
    scene_snapshot = screen.copy()
    for alpha in range(0, 255, 5):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        fade_surface.set_alpha(alpha)
        screen.blit(scene_snapshot, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pg.display.flip()
        pg.time.delay(30)
        clock.tick(FPS)

def fade_from_black(draw_scene):
    global game_part, fade_surface, is_transitioning
    fade_surface.fill(BLACK)
    for alpha in range(255, -1, -5):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        draw_scene()
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

        pg.display.flip()
        clock.tick(FPS)
        pg.time.delay(30)
    is_transitioning = False

def draw_menu_scene():
    draw_menu_background()
    for s in sprites:
        s.draw(screen)

def draw_game_scene():
    screen.fill(BLACK)
    if new_day:
        days_label.set_text(f"Day {days}")
        new_day_bg.image.set_alpha(255)
        days_label.image.set_alpha(255)
        new_day_bg.draw(screen, 0, 0)
        days_label.draw(screen)
    else:
        background1.draw(screen, camera_x, camera_y)
        pl.draw(screen, camera_x, camera_y)   

def draw_base_scene():
    global home_background, pl, workbench
    screen.fill(BLACK)
    home_background.draw(screen)
    pl.draw(screen)

def draw_current_location_scene():
    if location == "base":
        home_background.draw(screen)
        pl.draw(screen)
    else:
        background1.draw(screen, camera_x, camera_y)
        for m in actv_minerals:
            m.draw(screen, camera_x, camera_y)
        base_home.draw(screen, camera_x, camera_y)
        pl.draw(screen, camera_x, camera_y)

    for s in [hp_icon, o2_icon, sleep_icon, hunger_icon, stats, hp_bare, o2_bare, sleep_bare, hunger_bare, stone_icon, iron_icon, rubin_icon, gips_icon, stone_text, iron_text, rubin_text, gips_text]:
        s.draw(screen)

def play_death_animation():
    global game_part, new_day, wt, alpha_nd, location, days

    overlay = pg.Surface((WEIGHT, HEIGHT), pg.SRCALPHA)
    days_label_gameover.set_text(f"Прожито {days} днів")

    death_frames = getattr(pl, "imgs_die", [])
    if death_frames:
        for frame_image in death_frames:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            screen.fill(BLACK)
            pl.image = frame_image
            draw_current_location_scene()
            pg.display.flip()
            clock.tick(1)

    for frame in range(45):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        player_alpha = max(0, 255 - frame * 6)
        overlay_alpha = min(210, frame * 4)

        screen.fill(BLACK)
        temp_image = pl.image.copy()
        temp_image.set_alpha(player_alpha)
        pl.image = temp_image

        draw_current_location_scene()

        overlay.fill((80, 0, 0, overlay_alpha))
        screen.blit(overlay, (0, 0))
        pg.display.flip()
        clock.tick(18)
    game_part = "game_over"
    pl.hp = pl.hp_max
    pl.o2 = pl.o2_max
    pl.sleep = 100
    pl.hunger = 100
    location = "basic"
    new_day = True
    wt = 0
    alpha_nd = 255
    days = 1

def open_pause_menu():
    global game_part

    panel = pg.Rect(240, 120, 420, 340)
    overlay = pg.Surface((WEIGHT, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    pause_title = TextLabel(395, 150, 56, WHITE, "Pause", font_pixel)

    continue_btn = Button(360, 220, pause_continue_img, pause_continue_actv_img, btn_collision, btn_click)
    pause_settings_btn = Button(360, 305, pause_settings_img, pause_settings_actv_img, btn_collision, btn_click)
    pause_exit_btn = Button(360, 390, pause_exit_img, pause_exit_actv_img, btn_collision, btn_click)

    pause_open = True
    while pause_open:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pause_open = False

        def close_pause():
            nonlocal pause_open
            pause_open = False

        def open_pause_settings():
            open_settings_menu()

        def exit_to_menu():
            global game_part
            nonlocal pause_open
            pause_open = False
            game_part = "menu"

        continue_btn.onclick(close_pause)
        pause_settings_btn.onclick(open_pause_settings)
        pause_exit_btn.onclick(exit_to_menu)

        continue_btn.update()
        pause_settings_btn.update()
        pause_exit_btn.update()

        if location == "base":
            draw_base_scene()
        else:
            draw_game_scene()

        screen.blit(overlay, (0, 0))
        pg.draw.rect(screen, (18, 18, 24), panel, border_radius=14)
        pg.draw.rect(screen, (95, 85, 70), panel, 2, border_radius=14)
        pause_title.draw(screen)
        continue_btn.draw(screen)
        pause_settings_btn.draw(screen)
        pause_exit_btn.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

CRAFT_RECIPES = {
    "improved_o2_tank": {
        "title": "Поліпшений газовий балон",
        "cost": {"iron": [4,'Залізо'], "rubin": [2,'Рубін'], "gips": [2,'Гіпс']},
        "single": True
    },
    "food": {
        "title": "Їжа",
        "cost": {"stone": [1,'Камінь'], "gips": [1,'Гіпс']},
        "single": False
    },
    "medkit": {
        "title": "Аптечка",
        "cost": {"iron": [2,'Залізо'], "rubin": [1,'Рубін'], "gips": [2,'Гіпс']},
        "single": False
    }
}

def can_craft_recipe(player, recipe_key):
    recipe = CRAFT_RECIPES[recipe_key]
    if recipe["single"] and player.items[recipe_key] >= 1:
        return False
    for resource, cost_data in recipe["cost"].items():
        amount = cost_data[0] if isinstance(cost_data, list) else cost_data
        if player.resources.get(resource, 0) < amount:
            return False
    return True

def craft_recipe(player, recipe_key):
    if not can_craft_recipe(player, recipe_key):
        return False

    recipe = CRAFT_RECIPES[recipe_key]
    for resource, cost_data in recipe["cost"].items():
        amount = cost_data[0] if isinstance(cost_data, list) else cost_data
        player.resources[resource] -= amount
    player.items[recipe_key] += 1
    return True

def open_workbench_menu(player):
    selected_recipe = "improved_o2_tank"
    panel = pg.Rect(110, 90, 680, 420)
    left_panel = pg.Rect(140, 145, 250, 280)
    right_panel = pg.Rect(420, 145, 300, 280)
    overlay = pg.Surface((WEIGHT, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 170))

    title = TextLabel(285, 110, 42, WHITE, "Верстак", font_pixel)
    recipe_buttons = {
        "improved_o2_tank": TextButton(155, 170, "Газовий балон", 210),
        "food": TextButton(155, 245, "Їжа", 210),
        "medkit": TextButton(155, 320, "Аптечка", 210),
    }
    create_button = TextButton(470, 380, "Створити", 170)
    close_button = TextButton(650, 105, "X", 50)
    info_label = TextLabel(440, 170, 28, WHITE, "", font_pixel)
    status_label = TextLabel(440, 405, 24, WHITE, "", font_pixel)

    menu_open = True
    while menu_open:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == MUSIC_END:
                play_random_menu_music()

        def select_recipe(recipe_key):
            nonlocal selected_recipe
            selected_recipe = recipe_key

        def close_menu():
            nonlocal menu_open
            menu_open = False

        def create_item():
            recipe = CRAFT_RECIPES[selected_recipe]
            if recipe["single"] and player.items[selected_recipe] >= 1:
                status_label.set_text("Уже створено")
            elif craft_recipe(player, selected_recipe):
                status_label.set_text("Предмет створено")
            else:
                status_label.set_text("Недостатньо ресурсів")

        recipe_buttons["improved_o2_tank"].onclick(lambda: select_recipe("improved_o2_tank"))
        recipe_buttons["food"].onclick(lambda: select_recipe("food"))
        recipe_buttons["medkit"].onclick(lambda: select_recipe("medkit"))
        create_button.onclick(create_item)
        close_button.onclick(close_menu)

        for button in recipe_buttons.values():
            button.update()
        create_button.update()
        close_button.update()

        recipe = CRAFT_RECIPES[selected_recipe]
        info_label.set_text(recipe["title"])

        draw_base_scene()
        screen.blit(overlay, (0, 0))
        pg.draw.rect(screen, (18, 18, 24), panel, border_radius=14)
        pg.draw.rect(screen, (95, 85, 70), panel, 2, border_radius=14)
        pg.draw.rect(screen, (28, 28, 35), left_panel, border_radius=10)
        pg.draw.rect(screen, (28, 28, 35), right_panel, border_radius=10)

        title.draw(screen)
        info_label.draw(screen)

        for recipe_key, button in recipe_buttons.items():
            button.draw(screen)
            if recipe_key == selected_recipe:
                pg.draw.rect(screen, (210, 170, 80), button.rect, 2, border_radius=4)

        y = 210
        for resource, cost_data in recipe["cost"].items():
            if isinstance(cost_data, list):
                amount = cost_data[0]
                resource_name = cost_data[1]
            else:
                amount = cost_data
                resource_name = resource

            owned = player.resources.get(resource, 0)
            color = WHITE if owned >= amount else RED
            
            TextLabel(440, y, 24, color, f"{resource_name}: {owned}/{amount}", font_pixel).draw(screen)
            y += 38

        if recipe["single"]:
            single_text = "1/1 створено" if player.items[selected_recipe] >= 1 else "0/1 створено"
            TextLabel(440, y-5, 12, WHITE, single_text, font_pixel).draw(screen)


        TextLabel(440, 345, 12, WHITE, f"В наявності: {player.items[selected_recipe]}", font_pixel).draw(screen)
        create_button.draw(screen)
        close_button.draw(screen)
        status_label.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

# --- Class ---

class TextButton():
    clicked = False
    def __init__(self, x, y, text, w):
        self.rect = pg.Rect(x, y, w, 50)
        self.rect_image = pg.Surface((w, 50))
        self.rect_image.fill(BLUE)
        self.rect_image_active = pg.Surface((w, 50))
        self.rect_image_active.fill(GREEN)
        self.font = pg.font.Font(None, 32)
        self.text_image = self.font.render(text, True, RED)
        self.text_rect = self.text_image.get_rect()
        self.text_rect.x = self.rect.x + 20
        self.text_rect.y = y+5
        self.active = False
        self.fn = None
    def update(self):
        x, y = pg.mouse.get_pos()
        collision = self.rect.collidepoint(x, y)
        click = pg.mouse.get_pressed()[0]
        if collision:
            self.active = True
            if click and not TextButton.clicked:
                TextButton.clicked = True
                if self.fn:
                    self.fn()
        else:
            self.active = False
            if not click:
                TextButton.clicked = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.rect_image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.rect_image_active, (self.rect.x, self.rect.y))
        surface.blit(self.text_image, (self.text_rect.x, self.text_rect.y))

    def onclick(self, fn):
        self.fn = fn

class Sprite:
    # базовий клас для спадкування класами гри
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pg.Rect(x, y, self.image.get_width(),
                            self.image.get_height())

    def collide(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, screen, camera_x=0, camera_y=0):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Mineral(Sprite):
    def __init__(self, x, y, image, mineral_type):
        super().__init__(x, y, image)
        self.type = mineral_type
        self.collected = False
    def update(self, player):
        global not_enough_sleep_timer
        if self.rect.colliderect(player.pickaxe_rect) and player.sleep > 0:
            player.resources[self.type] += 1
            player.sleep -= 15
            return self.type
        if player.sleep <= 0 and not self.collected:
            not_enough_sleep_timer = 160
            player.sleep = 0
            self.collected = True
            
        return None

class Bare(Sprite):
    # Базовий клас для барів здоров'я, кисню, сну і голоду.
    def __init__(self, x, y, width, color):
        image = pg.Surface((width, 20))
        image.fill(color)
        self.color = color
        super().__init__(x, y, image)
    def update(self, current_value, max_value):
        ratio = max(0, min(current_value / max_value, 1))
        self.image = pg.Surface((int(self.rect.width * ratio), 20))
        self.image.fill(self.color)

class Sleep(Sprite):
    def __init__(self, x, y, image,location):
        self.location = location
        super().__init__(x,y,image)
    def update(self,player):
        global days, new_day, wt, alpha_nd
        if self.rect.colliderect(player):
            player.rect.x = 1200
            player.rect.y = 1200
            days += 1
            new_day = True
            wt = 0
            alpha_nd = 255
            player.sleep = 100
            days_label.set_text(f"Day {days}")
            new_day_bg.image.set_alpha(255)
            days_label.image.set_alpha(255)
            return self.location
        return None

class TextLabel:
    def __init__(self, x, y, size, color="black", default_text="text",font=None):
        self.font = font if font else pg.font.Font(None, size)
        self.coord = (x, y)
        self.color = color
        self.set_text(default_text)

    def set_text(self, text):
        self.image = self.font.render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.image, self.coord)

class BasicButton:
    # з попереднього проєкту
    def __init__(self, x, y, img, img_active):
        self.image_inactive = img
        self.image_active = img_active
        self.image = self.image_inactive
        self.rect = pg.Rect(x, y, self.image.get_width(),
                            self.image.get_height())
        self.fn = None

    def update(self):
        x, y = pg.mouse.get_pos()
        collision = self.rect.collidepoint(x, y)
        if collision:
            self.image = self.image_active
            click = pg.mouse.get_pressed()[0]
            if click and self.fn:
                self.fn()
        else:
            self.image = self.image_inactive

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def onclick(self, fn):
        self.fn = fn

class Button:
    # Кнопка меню: міняє картинку, трохи збільшується і може програвати звуки.
    clicked = False

    def __init__(self, x, y, img, img_active, hover_sound=None, click_sound=None, resize=True):
        self.image_inactive = img
        self.image_active = img_active
        self.image = self.image_inactive
        self.base_rect = pg.Rect(x, y, self.image.get_width(),
                                 self.image.get_height())
        self.rect = self.base_rect.copy()
        self.fn = None
        self.hover_sound = hover_sound
        self.click_sound = click_sound
        self.hovered = False
        self.scale = 1
        self.resize = resize

    def update(self):
        if is_transitioning:
            return
        if not pg.mouse.get_focused():
            self.image = self.image_inactive
            self.hovered = False
            return
        x, y = pg.mouse.get_pos()
        collision = self.base_rect.collidepoint(x, y)
        if collision:
            self.image = self.image_active
            if not self.hovered and self.hover_sound:
                self.hover_sound.play()
            self.hovered = True
            click = pg.mouse.get_pressed()[0]
            if click and not Button.clicked:
                Button.clicked = True
                if self.click_sound:
                    self.click_sound.play()
                if self.fn:
                    self.fn()
        else:
            self.image = self.image_inactive
            self.hovered = False

        if not pg.mouse.get_pressed()[0]:
            Button.clicked = False

        target_scale = 1.05 if collision and self.resize else 1
        self.scale += (target_scale - self.scale) * 0.25

    def draw(self, surface):
        width = int(self.base_rect.width * self.scale)
        height = int(self.base_rect.height * self.scale)
        image = pg.transform.smoothscale(self.image, (width, height))
        self.rect = image.get_rect(center=self.base_rect.center)
        surface.blit(image, self.rect)

    def onclick(self, fn):
        self.fn = fn

class Slider:
    # Test slider for settings: drag handle and update value from 0.0 to 1.0.
    def __init__(self, x, y, width, value=0.5):
        self.rect = pg.Rect(x, y, width, 8)
        self.value = value
        self.dragging = False
        self.knob_radius = 12

    def handle_event(self, event):
        knob_x = self.rect.x + int(self.rect.width * self.value)
        knob_rect = pg.Rect(0, 0, self.knob_radius * 2, self.knob_radius * 2)
        knob_rect.center = (knob_x, self.rect.centery)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) or knob_rect.collidepoint(event.pos):
                self.dragging = True
                self.set_by_mouse(event.pos[0])
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            self.set_by_mouse(event.pos[0])

    def set_by_mouse(self, mouse_x):
        relative_x = mouse_x - self.rect.x
        relative_x = max(0, min(relative_x, self.rect.width))
        self.value = relative_x / self.rect.width

    def draw(self, screen):
        fill_width = int(self.rect.width * self.value)
        pg.draw.rect(screen, (60, 60, 70), self.rect, border_radius=4)
        pg.draw.rect(
            screen,
            (210, 170, 80),
            (self.rect.x, self.rect.y, fill_width, self.rect.height),
            border_radius=4
        )
        knob_x = self.rect.x + fill_width
        knob_y = self.rect.centery
        pg.draw.circle(screen, (245, 245, 245), (knob_x, knob_y), self.knob_radius)
        pg.draw.circle(screen, (120, 120, 130), (knob_x, knob_y), self.knob_radius, 2)

class Player(Sprite):
    def __init__(self, x, y, imgs_down, imgs_right, imgs_left, imgs_up ,imgs_base,imgs_down_left,imgs_down_right,imgs_up_left,imgs_up_right, imgs_die):
        self.imgs_right = imgs_right
        self.imgs_left = imgs_left
        self.imgs_up = imgs_up
        self.imgs_down = imgs_down
        self.imgs_base = imgs_base
        self.imgs_down_left = imgs_down_left
        self.imgs_down_right = imgs_down_right
        self.imgs_up_left = imgs_up_left
        self.imgs_up_right = imgs_up_right
        self.imgs_die = imgs_die
        self.pickaxe_rect = pg.Rect(x, y, 40, 40)
        self.direction = "stop"
        self.hp_max = 100
        self.o2_max = 100
        self.idle = 0
        self.tr = 0
        self.tu = 0
        self.td = 0
        self.tl = 0
        self.tul = 0
        self.tur = 0
        self.tdl = 0
        self.tdr = 0
        self.hp = 100
        self.sleep = 100
        self.o2 = 100
        self.hunger = 100
        self.resources = {"stone": 0, "iron": 0, "rubin": 0, "gips": 0}
        self.items = {"improved_o2_tank": 0, "food": 0, "medkit": 0}
        super().__init__(x, y, imgs_base[0])
    def update(self,rects):
        if self.hp <= 0:
            return "dead"
        self.pickaxe_rect.x = self.rect.x
        self.pickaxe_rect.y = self.rect.y
        keys = pg.key.get_pressed()
        left = keys[pg.K_LEFT]
        right = keys[pg.K_RIGHT]
        up = keys[pg.K_UP]
        down = keys[pg.K_DOWN]

        if up and left:
            self.tr = 0
            self.tu = 0
            self.td = 0
            self.tl = 0
            self.tur = 0
            self.tdl = 0
            self.tdr = 0
            self.tul += 1
            self.idle = 0
            self.rect.x -= 2
            self.rect.y -= 2
            self.image = self.imgs_up_left[self.tul//10%len(self.imgs_up_left)]
            self.direction = "up-left"
        elif up and right:
            self.idle = 0
            self.tu = 0
            self.td = 0
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur += 1
            self.rect.x += 2
            self.rect.y -= 2
            self.image = self.imgs_up_right[self.tur//10%len(self.imgs_up_right)] 
            self.direction = "up-right"
        elif down and left:
            self.td = 0
            self.idle = 0
            self.tu = 0
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl += 1
            self.tdr = 0
            self.tur = 0
            self.rect.y += 2
            self.rect.x -= 2
            self.image = self.imgs_down_left[self.tdl//10%len(self.imgs_down_left)]
            self.direction = "down-left"
        elif down and right:
            self.idle = 0
            self.td = 0
            self.tu = 0
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr += 1
            self.tur = 0
            self.rect.x += 2
            self.rect.y += 2
            self.image = self.imgs_down_right[self.tdr//10%len(self.imgs_down_right)] 
            self.direction = "down-right"
        elif down:
            self.idle = 0
            self.td += 1
            self.tu = 0
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur = 0
            self.rect.y += 2
            self.image = self.imgs_down[self.td//10%len(self.imgs_down)]  
            self.direction = "down"
        elif up:
            self.idle = 0
            self.td = 0
            self.tu += 1
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur = 0
            self.rect.y -= 2
            self.image = self.imgs_up[self.tu//10%len(self.imgs_up)]
            self.direction = "up"
        elif left:
            self.idle = 0
            self.td = 0
            self.tu = 0
            self.tl += 1
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur = 0
            self.rect.x -= 2
            self.image = self.imgs_left[self.tl//10%len(self.imgs_left)]  
            self.direction = "left"
        elif right:
            self.idle = 0
            self.td = 0
            self.tu = 0
            self.tl = 0
            self.tr += 1
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur = 0
            self.rect.x += 2
            self.image = self.imgs_right[self.tr//10%len(self.imgs_right)]  
            self.direction = "right"
        else:
            self.td = 0
            self.tu = 0
            self.tl = 0
            self.tr = 0
            self.tul = 0
            self.tdl = 0
            self.tdr = 0
            self.tur = 0
            self.idle += 1
            self.image = self.imgs_base[0]
            self.direction = "stop"
        for i in rects:
            if self.collide(i):
                if self.direction == "left":
                    self.rect.x += 2
                elif self.direction == "right":
                    self.rect.x -= 2
                elif self.direction == "up":
                    self.rect.y += 2
                elif self.direction == "down":
                    self.rect.y -= 2
                elif self.direction == "up-left":
                    self.rect.x += 2
                    self.rect.y += 2
                elif self.direction == "up-right":
                    self.rect.x -= 2
                    self.rect.y += 2
                elif self.direction == "down-left":
                    self.rect.x += 2
                    self.rect.y -= 2
                elif self.direction == "down-right":
                    self.rect.x -= 2
                    self.rect.y -= 2

class Enemy(Sprite):
    def __init__(self, x, y, enemy_number):
        if enemy_number == 1:
            self.hp = 125
            self.damage = 15
            self.uhilena = 1
            self.name = "Вовка"
            img = pg.image.load("game/images/enemies/Wolf.png")
        elif enemy_number == 2:
            self.hp = 55
            self.damage = 7
            self.uhilena = 2
            self.name = "Слизня"
            img = pg.image.load("game/images/enemies/slime.png")
        elif enemy_number == 3:
            self.hp = 60
            self.damage = 15
            self.uhilena = 3
            self.name = "Змію"
            img = pg.image.load("game/images/enemies/snake.png")
        elif enemy_number == 4:
            self.hp = 15
            self.damage = 1
            self.uhilena = 10
            self.name = "Кролика"
            img = pg.image.load("game/images/enemies/bunny.png")
        self.number = enemy_number
        super().__init__(x, y, img)
    def attack(self,player,hp):
        if player.uhilena <= randint(1, 100):
            hp_new = hp - self.damage
        if hp < 0:
            hp_new = 0
        return hp_new
    def defend(self,damage):
        if self.uhilena <= randint(1, 100):
            self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

class MenuStar(Sprite):
    # Zoria menu: rozmir, svitinnia, pulsatsiia, rukh i paralaks v odnomu klasi.
    def __init__(self, x, y, image, scale, speed_x, speed_y):
        image = pg.transform.smoothscale(
            image,
            (max(1, int(image.get_width() * scale)),
             max(1, int(image.get_height() * scale)))
        )
        super().__init__(x, y, image)

        self.x = float(x)
        self.y = float(y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.phase = uniform(0, math.tau)
        self.pulse_speed = uniform(1.1, 2.4)
        self.glow_size = randint(24, 36)
        self.glow = pg.Surface((self.glow_size, self.glow_size), pg.SRCALPHA)
        center = self.glow_size // 2

        pg.draw.circle(self.glow, (255, 255, 255, 20), (center, center), center)
        pg.draw.circle(self.glow, (255, 255, 255, 38), (center, center), int(center * 0.65))
        pg.draw.circle(self.glow, (255, 255, 255, 70), (center, center), int(center * 0.30))

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < -20:
            self.x = WEIGHT + 20
            self.y = randint(0, HEIGHT)
        if self.x > WEIGHT + 20:
            self.x = -20
            self.y = randint(0, HEIGHT)
        if self.y > HEIGHT + 20:
            self.y = -20
            self.x = randint(0, WEIGHT)

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen):
        time = pg.time.get_ticks() / 1000
        pulse = (math.sin(time * self.pulse_speed + self.phase) + 1) / 2
        alpha = 45 + int(pulse * 75)
        size = self.glow_size + int(pulse * 6)
        glow = pg.transform.smoothscale(self.glow, (size, size))
        glow.set_alpha(alpha)
        glow_rect = glow.get_rect(center=self.rect.center)

        screen.blit(
            glow,
            glow_rect
        )

        super().draw(screen)

class SpaceDust:
    # Kosmichnyi pyl: dribni napivprozori tochky, yaki povilno plyvut.
    def __init__(self):
        self.x = uniform(0, WEIGHT)
        self.y = uniform(0, HEIGHT)
        self.radius = randint(1, 2)
        self.alpha = randint(18, 55)
        self.speed_x = uniform(-0.10, -0.03)
        self.speed_y = uniform(0.03, 0.12)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < -5 or self.y > HEIGHT + 5:
            self.x = uniform(0, WEIGHT)
            self.y = -5

    def draw(self, screen):
        dust = pg.Surface((self.radius * 4, self.radius * 4), pg.SRCALPHA)
        center = self.radius * 2
        pg.draw.circle(dust, (210, 220, 255, self.alpha), (center, center), self.radius)
        screen.blit(dust, (int(self.x), int(self.y)))

class FloatingSprite(Sprite):
    # Lehke "dykhannia" Marsa: rukh lyshe na kil'ka pikseliv.
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.base_x = x
        self.base_y = y
        self.phase = uniform(0, math.tau)

    def update(self):
        time = pg.time.get_ticks() / 1000
        self.rect.x = int(self.base_x + math.sin(time * 0.45 + self.phase) * 3)
        self.rect.y = int(self.base_y + math.cos(time * 0.35 + self.phase) * 2)

class Meteor:
    # Meteor bere kartynku meteor.png. Yakshcho yii shche nemaie, bude tymchasova smuha.
    def __init__(self, image):
        self.image = image
        self.active = False
        self.next_spawn = pg.time.get_ticks() + randint(2500, 6500)
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0

    def spawn(self):
        self.active = True
        self.x = uniform(-160, WEIGHT * 0.75)
        self.y = uniform(-80, HEIGHT * 0.25)
        self.speed_x = uniform(7.5, 10.5)
        self.speed_y = uniform(3.5, 5.5)

    def update(self):
        now = pg.time.get_ticks()
        if not self.active:
            if now >= self.next_spawn:
                self.spawn()
            return

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x > WEIGHT + 180 or self.y > HEIGHT + 120:
            self.active = False
            self.next_spawn = now + randint(3500, 8500)

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (int(self.x), int(self.y)))

class Base(Sprite):
    def __init__(self, x, y, image,location):
        super().__init__(x, y, image)
        self.entry = pg.Rect(x+100, y+200, 25, 25)
        self.location = location
    def update(self,player):
        if self.entry.colliderect(player):
            player.rect.x = 450
            player.rect.y = 300
            return self.location
        return None

class Workbench(Sprite):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.was_colliding = False

    def update(self, player):
        colliding = self.rect.colliderect(player.rect)
        should_open = colliding and not self.was_colliding
        self.was_colliding = colliding
        return should_open

class Teleport(Sprite):
    def __init__(self, x, y, image, target_location):
        super().__init__(x, y, image)
        self.location = target_location
    def update(self, player):
        if self.rect.colliderect(player):
            return self.location
        return None

# ------ Шрифти ------
font_win = pg.font.Font(None, 72)
font_main = pg.font.Font(None, 36)
font_pixel = pg.font.Font("data/fonts/Minecraftia.ttf", 24)

impt.load_and_inject_assets()

from data.modules.imports import *

pl = Player(1200, 1200, walk_down, walk_right, walk_left, walk_up, walk_down, 
            walk_down_left, walk_down_right, walk_up_left, walk_up_right, die)
sprites = []

# Головне Вікно

MUSIC_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(MUSIC_END)
WEIGHT, HEIGHT = 900, 600
settings_data = load_settings()
is_fullscreen = settings_data.get("fullscreen", False)

def apply_display_mode():
    global screen
    flags = pg.SCALED
    if is_fullscreen:
        flags |= pg.FULLSCREEN
    screen = pg.display.set_mode((WEIGHT, HEIGHT), flags)

apply_display_mode()
pg.display.set_caption("Mars")
pg.display.set_icon(pg.image.load("data/images/gui/icons/icon.ico"))
exit_rect = Teleport(398,401,pg.Surface((144,54)),'basic')
music_loud = settings_data.get("music_loud", 0.50)
sounds_loud = settings_data.get("sounds_loud", 0.50)
selected_difficulty = settings_data.get("difficult", 1)

mars_bg = FloatingSprite(788, 29, mars)
settings_btn = Button(232, 240, settings1, settings_actv, btn_collision, btn_click)
play_btn = Button(232, 45, play1, play_actv, btn_collision, btn_click)
exit_btn = Button(232, 435, exit1, exit_actv, btn_collision, btn_click)
back_btn = Button(60, 70, back1, back_actv, btn_collision, btn_click)

settings_title = TextLabel(315, 150, 56, WHITE, "Settings")
music_label = TextLabel(235, 255, 36, WHITE, "Music")
sounds_label = TextLabel(235, 350, 36, WHITE, "Sounds")
selected_portrait = None
sleep_bed = Sleep(575, 216, pg.Surface((100, 200), pg.SRCALPHA), "basic")


background1 = Sprite(0, 0, background_basic_img)
home_background = Sprite(0, 0, home_bg_img)
base_home = Base(1250, 1250, base_img,"base")
workbench = Workbench(259, 235, pg.Surface((121, 184)))
MAP_WIDTH = max(background_basic_img.get_width(), WEIGHT * 2)
MAP_HEIGHT = max(background_basic_img.get_height(), HEIGHT * 2)
camera_x = 0
camera_y = 0
camera_box = pg.Rect(WEIGHT // 2 - 80, HEIGHT // 2 - 60, 160, 120)
new_day_bg = Sprite(0, 0, start_day_img)
new_day = True
days = 1
days_label = TextLabel(50, 50, 24, WHITE, f"Day {days}", font_pixel)
wt = 0
stats = TextLabel(50, 20, 24, WHITE, "STATS")
hp_bare_width = 200
hp_bare = Bare(25, 40, hp_bare_width, RED)
hp_icon = Sprite(130,40, hp_icon_img)
o2_bare_width = 200
o2_bare = Bare(25, 70, o2_bare_width, BLUE)
o2_icon = Sprite(130,70, o2_icon_img)
sleep_bare_width = 200
sleep_bare = Bare(25, 100, sleep_bare_width, PURPLE)
sleep_icon = Sprite(130,100, sleep_icon_img)
hunger_bare_width = 200
hunger_bare = Bare(25, 130, hunger_bare_width, ORANGE)
hunger_icon = Sprite(130,130, hunger_icon_img)

alpha_nd = 255

stars_sprite = []
star_layers = [
    (35, 0.55, -0.05, 0.015),
    (42, 0.80, -0.10, 0.025),
    (48, 1.10, -0.16, 0.035),
]

for count, scale, speed_x, speed_y in star_layers:
    for i in range(count):
        s = MenuStar(
            randint(1, WEIGHT - 2),
            randint(1, HEIGHT - 2),
            stars[randint(0, len(stars) - 1)],
            uniform(scale * 0.75, scale * 1.25),
            uniform(speed_x * 1.30, speed_x * 0.70),
            uniform(speed_y * 0.70, speed_y * 1.30)
        )
        stars_sprite.append(s)

dust_sprite = [SpaceDust() for i in range(70)]
meteors = [Meteor(meteor_img)]

stone = Mineral(-100,-100, stone_img, "stone")
not_enough_sleep_label = TextLabel(WEIGHT//2, HEIGHT//2, 48, RED, "Ви занадто втомилися!", font_pixel)
stone_icon = Sprite(814,555, stone_icon_img)
stone_text = TextLabel(871, 555, 24, WHITE, f"{pl.resources['stone']}", font_pixel)
iron = Mineral(-100,-100, iron_img, "iron")
iron_icon = Sprite(814,508, iron_icon_img) 
iron_text = TextLabel(871, 508, 24, WHITE, f"{pl.resources['iron']}", font_pixel)
rubin = Mineral(-100,-100, rubin_img, "rubin")
rubin_icon = Sprite(814,461, rubin_icon_img)
rubin_text = TextLabel(871, 461, 24, WHITE, f"{pl.resources['rubin']}", font_pixel)
gips = Mineral(-100,-100, gips_img, "gips")
gips_icon = Sprite(814,414, gips_icon_img)
gips_text = TextLabel(871, 414, 24, WHITE, f"{pl.resources['gips']}", font_pixel)
minerals = [stone, iron, rubin, gips]

def draw_menu_background():
    screen.fill(BLACK)
    for s in stars_sprite:
        s.draw(screen)
    for d in dust_sprite:
        d.draw(screen)
    for m in meteors:
        m.draw(screen)
    mars_bg.draw(screen)

def update_menu_background():
    mars_bg.update()
    for s in stars_sprite:
        s.update()
    for d in dust_sprite:
        d.update()
    for m in meteors:
        m.update()

def open_settings_menu():
    global music_loud, sounds_loud, is_fullscreen

    music_slider = Slider(360, 270, 260, music_loud)
    sounds_slider = Slider(360, 365, 260, sounds_loud)
    panel = pg.Rect(140, 110, 620, 360)
    overlay = pg.Surface((WEIGHT, HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    fullscreen_box = pg.Rect(360, 432, 24, 24)
    fullscreen_label = TextLabel(395, 430, 28, WHITE, "Fullscreen")
    back_btn.onclick(lambda: None)
    back_btn.rect.x = 60
    back_btn.rect.y = 70

    settings_open = True
    while settings_open:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == MUSIC_END:
                play_random_menu_music()

            music_slider.handle_event(event)
            sounds_slider.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if fullscreen_box.collidepoint(event.pos):
                    is_fullscreen = not is_fullscreen
                    apply_display_mode()
                    save_settings()

        def close_settings():
            nonlocal settings_open
            save_settings()
            settings_open = False

        back_btn.onclick(close_settings)
        back_btn.update()

        update_menu_background()
        music_loud = music_slider.value
        sounds_loud = sounds_slider.value
        pg.mixer.music.set_volume(music_loud)
        for s in sounds:
            s.set_volume(sounds_loud)

        draw_menu_background()
        screen.blit(overlay, (0, 0))
        pg.draw.rect(screen, (18, 18, 24), panel, border_radius=14)
        pg.draw.rect(screen, (95, 85, 70), panel, 2, border_radius=14)

        settings_title.draw(screen)
        music_label.draw(screen)
        sounds_label.draw(screen)
        music_slider.draw(screen)
        sounds_slider.draw(screen)
        pg.draw.rect(screen, WHITE, fullscreen_box, 2)
        if is_fullscreen:
            pg.draw.line(screen, WHITE, (fullscreen_box.x + 5, fullscreen_box.y + 12), (fullscreen_box.x + 10, fullscreen_box.y + 18), 3)
            pg.draw.line(screen, WHITE, (fullscreen_box.x + 10, fullscreen_box.y + 18), (fullscreen_box.x + 19, fullscreen_box.y + 6), 3)
        fullscreen_label.draw(screen)
        back_btn.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

def open_new_game_menu():
    global music_loud, sounds_loud, screen, selected_portrait,sprites
    def on_fem():
        global selected_portrait
        selected_portrait = "female"
    def on_male():
        global selected_portrait
        selected_portrait = "male"
    def easy():
        global selected_difficulty
        selected_difficulty = "easy"
        save_selected_difficulty()
    def medium():
        global selected_difficulty
        selected_difficulty = "medium"
        save_selected_difficulty()
    def hard():
        global selected_difficulty
        selected_difficulty = "hard"
        save_selected_difficulty()
    def on_landing():
        global game_part
        nonlocal start_1_open
        start_1_open = False
        save_selected_difficulty()
        fade_to_black(draw_menu_scene)
        game_part = "game"
        fade_from_black(draw_game_scene)
    def close_menu():
        nonlocal start_1_open
        start_1_open = False
    female_portrait = Button(123, 104, female_portrait_img, female_actv_img,btn_collision, btn_click)
    male_portrait = Button(559, 104, male_portrait_img, male_actv_img,btn_collision, btn_click)
    female_portrait.onclick(on_fem)
    male_portrait.onclick(on_male)
    prepare_label = TextLabel(235, 61, 45, WHITE, "Choose difficulty and character")
    diff_easy = Button(51, 394, easy_img, easy_actv_img,btn_collision, btn_click, False)
    diff_medium = Button(348, 394, medium_img, medium_actv_img,btn_collision, btn_click, False)
    diff_hard = Button(656, 394, hard_img, hard_actv_img,btn_collision, btn_click, False)
    border_sprite = Sprite(-500, -500, border_img)
    diff_easy.onclick(easy)
    diff_medium.onclick(medium)
    diff_hard.onclick(hard)
    landing = Button(263, 477, landing_img, landing_img, btn_collision, btn_click)
    landing.onclick(on_landing)
    back_btn.onclick(lambda: None)
    sprites = [female_portrait, male_portrait, diff_easy, diff_medium, diff_hard, landing, border_sprite]

    start_1_open = True
    while start_1_open:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == MUSIC_END:
                play_random_menu_music()
        diff_easy.update()
        diff_medium.update()
        diff_hard.update()
        update_menu_background()
        female_portrait.update()
        male_portrait.update()
        landing.update()
        back_btn.onclick(close_menu)
        back_btn.update()
        back_btn.rect.x = 10
        back_btn.rect.y = 10

        if not start_1_open:
            break


        if selected_portrait == "female":
            female_portrait.image = female_portrait.image_active
            male_portrait.image = male_portrait.image_inactive
        elif selected_portrait == "male":
            female_portrait.image = female_portrait.image_inactive
            male_portrait.image = male_portrait.image_active
        if selected_difficulty == "easy":
            border_sprite.rect.x = diff_easy.rect.x - 2
            border_sprite.rect.y = diff_easy.rect.y - 2
        elif selected_difficulty == "medium":
            border_sprite.rect.x = diff_medium.rect.x - 2
            border_sprite.rect.y = diff_medium.rect.y - 2
        elif selected_difficulty == "hard":
            border_sprite.rect.x = diff_hard.rect.x - 2
            border_sprite.rect.y = diff_hard.rect.y - 2


        screen.fill(BLACK)

        draw_menu_background()
        for s in sprites:
            s.draw(screen)
        

        pg.display.flip()
        clock.tick(FPS)

def calculate_bars(player):
    global hp_bare_width, o2_bare_width, sleep_bare_width, hunger_bare_width
    hp_bare_width = player.hp
    o2_bare_width = player.o2
    sleep_bare_width = player.sleep
    hunger_bare_width = player.hunger

play_random_menu_music()

def menu():
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == MUSIC_END:
                play_random_menu_music()
    def on_start():
        open_new_game_menu()
    def on_exit():
        pg.quit()
    def settings():
        open_settings_menu()
    sprites = [mars_bg,settings_btn,play_btn,exit_btn]


    play_btn.onclick(on_start)
    exit_btn.onclick(on_exit)
    settings_btn.onclick(settings)

    exit_btn.update()
    settings_btn.update()
    update_menu_background()
    for s in sounds:
        s.set_volume(sounds_loud)

    draw_menu_background()
    for s in sprites:
            s.draw(screen)
    play_btn.update()

    pg.display.flip()
    clock.tick(FPS)


def update_game_camera():
    global camera_x, camera_y

    player_screen_x = pl.rect.centerx - camera_x
    player_screen_y = pl.rect.centery - camera_y

    if player_screen_x < camera_box.left:
        camera_x = pl.rect.centerx - camera_box.left
    elif player_screen_x > camera_box.right:
        camera_x = pl.rect.centerx - camera_box.right

    if player_screen_y < camera_box.top:
        camera_y = pl.rect.centery - camera_box.top
    elif player_screen_y > camera_box.bottom:
        camera_y = pl.rect.centery - camera_box.bottom

    camera_x = max(0, min(camera_x, MAP_WIDTH - WEIGHT))
    camera_y = max(0, min(camera_y, MAP_HEIGHT - HEIGHT))

def clamp_player_to_map():
    pl.rect.x = max(0, min(pl.rect.x, MAP_WIDTH - pl.rect.width))
    pl.rect.y = max(0, min(pl.rect.y, MAP_HEIGHT - pl.rect.height))
not_enough_sleep_timer = 0
location = "basic"
right_wall = Sprite(654, 42, pg.Surface((58, 429)))
left_wall = Sprite(230,42, pg.Surface((58, 429)))
up_wall = Sprite(237, 27, pg.Surface((452, 122)))
down_wall = Sprite(237, 455, pg.Surface((452, 122)))
def game():
    global game_part, new_day, wt, alpha_nd, location, not_enough_sleep_timer, days,actv_minerals, camera_x, camera_y, not_enough_sleep_timer, right_wall, left_wall, up_wall, down_wall, location
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            open_pause_menu()
            if game_part != "game":
                return
        if event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
            try:
                open_console()
            except Exception as e:
                print(f"Помилка відкриття консолі: {e}")


    screen.fill(BLACK)
    if new_day:
        days_label.set_text(f"Day {days}")
        new_day_bg.image.set_alpha(255)
        days_label.image.set_alpha(255)
        if wt == 0 and pl.items['food'] > 0:
            pl.items['food'] -= 1
            pl.hunger += 50
            if pl.hunger > 100:
                pl.hunger = 100
        if wt == 0 and pl.items[''] > 0:
            pl.items['food'] -= 1
            pl.hunger += 50
            if pl.hunger > 100:
                pl.hunger = 100
        if wt > 170:
            background1.draw(screen, camera_x, camera_y)
            pl.rect.x = 1200
            pl.rect.y = 1200
            pl.draw(screen, camera_x, camera_y)
            days_label.set_text(f"Day {days}")
            new_day_bg.image.set_alpha(alpha_nd)
            days_label.image.set_alpha(alpha_nd)
            new_day_bg.draw(screen, 0, 0)
            days_label.draw(screen)
            if alpha_nd <= 0:
                new_day = False
                wt = 0
                alpha_nd = 255
                new_day_bg.image.set_alpha(255)
                days_label.image.set_alpha(255)
            else:
                alpha_nd -= 5
        elif wt == 0:
            actv_minerals = []
            for r in range(difficulty_settings[selected_difficulty]["minerals_per_day"]):
                template = minerals[randint(0, len(minerals) - 1)]
                new_mineral = Mineral(
                    randint(0, MAP_WIDTH - template.rect.width),
                    randint(0, MAP_HEIGHT - template.rect.height),
                    template.image, 
                    template.type
                )
                actv_minerals.append(new_mineral)
            wt += 1
            new_day_bg.draw(screen, 0, 0)
            days_label.draw(screen)
        else:
            wt += 1
            new_day_bg.draw(screen, 0, 0)
            days_label.draw(screen)
            clamp_player_to_map()
            update_game_camera()    

    elif location == "basic":
        pl.o2 -= difficulty_settings[selected_difficulty]["o2_loss_speed"]
        calculate_bars(pl)
        lc = base_home.update(pl)
        if lc != None:
            location = lc
        pl.update([base_home])
        hp_bare.update(hp_bare_width,200)
        o2_bare.update(o2_bare_width,200)
        sleep_bare.update(sleep_bare_width,200)
        hunger_bare.update(hunger_bare_width,200)
        for m in actv_minerals[:]:
            collected_type = m.update(pl)
            if collected_type:
                actv_minerals.remove(m)

        

        background1.draw(screen, camera_x, camera_y)
        for m in actv_minerals:
            m.draw(screen, camera_x, camera_y)
        base_home.draw(screen, camera_x, camera_y)
        pl.draw(screen, camera_x, camera_y)
        for s in [hp_icon, o2_icon, sleep_icon, hunger_icon,stats,hp_bare,o2_bare,sleep_bare,hunger_bare,stone_icon,iron_icon,rubin_icon,gips_icon,stone_text,iron_text,rubin_text,gips_text]:
            s.draw(screen)
        stone_text.set_text(f"{pl.resources['stone']}")
        iron_text.set_text(f"{pl.resources['iron']}")
        rubin_text.set_text(f"{pl.resources['rubin']}")
        gips_text.set_text(f"{pl.resources['gips']}")
        clamp_player_to_map()
        update_game_camera()
    elif location == "base":
        if pl.o2 >= pl.o2_max:
            pl.o2 = pl.o2_max
        if pl.o2 < pl.o2_max:
            pl.o2 += difficulty_settings[selected_difficulty]["o2_recovery_speed"]
        calculate_bars(pl)
        hp_bare.update(hp_bare_width,200)
        o2_bare.update(o2_bare_width,200)
        sleep_bare.update(sleep_bare_width,200)
        hunger_bare.update(hunger_bare_width,200)
        pl.update([left_wall,right_wall,up_wall,down_wall])
        if sleep_bed.rect.colliderect(pl):
            fade_to_black(draw_base_scene)
            nd = sleep_bed.update(pl)
            if nd != None:
                location = nd
            fade_from_black(draw_game_scene)
            return
        nd = exit_rect.update(pl)
        if nd != None:
            location = nd
            pl.rect.x = 1200
            pl.rect.y = 1200
        if workbench.update(pl):
            open_workbench_menu(pl)

    
        home_background.draw(screen)
        pl.draw(screen)
        for s in [hp_icon, o2_icon, sleep_icon, hunger_icon,stats,hp_bare,o2_bare,sleep_bare,hunger_bare,stone_icon,iron_icon,rubin_icon,gips_icon,stone_text,iron_text,rubin_text,gips_text]:
            s.draw(screen)
        stone_text.set_text(f"{pl.resources['stone']}")
        iron_text.set_text(f"{pl.resources['iron']}")
        rubin_text.set_text(f"{pl.resources['rubin']}")
        gips_text.set_text(f"{pl.resources['gips']}")
    if not_enough_sleep_timer > 0:
        not_enough_sleep_label.draw(screen)
        not_enough_sleep_timer -= 1
    if pl.o2 <= 0:
        pl.hp -= difficulty_settings[selected_difficulty]["o2_hp_loss_speed"]
    if pl.hunger <= 0:
        pl.hp -= difficulty_settings[selected_difficulty]["hunger_hp_loss_speed"]
    if  pl.hp <= 0: 
        play_death_animation()
        return
    pl.hunger -= difficulty_settings[selected_difficulty]["hunger_loss_speed"]

    pg.display.flip()
    clock.tick(FPS)

title_gameover = TextLabel(350, 100, 48, WHITE, "Програш", font_pixel)
days_label_gameover = TextLabel(320, 210, 36, WHITE, f"Прожито {days} днів", font_pixel)
menu_button = TextButton(250, 500, "Меню", 300)
def on_menu():
    global game_part
    game_part = "menu"
menu_button.onclick(on_menu)

def game_over():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    menu_button.update()
    screen.fill(RED)
    title_gameover.draw(screen)
    days_label_gameover.draw(screen)
    menu_button.draw(screen)
    
    pg.display.flip()
    clock.tick(50)

while True:
    while game_part == 'menu':
        menu()
    while game_part == 'game':
        game()
    while game_part == 'game_over':
        game_over()
