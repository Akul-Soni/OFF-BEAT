define mg_w = 1280
define mg_h = 720
define mg_lanes = 8
define mg_tile_w = 160
define mg_tile_y = 610
define mg_tile_h = 110
define mg_tile_labels = ["C","D","E","F","G","A","B","C"]

define mg_note_size = 72
define mg_hit_y = 574
define mg_catch_y = 470
define mg_catch_tol =70

define mg_glove_w = 140
define mg_glove_h = 150
define mg_glove_y = 440
define mg_glove_speed = 750.0
define mg_mouse_follow = 28.0

define mg_win_score = 10
define mg_max_misses = 3

define mg_base_speed = 240.0
define mg_speed_step = 14.0
define mg_max_speed = 380.0
define mg_second_speed_increase = 1.5
define mg_bounce_height = 230.0
define mg_bounce_time = 0.5

define mg_start_delay = 0.8
define mg_spawn_delay = 0.45
define mg_end_delay = 0.9
define mg_press_time = 0.22
define mg_press_depth = 16
define mg_flash_time = 0.45
define mg_glove_press_time = 0.2
define mg_fb_time = 1.1

define mg_allow_retry = False
define mg_debug = False

define mg_bg = "images/mg_bg.png"
define mg_glove = "images/white_glove.png"
define mg_note = "images/note.png"
define chibi = "images/chibi.png"


define mg_music = "audio/mg_music.ogg"
define mg_catch = "audio/catch.ogg"
define mg_bounce = "audio/bounce.ogg"
define mg_miss = "audio/miss.ogg"
define mg_win_sound = "audio/win.ogg"
define mg_lose_sound = "audio/lose.ogg"



define mg_note_symbol = ["\u266a","\u2669","\u266b"]
define mg_flash = {
    "bounce": (255,205,70),
    "miss":(255,110,110),
    "good":(130,225,160),
}
define mg_fb_rgb = {
    "good": (31,157,85),
    "bounce": (217,130,0),
    "miss": (214,45,45),
}

define mg_decor = [
    (210,150,"\u266a"), (1030,190,"\u266b"), (260, 520, "\u2669"),
    (980, 500, "\u266a"), (120, 330, "\u266b"), (1130, 350, "\u2669"),
]

define mg_glove_parts = [
    (34, 72, 76, 56),
    (60, 14, 26, 62),
    (12, 82, 26, 30),
    (84, 66, 26, 26),
]

default game_score = 0
default misses = 0
default win_state = False
default game_finished = False

default mg_prev_rollback = True
default mg_music_on = False


init python:

    import math
    import time

    class melodystate(object):

        def __init__(self):
            self.reset()

        def reset(self):
            self.phase = "idle"
            self.last_time = None
            self.end_timer = 0.0

            self.glove_x = mg_w / 2.0
            self.glove_press = 0.0
            self.left = False
            self.right = False
            self.mouse_control = False
            self.last_mouse_x = None

            self.note_on = False
            self.note_lane = 0
            self.note_x = 0.0
            self.note_y = -100.0
            self.note_state = "fall1"
            self.note_speed = 0.0
            self.note_speed1 = 0.0
            self.note_speed2 = 0.0
            self.note_vy = 0.0
            self.note_gravity = 0.0
            self.note_sym = mg_note_symbol[0]
            self.spawn_timer = mg_start_delay

            self.tile_press = [0.0] * mg_lanes
            self.tile_flash = [0.0] * mg_lanes
            self.tile_kind = ["bounce"] * mg_lanes
            self.particles = []
            self.fb_text = ""
            self.fb_kind = "good"
            self.fb_timer = 0.0

            self.has_bg = False
            self.has_glove = False
            self.has_note = False
            self.glove_img_size = (mg_glove_w, mg_glove_h)
            self.note_img_size = (mg_note_size, mg_note_size)


    def mg_clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def mg_rgba(rgb, alpha):
        a = int(255 * mg_clamp(alpha, 0.0, 1.0))
        return "#%02x%02x%02x%02x" % (rgb[0], rgb[1], rgb[2], a)

    def mg_mix(c1, c2, k):
        k = mg_clamp(k, 0.0, 1.0)
        return "#%02x%02x%02x" % tuple(int(c1[n] + (c2[n] - c1[n]) * k) for n in range(3))

    def mg_fit_size(path, max_w, max_h):
        w, h = renpy.image_size(path)
        s = min(float(max_w) / w, float(max_h) / h)
        return (max(1, int(w * s)), max(1, int(h * s)))

    def mg_sfx(path):
        try:
            if renpy.loadable(path):
                renpy.play(path, channel="sound")
        except Exception:
            pass

    def mg_start_music():
        global mg_music_on
        try:
            if renpy.loadable(mg_music):
                renpy.music.play(mg_music, channel="music", loop=True, fadein=0.5)
                mg_music_on = True
            else:
                mg_music_on = False
        except Exception:
            mg_music_on = False

    def mg_stop_music(fade=0.6):
        global mg_music_on
        if mg_music_on:
            try:
                renpy.music.stop(channel="music", fadeout=fade)
            except Exception:
                pass
            mg_music_on = False

    def reset_melody_game():
        global game_score, misses, win_state, game_finished

        game_score = 0
        misses = 0
        win_state = False
        game_finished = False

        mg.reset()

        try:
            mg.has_bg = renpy.loadable(mg_bg)
        except Exception:
            mg.has_bg = False

        try:
            mg.has_glove = renpy.loadable(mg_glove)
            if mg.has_glove:
                mg.glove_img_size = mg_fit_size(mg_glove, mg_glove_w, mg_glove_h)
        except Exception:
            mg.has_glove = False

        try:
            mg.has_note = renpy.loadable(mg_note)
            if mg.has_note:
                mg.note_img_size = mg_fit_size(mg_note, mg_note_size, mg_note_size)
        except Exception:
            mg.has_note = False

        mg.phase = "playing"
        mg.last_time = time.monotonic()

    def mg_set_key(which, down):
        if which == "left":
            mg.left = down
        else:
            mg.right = down
        if down:
            mg.mouse_control = False

    def mg_burst(x, y, count, symbols, rgb):
        for n in range(count):
            mg.particles.append([
                float(x), float(y), 0.0, 0.75,
                renpy.random.choice(symbols),
                renpy.random.uniform(-90.0, 90.0),
                renpy.random.uniform(-210.0, -90.0),
                renpy.random.randint(28, 44),
                rgb,
            ])

    def mg_pop_text(x, y, text, rgb):
        mg.particles.append([float(x), float(y), 0.0, 0.85, text, 0.0, -80.0, 46, rgb])

    def mg_feedback(text, kind):
        mg.fb_text = text
        mg.fb_kind = kind
        mg.fb_timer = mg_fb_time

    def mg_tile_hit(lane, kind):
        mg.tile_press[lane] = mg_press_time
        mg.tile_flash[lane] = mg_flash_time
        mg.tile_kind[lane] = kind
        mg_burst(lane * mg_tile_w + mg_tile_w / 2.0, mg_tile_y - 10, 5,
                mg_note_symbol, mg_flash[kind])

    def mg_update_effects(dt):
        for i in range(mg_lanes):
            if mg.tile_press[i] > 0.0:
                mg.tile_press[i] = max(0.0, mg.tile_press[i] - dt)
            if mg.tile_flash[i] > 0.0:
                mg.tile_flash[i] = max(0.0, mg.tile_flash[i] - dt)

        if mg.glove_press > 0.0:
            mg.glove_press = max(0.0, mg.glove_press - dt)

        if mg.fb_timer > 0.0:
            mg.fb_timer = max(0.0, mg.fb_timer - dt)

        alive = []
        for p in mg.particles:
            p[2] += dt
            if p[2] < p[3]:
                p[0] += p[5] * dt
                p[1] += p[6] * dt
                p[6] += 160.0 * dt
                alive.append(p)
        mg.particles = alive

    def mg_tile_offset(i):
        t = mg.tile_press[i]
        if t <= 0.0:
            return 0
        prog = 1.0 - t / mg_press_time
        return int(mg_press_depth * math.sin(math.pi * prog))

    def mg_tile_color(i):
        t = mg.tile_flash[i]
        if t <= 0.0:
            return "#ffffff"
        return mg_mix((255, 255, 255), mg_flash[mg.tile_kind[i]], t / mg_flash_time)

    def mg_glow_color(i):
        k = mg_clamp(mg.tile_flash[i] / mg_flash_time, 0.0, 1.0)
        return mg_rgba(mg_flash[mg.tile_kind[i]], 0.45 * k)

    def mg_glove_dy():
        t = mg.glove_press
        if t <= 0.0:
            return 0
        prog = 1.0 - t / mg_glove_press_time
        return int(12 * math.sin(math.pi * prog))

    def mg_particle_color(p):
        return mg_rgba(p[8], 1.0 - p[2] / p[3])

    def mg_fb_color():
        a = mg_clamp(mg.fb_timer / 0.3, 0.0, 1.0)
        return mg_rgba(mg_fb_rgb[mg.fb_kind], a)

    def mg_fb_y():
        prog = 1.0 - mg.fb_timer / mg_fb_time
        return int(168 - 22 * prog)

    def mg_spawn_note():
        lane = renpy.random.randint(0, mg_lanes - 1)
        speed = min(mg_max_speed, mg_base_speed + game_score * mg_speed_step)

        mg.note_on = True
        mg.note_lane = lane
        mg.note_x = lane * mg_tile_w + mg_tile_w / 2.0
        mg.note_y = float(-mg_note_size)
        mg.note_state = "fall1"
        mg.note_speed1 = float(speed)
        mg.note_speed2 = float(speed) * mg_second_speed_increase
        mg.note_speed = mg.note_speed1
        mg.note_vy = 0.0
        mg.note_gravity = 0.0
        mg.note_sym = renpy.random.choice(mg_note_symbol)

    def mg_end(won):
        global win_state, game_finished, melody_complete

        win_state = bool(won)
        melody_complete = win_state
        game_finished = True

        mg.note_on = False
        mg.left = False
        mg.right = False
        mg.phase = "ending"
        mg.end_timer = mg_end_delay

        mg_stop_music(0.4)
        if won:
            mg_sfx(mg_win_sound)
        else:
            mg_sfx(mg_lose_sound)

    def mg_catch_note():
        global game_score

        second_chance = (mg.note_state == "fall2")
        game_score += 1

        mg.glove_press = mg_glove_press_time
        mg_burst(mg.note_x, mg_glove_y + 10, 6, mg_note_symbol, mg_flash["good"])
        mg_pop_text(mg.note_x, mg_glove_y - 20, "+1", mg_fb_rgb["good"])
        if second_chance:
            mg_feedback("Great save!", "good")
        else:
            mg_feedback("Caught!", "good")
        mg_sfx(mg_catch)

        mg.note_on = False
        mg.spawn_timer = mg_spawn_delay

        if game_score >= mg_win_score:
            mg_end(True)

    def mg_bounce_note():
        mg_tile_hit(mg.note_lane, "bounce")
        mg_feedback("Bounce! Catch it again!", "bounce")
        mg_sfx(mg_bounce)

        mg.note_state = "rise"
        v0 = 2.0 * mg_bounce_height / mg_bounce_time
        mg.note_vy = v0
        mg.note_gravity = v0 / mg_bounce_time

    def mg_full_miss():
        global misses

        misses += 1
        mg_tile_hit(mg.note_lane, "miss")
        mg_feedback("Missed!", "miss")
        mg_sfx(mg_miss)

        mg.note_on = False
        mg.spawn_timer = mg_spawn_delay

        if misses >= mg_max_misses:
            mg_end(False)

    def mg_update_glove(dt):
        pos = renpy.get_mouse_pos()
        mx = pos[0] if pos else None

        direction = (1 if mg.right else 0) - (1 if mg.left else 0)

        if direction != 0:
            mg.glove_x += direction * mg_glove_speed * dt
            mg.last_mouse_x = mx
        elif mx is not None:
            if mg.last_mouse_x is not None and abs(mx - mg.last_mouse_x) > 1:
                mg.mouse_control = True
            mg.last_mouse_x = mx
            if mg.mouse_control:
                k = min(1.0, mg_mouse_follow * dt)
                mg.glove_x += (mx - mg.glove_x) * k

        half = mg_glove_w / 2.0
        mg.glove_x = mg_clamp(mg.glove_x, half, mg_w - half)

    def mg_update_note(dt):
        if not mg.note_on:
            mg.spawn_timer -= dt
            if mg.spawn_timer <= 0.0:
                mg_spawn_note()
            return

        if mg.note_state == "rise":
            mg.note_y -= mg.note_vy * dt
            mg.note_vy -= mg.note_gravity * dt
            if mg.note_vy <= 0.0:
                mg.note_vy = 0.0
                mg.note_state = "fall2"
                mg.note_speed = mg.note_speed2
            return

        mg.note_y += mg.note_speed * dt

        if mg.note_y >= mg_catch_y and abs(mg.glove_x - mg.note_x) <= mg_catch_tol:
            mg_catch_note()
            return

        if mg.note_y >= mg_hit_y:
            mg.note_y = float(mg_hit_y)
            if mg.note_state == "fall1":
                mg_bounce_note()
            else:
                mg_full_miss()

    def mg_update():
        if mg.phase not in ("playing", "ending"):
            return

        now = time.monotonic()
        if mg.last_time is None:
            dt = 0.0
        else:
            dt = now - mg.last_time
        mg.last_time = now
        dt = mg_clamp(dt, 0.0, 0.05)

        mg_update_effects(dt)

        if mg.phase == "ending":
            mg.end_timer -= dt
            if mg.end_timer <= 0.0:
                mg.phase = "result"
            return

        mg_update_glove(dt)
        mg_update_note(dt)


default mg = melodystate()


transform mg_fade_in_fast:
    alpha 0.0
    linear 0.35 alpha 1.0

transform mg_fade_in:
    alpha 0.0
    linear 0.5 alpha 1.0

transform mg_pop_in:
    alpha 0.0 yoffset -50
    ease 0.5 alpha 1.0 yoffset 0

transform mg_bob(delay=0.0):
    pause delay
    block:
        ease 1.1 yoffset -14
        ease 1.1 yoffset 0
        repeat


screen melody_game_screen():

    modal True
    zorder 200

    if mg.phase in ("playing", "ending"):
        timer 0.016 repeat True action Function(mg_update)

    if mg.phase == "playing":
        key "keydown_K_LEFT" action Function(mg_set_key, "left", True)
        key "keyup_K_LEFT" action Function(mg_set_key, "left", False)
        key "keydown_K_RIGHT" action Function(mg_set_key, "right", True)
        key "keyup_K_RIGHT" action Function(mg_set_key, "right", False)
        key "keydown_K_a" action Function(mg_set_key, "left", True)
        key "keyup_K_a" action Function(mg_set_key, "left", False)
        key "keydown_K_d" action Function(mg_set_key, "right", True)
        key "keyup_K_d" action Function(mg_set_key, "right", False)

    if mg.phase == "result":
        key "K_RETURN" action Return("done")

    fixed at mg_fade_in_fast:

        if mg.has_bg:
            add im.Scale(mg_bg, mg_w, mg_h)
        else:
            add Solid("#ffffff")

        for i in range(mg_lanes):
            if i % 2 == 0:
                add Solid("#6c5ce714") pos (i * mg_tile_w, 0) xysize (mg_tile_w, mg_tile_y)
            add Solid("#6c5ce722") pos (i * mg_tile_w, 0) xysize (2, mg_tile_y)

        if mg.note_on:
            add Solid("#6c5ce722") pos (mg.note_lane * mg_tile_w, 0) xysize (mg_tile_w, mg_tile_y)

        text "FALLING NOTES":
            size 44
            bold True
            color "#2b2b3a"
            xalign 0.5
            ypos 12
        text "PIANO CATCHER":
            size 20
            color "#6c5ce7"
            xalign 0.5
            ypos 62
        text "Move the glove with the mouse or the Left / Right arrow keys.\nA missed note bounces once; miss it twice and it counts as a miss.":
            size 17
            color "#6a6a80"
            text_align 0.5
            xalign 0.5
            ypos 92

        frame:
            pos (24, 18)
            background Solid("#2b2b3a")
            padding (22, 10)
            vbox:
                spacing 0
                text "SCORE" size 18 color "#b9b4e6"
                text "[game_score] / [mg_win_score]" size 40 bold True color "#ffffff"

        frame:
            xalign 1.0
            xoffset -24
            ypos 18
            background Solid("#2b2b3a")
            padding (22, 10)
            vbox:
                spacing 4
                text "MISSES  [misses] / [mg_max_misses]" size 18 color "#b9b4e6"
                hbox:
                    spacing 10
                    for n in range(mg_max_misses):
                        if n < misses:
                            add Solid("#ff5d5d") xysize (30, 30)
                        else:
                            add Solid("#4a4a63") xysize (30, 30)

        if mg.fb_timer > 0.0:
            text mg.fb_text:
                size 42
                bold True
                color mg_fb_color()
                xalign 0.5
                ypos mg_fb_y()

        add Solid("#1c1c28") pos (0, mg_tile_y - 2) xysize (mg_w, mg_tile_h + 2)

        for i in range(mg_lanes):
            if mg.tile_flash[i] > 0.0:
                add Solid(mg_glow_color(i)) pos (i * mg_tile_w, mg_tile_y - 46) xysize (mg_tile_w, 46)
            fixed:
                pos (i * mg_tile_w, mg_tile_y + mg_tile_offset(i))
                xysize (mg_tile_w, mg_tile_h)
                add Solid("#2b2b3a")
                add Solid(mg_tile_color(i)) pos (3, 0) xysize (mg_tile_w - 6, mg_tile_h - 4)
                text mg_tile_labels[i]:
                    size 24
                    color "#9a9ab0"
                    xalign 0.5
                    ypos mg_tile_h - 42

        if mg.note_on:
            $ nx = int(mg.note_x)
            $ ny = int(mg.note_y)

            if mg.note_state == "fall2":
                add Solid("#ff6a4d55") pos (nx - 4, ny - 130) xysize (8, 90)

            if mg.has_note:
                add im.Scale(mg_note, mg.note_img_size[0], mg.note_img_size[1]):
                    anchor (0.5, 0.5)
                    pos (nx, ny)
            else:
                text mg.note_sym:
                    size 92
                    font "DejaVuSans.ttf"
                    color ("#d9381e" if mg.note_state == "fall2" else "#3b2f6b")
                    anchor (0.5, 0.5)
                    pos (nx, ny)

            if mg_debug:
                add Solid("#ff000040") pos (nx - mg_note_size // 2, ny - mg_note_size // 2) xysize (mg_note_size, mg_note_size)

        $ gx = int(mg.glove_x)
        $ gy = mg_glove_y + mg_glove_dy()

        add Solid("#00000028") pos (gx - 55, mg_glove_y + mg_glove_h - 4) xysize (110, 12)

        fixed:
            pos (gx - mg_glove_w // 2, gy)
            xysize (mg_glove_w, mg_glove_h)

            if mg.has_glove:
                add im.Scale(mg_glove, mg.glove_img_size[0], mg.glove_img_size[1]):
                    xalign 0.5
                    yalign 1.0
            else:
                for (px, py, pw, ph) in mg_glove_parts:
                    add Solid("#2b2b3a") pos (px - 4, py - 4) xysize (pw + 8, ph + 8)
                for (px, py, pw, ph) in mg_glove_parts:
                    add Solid("#ffffff") pos (px, py) xysize (pw, ph)
                add Solid("#d9d6f2") pos (38, 128) xysize (64, 10)
                add Solid("#2b2b3a") pos (88, 90) xysize (22, 3)

        if mg_debug:
            add Solid("#0000ff30") pos (gx - mg_catch_tol, mg_catch_y) xysize (mg_catch_tol * 2, mg_hit_y - mg_catch_y)

        for p in mg.particles:
            text p[4]:
                size p[7]
                font "DejaVuSans.ttf"
                color mg_particle_color(p)
                anchor (0.5, 0.5)
                pos (int(p[0]), int(p[1]))

        if mg.phase == "result":

            add Solid("#141428b0") at mg_fade_in

            for k, (sx, sy, ss) in enumerate(mg_decor):
                text ss:
                    size 54
                    font "DejaVuSans.ttf"
                    color ("#f2b705" if win_state else "#8a8aa3")
                    pos (sx, sy)
                    at mg_bob(k * 0.25)

            frame at mg_pop_in:
                xalign 0.5
                yalign 0.5
                background Solid("#2b2b3a")
                padding (6, 6)

                frame:
                    background Solid("#ffffff")
                    padding (60, 36)
                    xminimum 700

                    vbox:
                        spacing 14
                        xalign 0.5

                        if win_state:
                            text "VICTORY!" size 78 bold True color "#1f9d55" xalign 0.5
                            text "You caught all [mg_win_score] notes.\nThe melody comes back to you." size 26 color "#4a4a63" text_align 0.5 xalign 0.5
                        else:
                            text "GAME OVER" size 78 bold True color "#d62d2d" xalign 0.5
                            text "Three notes slipped away.\nThe melody is still out of reach." size 26 color "#4a4a63" text_align 0.5 xalign 0.5

                        text "Notes caught: [game_score] / [mg_win_score]      Misses: [misses] / [mg_max_misses]" size 22 color "#6a6a80" xalign 0.5

                        hbox:
                            xalign 0.5
                            spacing 24

                            textbutton "Continue":
                                action Return("done")
                                background Solid("#2b2b3a")
                                hover_background Solid("#6c5ce7")
                                text_color "#ffffff"
                                text_hover_color "#ffffff"
                                text_size 30
                                padding (36, 12)

                            if (not win_state) and mg_allow_retry:
                                textbutton "Try Again":
                                    action Return("retry")
                                    background Solid("#6c5ce7")
                                    hover_background Solid("#2b2b3a")
                                    text_color "#ffffff"
                                    text_hover_color "#ffffff"
                                    text_size 30
                                    padding (36, 12)


label melody_game:

    $ mg_prev_rollback = config.rollback_enabled
    $ config.rollback_enabled = False

    $ mg_start_music()

label .round:

    $ reset_melody_game()
    call screen melody_game_screen

    if _return == "retry":
        jump .round

    $ mg_stop_music()
    $ config.rollback_enabled = mg_prev_rollback
    $ renpy.block_rollback()

    with dissolve

    return
