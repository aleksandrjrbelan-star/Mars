import json
import os
from data.config import SETTINGS_PATH


def load_settings():
    default_settings = {
        "difficult": "none",
        "music_loud": 0.50,
        "sounds_loud": 0.50,
        'portrait': "none",
        "fullscreen": False,
        "lang": "eng"
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

def save_settings(game_settings = True):
    if game_settings:
        settings_data["music_loud"] = round(music_loud, 2)
        settings_data["sounds_loud"] = round(sounds_loud, 2)
        settings_data["difficult"] = selected_difficulty
        settings_data["portrait"] = selected_portrait
    else:
        settings_data["lang"] = selected_language 
    settings_data["fullscreen"] = is_fullscreen
    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings_data, file)

settings_data = load_settings()
selected_difficulty = settings_data.get("difficult", "none")
music_loud = settings_data.get("music_loud", 0.50)
sounds_loud = settings_data.get("sounds_loud", 0.50)
selected_portrait = settings_data.get("portrait", "none")
selected_language = settings_data.get("lang", "eng")
is_fullscreen = settings_data.get("fullscreen", False)