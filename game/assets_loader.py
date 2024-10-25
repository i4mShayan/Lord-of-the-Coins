import os
import pygame

def load_assets():
    grandparent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    APP_FOLDER = os.path.join(grandparent_dir, 'assets')

    # Initialize pygame's image and mixer modules if not already initialized
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    # Load Images
    images = {
        "icon": pygame.image.load(os.path.join(APP_FOLDER, "icon.png")),
        "a_star_button": pygame.image.load(os.path.join(APP_FOLDER, "a_star_button.png")),
        "bfs_button": pygame.image.load(os.path.join(APP_FOLDER, "bfs_button.png")),
        "dfs_button": pygame.image.load(os.path.join(APP_FOLDER, "dfs_button.png")),
        "next_button": pygame.image.load(os.path.join(APP_FOLDER, "next_button.png")),
        "crate": pygame.image.load(os.path.join(APP_FOLDER, "crate.png")),
        "treasure": pygame.image.load(os.path.join(APP_FOLDER, "treasure.png")),
        "wall_b": pygame.image.load(os.path.join(APP_FOLDER, "wall_b.png")),
        "wall_l": pygame.image.load(os.path.join(APP_FOLDER, "wall_l.png")),
        "wall_r": pygame.image.load(os.path.join(APP_FOLDER, "wall_r.png")),
        "wall_t": pygame.image.load(os.path.join(APP_FOLDER, "wall_t.png")),
        "wall_lt": pygame.image.load(os.path.join(APP_FOLDER, "wall_lt.png")),
        "wall_lb": pygame.image.load(os.path.join(APP_FOLDER, "wall_lb.png")),
        "wall_rt": pygame.image.load(os.path.join(APP_FOLDER, "wall_rt.png")),
        "wall_rb": pygame.image.load(os.path.join(APP_FOLDER, "wall_rb.png")),
        "wall_tb": pygame.image.load(os.path.join(APP_FOLDER, "wall_tb.png")),
        "wall_lr": pygame.image.load(os.path.join(APP_FOLDER, "wall_lr.png")),
        "wall_3l": pygame.image.load(os.path.join(APP_FOLDER, "wall_3l.png")),
        "wall_3r": pygame.image.load(os.path.join(APP_FOLDER, "wall_3r.png")),
        "wall_3t": pygame.image.load(os.path.join(APP_FOLDER, "wall_3t.png")),
        "wall_3b": pygame.image.load(os.path.join(APP_FOLDER, "wall_3b.png")),
        "wall_4": pygame.image.load(os.path.join(APP_FOLDER, "wall_4.png")),
        "char_s": pygame.image.load(os.path.join(APP_FOLDER, "char_s.png")),
        "ground_l1": pygame.image.load(os.path.join(APP_FOLDER, "ground_l1.png")),
        "ground_l2": pygame.image.load(os.path.join(APP_FOLDER, "ground_l2.png")),
        "ground_d1": pygame.image.load(os.path.join(APP_FOLDER, "ground_d1.png")),
        "ground_d2": pygame.image.load(os.path.join(APP_FOLDER, "ground_d2.png")),
        "ground_ls1": pygame.image.load(os.path.join(APP_FOLDER, "ground_ls1.png")),
        "ground_ls2": pygame.image.load(os.path.join(APP_FOLDER, "ground_ls2.png")),
        "ground_ds1": pygame.image.load(os.path.join(APP_FOLDER, "ground_ds1.png")),
        "ground_ds2": pygame.image.load(os.path.join(APP_FOLDER, "ground_ds2.png")),
        "coin1": pygame.image.load(os.path.join(APP_FOLDER, "coin1.png")),
        "coin2": pygame.image.load(os.path.join(APP_FOLDER, "coin2.png")),
        "coin3": pygame.image.load(os.path.join(APP_FOLDER, "coin3.png")),
        "coin4": pygame.image.load(os.path.join(APP_FOLDER, "coin4.png")),
        "coin5": pygame.image.load(os.path.join(APP_FOLDER, "coin5.png")),
        "coin6": pygame.image.load(os.path.join(APP_FOLDER, "coin6.png")),
        "coin7": pygame.image.load(os.path.join(APP_FOLDER, "coin7.png")),
        "coin8": pygame.image.load(os.path.join(APP_FOLDER, "coin8.png")),
        "character_1": pygame.image.load(os.path.join(APP_FOLDER, "character_1.png")),
        "character_2": pygame.image.load(os.path.join(APP_FOLDER, "character_2.png")),
    }

    # Group related images into tuples for animations
    images["ground_l"] = (images["ground_l1"], images["ground_l2"])
    images["ground_d"] = (images["ground_d1"], images["ground_d2"])
    images["ground_ls"] = (images["ground_ls1"], images["ground_ls2"])
    images["ground_ds"] = (images["ground_ds1"], images["ground_ds2"])
    images["coin"] = [images[f"coin{i}"] for i in range(1, 9)]
    images["character"] = (images["character_1"], images["character_2"])

    # Load Sounds
    sounds = {
        "push": pygame.mixer.Sound(os.path.join(APP_FOLDER, "push.wav")),
        "footstep": pygame.mixer.Sound(os.path.join(APP_FOLDER, "footstep.wav")),
        "metal": pygame.mixer.Sound(os.path.join(APP_FOLDER, "metal.wav"))
    }

    # Load Fonts
    fonts = {
        "text" : pygame.font.Font(os.path.join(APP_FOLDER, "font.ttf"), 16),
        "title" : pygame.font.Font(os.path.join(APP_FOLDER, "font.ttf"), 26),
    }

    # Background Path
    background_path = os.path.join(APP_FOLDER, "background.webp")

    return images, sounds, fonts, background_path
