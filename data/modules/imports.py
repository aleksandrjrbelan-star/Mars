import pygame as pg
import os
from data.config import * # Для констант WEIGHT та HEIGHT, якщо вони там

def load_and_inject_assets():
    """
    Автоматично завантажує та масштабує всі ресурси гри,
    створюючи змінні, які будуть доступні в main.py.
    """
    # Отримуємо доступ до глобального простору імен модуля
    gl = globals()

    try:
        # --- 1. АНІМАЦІЇ ГРАВЦЯ ---
        gl['walk_left'] = [pg.image.load(f"data/images/player/walking/left/{i}.png") for i in range(1, 7)]
        gl['walk_right'] = [pg.image.load(f"data/images/player/walking/right/{i}.png") for i in range(1, 7)]
        gl['walk_up'] = [pg.image.load(f"data/images/player/walking/up/{i}.png") for i in range(1, 7)]
        gl['walk_down'] = [pg.image.load(f"data/images/player/walking/down/{i}.png") for i in range(1, 7)]
        gl['walk_down_left'] = [pg.image.load(f"data/images/player/walking/down-left/{i}.png") for i in range(1, 7)]
        gl['walk_down_right'] = [pg.image.load(f"data/images/player/walking/down-right/{i}.png") for i in range(1, 7)]
        gl['walk_up_left'] = [pg.image.load(f"data/images/player/walking/up-left/{i}.png") for i in range(1, 7)]
        gl['walk_up_right'] = [pg.image.load(f"data/images/player/walking/up-right/{i}.png") for i in range(1, 7)]
        
        gl['die'] = [pg.transform.smoothscale(pg.image.load(f"data/images/player/die/{i}.png"), (29, 54)) for i in range(1, 6)]
        gl['die'].append(pg.transform.smoothscale(pg.image.load("data/images/player/die/6.png"), (65, 55)))

        # --- 2. ЕЛЕМЕНТИ ІНТЕРФЕЙСУ (КНОПКИ ТА МЕНЮ) ---
        gl['play1'] = pg.image.load("data/images/gui/buttons/play.png")
        gl['play_actv'] = pg.image.load("data/images/gui/buttons/play2.png")
        
        continue_path = "data/images/gui/buttons/continue.png"
        continue_actv_path = "data/images/gui/buttons/continue2.png"
        
        if os.path.exists(continue_path) and os.path.exists(continue_actv_path):
            gl['continue_img'] = pg.image.load(continue_path)
            gl['continue_actv_img'] = pg.image.load(continue_actv_path)
        else:
            gl['continue_img'] = gl['play1']
            gl['continue_actv_img'] = gl['play_actv']

        gl['settings1'] = pg.image.load("data/images/gui/buttons/settings.png")
        gl['settings_actv'] = pg.image.load("data/images/gui/buttons/settings2.png")
        gl['exit1'] = pg.image.load("data/images/gui/buttons/exit.png")
        gl['exit_actv'] = pg.image.load("data/images/gui/buttons/exit2.png")
        gl['back1'] = pg.image.load("data/images/gui/buttons/back.png")
        gl['back_actv'] = pg.image.load("data/images/gui/buttons/back2.png")
        
        # --- 3. ЛОКАЦІЇ ТА ОТОЧЕННЯ (МЕНЮ) ---
        gl['mars'] = pg.image.load("data/images/background/locations/menu/mars.png")
        gl['star'] = pg.image.load("data/images/background/locations/menu/star1.png")
        gl['star1'] = pg.image.load("data/images/background/locations/menu/star2.png")
        gl['star2'] = pg.image.load("data/images/background/locations/menu/star3.png")
        gl['meteor_img'] = pg.image.load("data/images/background/locations/menu/meteor.png")
        gl['stars'] = [gl['star'], gl['star1'], gl['star2']]

        # --- 4. КНОПКИ СКЛАДНОСТІ ---
        gl['easy_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/easy.png"), (217, 60))
        gl['easy_actv_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/easy2.png"), (217, 60))
        
        gl['medium_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/medium.png"), (217, 60))
        gl['medium_actv_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/medium2.png"), (217, 60))
        
        gl['hard_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/hard.png"), (217, 60))
        gl['hard_actv_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/hard2.png"), (217, 60))

        # --- 5. ПОРТРЕТИ ПЕРСОНАЖІВ ---
        gl['female_portrait_img'] = pg.transform.smoothscale(pg.image.load("data/images/player/portraits/female_astronaut.png"), (232, 235))
        gl['female_actv_img'] = pg.transform.smoothscale(pg.image.load("data/images/player/portraits/female_astronaut_actv.png"), (232, 235))
        
        gl['male_portrait_img'] = pg.transform.smoothscale(pg.image.load("data/images/player/portraits/male_astronaut.png"), (232, 235))
        gl['male_actv_img'] = pg.transform.smoothscale(pg.image.load("data/images/player/portraits/male_astronaut_actv.png"), (232, 235))

        # --- 6. ЗАДНІ ФОНИ ТА ДЕКОР ---
        gl['border_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/border.png"), (221, 64))
        gl['landing_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/buttons/landing.png"), (374, 103))
        gl['background_basic_img'] = pg.image.load("data/images/background/locations/basic/background.png")
        gl['start_day_img'] = pg.image.load("data/images/background/locations/start_day/new_day.png")

        # --- 7. ІКОНКИ СТАТУСУ ---
        gl['hp_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/hp.png"), (20, 20))
        gl['o2_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/o2.png"), (20, 20))
        gl['sleep_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/sleep.png"), (20, 20))
        gl['hunger_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/hunger.png"), (20, 20))

        # --- 8. ТЕКСТУРИ РЕСУРСІВ ТА ЇХНІ ІКОНКИ ---
        gl['stone_img'] = pg.transform.smoothscale(pg.image.load("data/images/resources/stone.png"), (52, 35))
        gl['iron_img'] = pg.transform.smoothscale(pg.image.load("data/images/resources/iron.png"), (52, 35))
        gl['rubin_img'] = pg.transform.smoothscale(pg.image.load("data/images/resources/rubin.png"), (52, 35))
        gl['gips_img'] = pg.transform.smoothscale(pg.image.load("data/images/resources/gips.png"), (52, 35))
        
        gl['stone_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/stone.png"), (32, 32))
        gl['iron_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/iron.png"), (32, 32))
        gl['rubin_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/rubin.png"), (32, 32))
        gl['gips_icon_img'] = pg.transform.smoothscale(pg.image.load("data/images/gui/icons/gips.png"), (32, 32))

        # --- 9. БАЗА ТА ІНТЕР'ЄР ---
        gl['base_img'] = pg.transform.smoothscale(pg.image.load("data/images/background/locations/basic/base.png"), (200, 200))
        gl['home_bg_img'] = pg.transform.smoothscale(pg.image.load("data/images/background/locations/base/base_bg.png"), (WEIGHT, HEIGHT))

        # --- 10. КНОПКИ ПАУЗИ (МАСШТАБОВАНІ) ---
        gl['pause_continue_img'] = pg.transform.smoothscale(gl['continue_img'], (160, 50))
        gl['pause_continue_actv_img'] = pg.transform.smoothscale(gl['continue_actv_img'], (160, 50))
        gl['pause_settings_img'] = pg.transform.smoothscale(gl['settings1'], (160, 50))
        gl['pause_settings_actv_img'] = pg.transform.smoothscale(gl['settings_actv'], (160, 50))
        gl['pause_exit_img'] = pg.transform.smoothscale(gl['exit1'], (160, 50))
        gl['pause_exit_actv_img'] = pg.transform.smoothscale(gl['exit_actv'], (160, 50))

        # --- 11. ЗВУКИ ---
        gl['btn_collision'] = pg.mixer.Sound("data/sounds/sounds/button/btn_collision.wav")
        gl['btn_click'] = pg.mixer.Sound("data/sounds/sounds/button/btn_click.ogg")
        gl['sounds'] = [gl['btn_collision'], gl['btn_click']]

    except pg.error as e:
        print(f"❌ Критична помилка Pygame під час завантаження: {e}")
    except FileNotFoundError as e:
        print(f"❌ Файл не знайдено: {e}")