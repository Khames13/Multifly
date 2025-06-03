from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line
from kivy.utils import get_color_from_hex as rgb
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
from datetime import timedelta

from payment_screen import PaymentScreen



from random import choice
from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from random import uniform
from kivy.uix.relativelayout import RelativeLayout

import math
import colorsys
import os
import time
import random
import sys
import json


from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image




from datetime import datetime, timedelta

class TimerManager:
    def __init__(self):
        self.level_timers = {}  # Stores remaining time per level
        self.active_level = None
        self.paused_time = None

    def start_level(self, level_name, full_time_seconds):
        """Call when a level is freshly started or retried."""
        self.level_timers[level_name] = timedelta(seconds=full_time_seconds)
        self.active_level = level_name
        self.paused_time = None

    def resume_level(self, level_name):
        """Resume timer for a paused level."""
        self.active_level = level_name
        self.paused_time = datetime.now()

    def pause_level(self, level_name):
        """Pause timer and store remaining time."""
        if self.active_level == level_name and self.paused_time:
            elapsed = datetime.now() - self.paused_time
            self.level_timers[level_name] -= elapsed
        self.paused_time = None

    def get_remaining_time(self, level_name):
        """Return remaining time as timedelta."""
        if self.active_level == level_name and self.paused_time:
            elapsed = datetime.now() - self.paused_time
            return self.level_timers[level_name] - elapsed
        return self.level_timers.get(level_name, timedelta(seconds=0))

    def reset_level(self, level_name, full_time_seconds):
        """Reset level time to full."""
        self.level_timers[level_name] = timedelta(seconds=full_time_seconds)
        self.paused_time = None


class ImageButton(ButtonBehavior, Image):
    pass

# Register Baloo font
LabelBase.register(name='Baloo', fn_regular='assets/fonts/Baloo-Regular.ttf')
LabelBase.register(name='LuckiestGuy', fn_regular='assets/fonts/LuckiestGuy-Regular.ttf')

#WELCOME_SCREEN
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Immediately show a light blue color to block black flash
        with self.canvas.before:
            Color(0.8, 0.9, 1, 1)  # light blue
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

        # Schedule background image loading 1 frame later (avoids black flash)
        Clock.schedule_once(self.add_background_image, 0)

    def update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def add_background_image(self, dt):
        self.bg_image = Image(
            source='assets/backgrounds/background.PNG',
            allow_stretch=True,
            keep_ratio=False,
            opacity=0,  # Start invisible
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.layout.add_widget(self.bg_image)

        # Fade in image smoothly
        Animation(opacity=1, duration=0.5).start(self.bg_image)

    def on_enter(self):
        #App.get_running_app().stop_music()  # 👈 Stop music on welcome
        Clock.schedule_once(self.go_to_loading, 5)

    def go_to_loading(self, dt):
        self.manager.current = 'loading_screen'
        
    def stop_music(self):
        if self.music and self.music.status == 'play':
            self.music.stop()


# --- LOADING_SCREEN ---
class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Aqua solid background
        with self.canvas.before:
            Color(0, 1, 1, 1)  # Aqua
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        # Loading label with Baloo font
        self.loading_label = Label(
            text='Loading',
            font_size='50sp',
            font_name='Baloo',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.loading_label)

        # Create 3 square bullets in front of "Loading"
        self.bullets = []
        spacing = 0.05
        start_x = 0.38
        for i in range(3):
            bullet = Label(
                text='.',
                font_size='70sp',
                pos_hint={'center_x': start_x + i * spacing, 'center_y': 0.6},
                color=(1, 1, 1, 0.4)
            )
            self.layout.add_widget(bullet)
            self.bullets.append(bullet)

        self.blink_index = 0

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self):
        
        self.blink_event = Clock.schedule_interval(self.blink_bullets, 0.5)
        Clock.schedule_once(self.go_to_level_select, 5)

    def blink_bullets(self, dt):
        for i, bullet in enumerate(self.bullets):
            bullet.color = (1, 1, 1, 1 if i == self.blink_index else 0.3)
        self.blink_index = (self.blink_index + 1) % len(self.bullets)

    def go_to_level_select(self, dt):
        if self.blink_event:
            self.blink_event.cancel()
        self.manager.current = 'level_select'


 #LEVEL_SELECT_SCREEN
        
class GlowButton(ButtonBehavior, Label):
    hovering = BooleanProperty(False)
    unlocked = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(GlowButton, self).__init__(**kwargs)
        self.font_size = '20sp'
        self.size_hint = (0.6, None)
        self.height = 80
        self.color = (1, 1, 1, 1)
        self.text_size = self.size
        self.halign = 'center'
        self.valign = 'middle'
        self.padding = (10, 10)

        self.bind(pos=self.update_canvas, size=self.update_canvas, unlocked=self.update_appearance)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.bind(on_press=self.on_press_effect, on_release=self.on_release_effect)

        with self.canvas.before:
            self.shadow_color = Color(0, 0.7, 1, 0.4)
            self.shadow = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

            self.bg_color = Color(1, 0.84, 0, 1)  # Default: Gold
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])

            self.inner_color = Color(0.2, 0.8, 1, 1)
            self.inner = RoundedRectangle(pos=self.pos, size=self.size, radius=[16])

        self.update_appearance()
        
    def animate_button(btn):
        anim = Animation(opacity=0.7, duration=1) + Animation(opacity=1, duration=1)
        anim.repeat = True
        anim.start(btn)

    def update_canvas(self, *args):
        self.shadow.pos = (self.x + 2, self.y - 2)
        self.shadow.size = self.size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.inner.pos = (self.x + 6, self.y + 6)
        self.inner.size = (self.width - 12, self.height - 12)

    def update_appearance(self, *args):
        if not self.unlocked:
            # Gray style for locked
            self.bg_color.rgba = (0.5, 0.5, 0.5, 1)
            self.inner_color.rgba = (0.3, 0.3, 0.3, 1)
            self.color = (0.7, 0.7, 0.7, 1)
        else:
            # Gold glowing style
            self.bg_color.rgba = (1, 0.84, 0, 1)
            self.inner_color.rgba = (0.2, 0.8, 1, 1)
            self.color = (1, 1, 1, 1)

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window() or not self.unlocked:
            return
        self.hovering = self.collide_point(*self.to_widget(*pos))
        if self.hovering:
            self.inner_color.rgba = (0.3, 0.9, 1, 1)
        else:
            self.inner_color.rgba = (0.2, 0.8, 1, 1)

    def on_press_effect(self, *args):
        if self.unlocked:
            self.inner_color.rgba = (0.1, 0.5, 0.8, 1)

    def on_release_effect(self, *args):
        if self.unlocked:
            self.inner_color.rgba = (0.2, 0.8, 1, 1)

class LevelSelectScreen(Screen):
    def __init__(self, **kwargs):
        super(LevelSelectScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        label = Label(text="Select a Level",
                      font_size='32sp',
                      color=(0, 0, 0.5, 1),
                      size_hint=(None, None),
                      size=(300, 50),
                      pos_hint={"center_x": 0.5, "top": 0.95})
        self.layout.add_widget(label)

        scroll = ScrollView(size_hint=(1, 0.75), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.grid = GridLayout(cols=3, spacing=[20, 40], padding=[30, 40], size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        scroll.add_widget(self.grid)
        self.layout.add_widget(scroll)

        self.back_btn = Button(text="Back",
                               font_size='20sp',
                               size_hint=(0.2, 0.08),
                               pos_hint={"x": 0.05, "y": 0.05})
        self.back_btn.bind(on_release=lambda *args: setattr(self.manager, 'current', 'welcome'))
        self.layout.add_widget(self.back_btn)

        # 🔇 Mute/Unmute Toggle Button
        self.music_toggle_btn = Button(text="🔊",
                                       font_size='24sp',
                                       size_hint=(None, None),
                                       size=(60, 60),
                                       pos_hint={"right": 0.98, "top": 0.98},
                                       background_color=(0.8, 0.8, 0.8, 1))
        self.music_toggle_btn.bind(on_release=self.toggle_music)
        self.layout.add_widget(self.music_toggle_btn)

        # Load sounds
        self.level_select_sound = SoundLoader.load('assets/sounds/level_select.wav')
        self.level_button_click_sound = SoundLoader.load('assets/sounds/level_button_click.wav')

        if self.level_select_sound:
            self.level_select_sound.loop = True

        # ===== Add secret button here =====
        secret_btn = Button(
            text=".",
            font_size='24sp',
            size_hint=(None, None),
            size=(30, 30),
            
            pos_hint={"right": 0.96, "y": 0.01},  # bottom-right corner
            background_color=(0, 0, 0, 0),  # semi-transparent red
            color=(1, 0, 0, 1))  # Red dot
            
        secret_btn.bind(on_release=self.open_secret_area)
        self.layout.add_widget(secret_btn)
        from kivy.animation import Animation

    def flash(btn):
            anim = Animation(background_color=(1, 0, 0, 1), duration=0.5) + Animation(background_color=(1, 0, 0, 0.5), duration=0.5)
            anim.repeat = True
            anim.start(btn)

            flash(secret_btn)


    def open_secret_area(self, *args):
        # You can define what happens here when secret button is pressed
        print("Secret area unlocked!")
        # For example, switch to a secret screen:
        # self.manager.current = 'secret_screen'

    def on_enter(self):
        self.create_level_buttons()

        app = App.get_running_app()
        if app.music:
            app.reduce_main_volume()

        # Delay before playing level_select sound
        Clock.schedule_once(self.play_level_select_sound, 0.015)

        # Resume main music if needed
        Clock.schedule_once(self.play_main_music, 0.01)
        
        

    def on_leave(self):
        # Stop the level select sound
        if self.level_select_sound and self.level_select_sound.state == 'play':
            self.level_select_sound.stop()

        # Restore main music volume
        app = App.get_running_app()
        if app.music:
            app.restore_main_volume()
            
            from kivy.animation import Animation

   
    def create_level_buttons(self):
        self.level_buttons = {}  # Dictionary to hold level buttons
        self.grid.clear_widgets()

        app = App.get_running_app()

        for i in range(1, 16):  # Levels 1 to 15
            btn = GlowButton(text=f"Level {i}")
            btn.unlocked = (i in app.unlocked_levels)  # Use app.unlocked_levels to control unlock state
            btn.disabled = not btn.unlocked
            btn.bind(on_release=lambda btn, lvl=i: self.select_level(lvl) if btn.unlocked else None)
            self.grid.add_widget(btn)
            self.level_buttons[i] = btn  # Store button by level number
        if btn.unlocked:
            animate_button(btn)
            
    def show_upgrade_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        message = Label(
            text="This level is available for Premium members only.\nUpgrade now to unlock all levels!",
            halign="center",
            valign="middle"
        )
        message.bind(size=message.setter('text_size'))  # Enable text wrapping

        button_layout = BoxLayout(spacing=10, size_hint_y=0.3)

        upgrade_button = Button(text="Upgrade")
        cancel_button = Button(text="Cancel")

        # --- Define what happens when buttons are pressed ---
        def upgrade_pressed(instance):
            popup.dismiss()
            self.manager.current = "payment_screen"  # Change to your payment screen name

        def cancel_pressed(instance):
            popup.dismiss()

        # --- Bind buttons to actions ---
        upgrade_button.bind(on_release=upgrade_pressed)
        cancel_button.bind(on_release=cancel_pressed)

        button_layout.add_widget(upgrade_button)
        button_layout.add_widget(cancel_button)

        layout.add_widget(message)
        layout.add_widget(button_layout)

        popup = Popup(title="Premium Feature",
                      content=layout,
                      size_hint=(None, None),
                      size=(400, 300),
                      auto_dismiss=False)
        popup.open()

                
    def shake_button(self, button):
        anim = (
            Animation(pos_hint={'center_x': 0.48}, duration=0.05) +
            Animation(pos_hint={'center_x': 0.52}, duration=0.05) +
            Animation(pos_hint={'center_x': 0.5}, duration=0.05)
        )
        anim.start(button)

            
          

    def create_level_buttons(self):
        self.level_buttons = {}
        self.grid.clear_widgets()

        app = App.get_running_app()
        is_premium = getattr(app, 'is_premium_user', False)

        for i in range(1, 16):
            btn = GlowButton(text=f"Level {i}")
            is_premium_level = (i >= 10)
            is_unlocked = i in app.unlocked_levels

            if is_premium_level and not is_premium:
                # Non-premium user trying to access premium level
                btn.disabled = False  # Still clickable
                btn.unlocked = False

                def make_locked_callback(btn_ref, lvl=i):
                    def on_click(_):
                        self.shake_button(btn_ref)
                        self.show_upgrade_popup()

                    return on_click

                btn.bind(on_release=make_locked_callback(btn))
            else:
                # Level is allowed
                btn.unlocked = is_unlocked
                btn.disabled = not is_unlocked
                btn.bind(on_release=lambda btn, lvl=i: self.select_level(lvl) if btn.unlocked else None)

                #if btn.unlocked:
                    #animate_button(btn)

            self.grid.add_widget(btn)
            self.level_buttons[i] = btn

    def animate_button(button):
        anim = Animation(scale=1.1, duration=0.1) + Animation(scale=1.0, duration=0.1)
        anim.start(button)

       
    def flash_color(btn, color=(1, 1, 0, 1)):
        original_color = btn.background_color
        anim = Animation(background_color=color, duration=0.1) + Animation(background_color=original_color, duration=0.1)
        anim.start(btn)

    def select_level(self, level_number):
        app = App.get_running_app()

        # Play click sound
        if self.level_button_click_sound:
            self.level_button_click_sound.stop()  # Restart if already playing
            self.level_button_click_sound.play()
            if app.music:
                app.reduce_main_volume()
                Clock.schedule_once(lambda dt: app.restore_main_volume(), 1)

        # Transition to game screen
        self.manager.get_screen("game").start_level(level_number)
        self.manager.current = "game"

    def play_main_music(self, dt):
        app = App.get_running_app()
        if app.music and app.music.state != 'play':
            app.play_music()

    def play_level_select_sound(self, dt):
        if self.level_select_sound:
            self.level_select_sound.play()

    def toggle_music(self, instance):
        app = App.get_running_app()
        if app.music:
            if app.music.state == 'play':
                app.music.stop()
                self.music_toggle_btn.text = "🔇"
            else:
                app.music.play()
                self.music_toggle_btn.text = "🔊"
                
# --- GAME SCREEN ---#
class GameScreen(Screen):
    
    level = StringProperty("")
    # At the top of your class or in __init__, set font

    def __init__(self, **kwargs):
        
        super(GameScreen, self).__init__(**kwargs)
        self.time_left = 45
        self.score = App.get_running_app().total_score
        self.current_level_index = 1
        self.question_count = 0
        self.question_count = 0
        self.correct_count = 0
        self.level_complete = False
        self.question_pool = []
        self.mixed_questions = []
        self.answer = ""
        self.correct_answer = ""
        self.auto_check_event = None
        self.hearts = 5
        self.restarts = 3  # Number of restart chances
        self.correct_streak = 0
        self.wrong_streak = 0
        self.correct_count = 0
        self.timer_running = False
        self.timer_event = None
        

        
        # --- Background ---
        with self.canvas.before:
            Color(0.53, 0.81, 0.98, 1)  # Sky blue
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # --- Top Bar ---
        self.top_bar = BoxLayout(orientation='horizontal', size_hint=(1, None), height=70,
                                 pos_hint={"top": 1}, spacing=50, padding=[20, 10, 20, 10 ])
        with self.top_bar.canvas.before:
            Color(0.9, 0.9, 0.98, 1)  # Lavender
            self.top_bar_rect = Rectangle(pos=self.top_bar.pos, size=self.top_bar.size)
            self.top_bar.bind(size=self._update_top_bar_rect, pos=self._update_top_bar_rect)

        # --- Top Bar Widgets ---
        self.score_icon = Image(source="assets/images/score.png", size_hint=(None, None), size=(50, 50))
        self.score_label = Label(text="", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, 1), width=80)

        self.heart_icon = Image(source="assets/images/heart.png", size_hint=(None, None), size=(60, 60))
        self.heart_label = Label(text="", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, 1), width=80)

        self.restart_icon = Image(source="assets/images/restarts.png", size_hint=(None, None), size=(60, 60))
        self.restart_label = Label(text="", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, 1), width=80)

        self.timer_icon = Image(source="assets/images/timer.png", size_hint=(None, None), size=(60, 60))
        self.timer_label = Label(text="", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, 1), width=80)

        self.level_icon = Image(source="assets/images/level.png", size_hint=(None, None), size=(50, 50))
        self.level_label = Label(text="", font_size='18sp', color=(0, 0, 0, 1), size_hint=(None, 1), width=100)
        
                  # --- Canvas Background Behind Answer Area and Keypad ---
        self.canvas_image = Image(
            source='assets/images/canvas.png',
            size_hint=(None, None),
            size=(610, 200),  # Adjust this size as needed to fit behind the input + keypad
            pos_hint={"center_x": 0.5, "y": 0.68}  # Adjust vertical placement
        )
        self.layout.add_widget(self.canvas_image)
        #feedback
        self.feedback_image = Image(source="", size_hint=(None, None), size=(100, 100),
                                    pos_hint={"center_x": 0.50, "top": 0.65}, opacity=0)
        self.layout.add_widget(self.feedback_image)
        self.glow_image = Image(source='assests/images/tick.png')

        # --- Add widgets to top bar ---
        for widget in [
            self.score_icon, self.score_label,
            self.heart_icon, self.heart_label,
            self.restart_icon, self.restart_label,
            self.timer_icon, self.timer_label,
            self.level_icon, self.level_label
        ]:
            self.top_bar.add_widget(widget)

        self.layout.add_widget(self.top_bar)

        # --- Question Label ---
        self.question_label = Label(text="", font_size='250sp',
                                    size_hint=(None, None), size=(400, 100),
                                    pos_hint={"center_x": 0.5, "top": 0.85})
        self.layout.add_widget(self.question_label)
    

        
        # --- Input Label ---
        self.input_label = Label(text="", font_size='72sp',
                                 size_hint=(None, None), size=(200, 80),
                                 pos_hint={"center_x": 0.5, "top": 0.65})
        self.layout.add_widget(self.input_label)

        # --- Keypad ---
        self.create_keypad()

        # --- Back Button ---
        back_btn = Button(text="Back", size_hint=(0.2, 0.08), pos_hint={"x": 0.02, "y": 0.01})
        back_btn.bind(on_release=lambda *args: setattr(self.manager, 'current', 'level_select'))
        self.layout.add_widget(back_btn)

        # --- Quit Button ---
        quit_btn = Button(text="Quit", size_hint=(0.2, 0.08), pos_hint={"right": 0.98, "y": 0.01})
        quit_btn.bind(on_release=self.quit_game)
        self.layout.add_widget(quit_btn)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _update_top_bar_rect(self, *args):
        self.top_bar_rect.pos = self.top_bar.pos
        self.top_bar_rect.size = self.top_bar.size

    def start_level(self, level_index):
        self.current_level_index = level_index
        self.current_level = f"level{level_index}"
        self.question_count = 0
        self.answer = ""
        self.correct_count = 0

        app = App.get_running_app()

        # Restore saved time or use full
        self.time_left = app.level_timer_checkpoints.get(self.current_level, 45)

        # Only store checkpoint the first time entering this level
        if self.current_level not in app.level_score_checkpoints:
            app.level_score_checkpoints[self.current_level] = app.total_score

        # Now restore score ONLY if user is non-premium
        if not app.is_premium_user:
            app.total_score = app.level_score_checkpoints[self.current_level]
            self.score = app.total_score
        else:
            self.score = app.total_score  # Keep current progress

        self.update_top_label()
        self.generate_question()
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)
        self.manager.current = "game"
        
    

    def save_timer_checkpoint(self):
        app = App.get_running_app()
        app.level_timer_checkpoints[self.current_level] = self.time_left
        app.save_progress()  # If you save progress persistently
        print(f"[Timer] Saved checkpoint for {self.current_level}: {self.time_left}s left")


    def on_quit_pressed(self):
        app = App.get_running_app()
        if not app.is_premium_user:
            # Reset both total_score and screen score to checkpoint
            if self.current_level in app.level_score_checkpoints:
                app.total_score = app.level_score_checkpoints[self.current_level]
                self.score = app.total_score
                print(f"Non-premium quit: Score reset to checkpoint {self.score}")
        else:
            print("Premium user: score preserved on quit")

        self.manager.current = 'level_select'
            
    def on_quit_pressed(self):
        self.save_timer_checkpoint()

        app = App.get_running_app()
        if not app.is_premium_user:
            # Reset both total_score and screen score to checkpoint
            if self.current_level in app.level_score_checkpoints:
                app.total_score = app.level_score_checkpoints[self.current_level]
                self.score = app.total_score
                print(f"Non-premium quit: Score reset to checkpoint {self.score}")
        else:
            print("Premium user: score preserved on quit")

        self.manager.current = 'level_select'


    def complete_level(self):
        next_level = f"level{self.current_level_index + 1}"
        App.get_running_app().level_score_checkpoints[next_level] = App.get_running_app().total_score
        
    def level_completed(self):
        app = App.get_running_app()

        # Remove the saved timer to reset it next time
        if self.current_level in app.level_timer_checkpoints:
            del app.level_timer_checkpoints[self.current_level]

    # Continue with unlocking next level, etc.




    def update_top_label(self):
        self.score_label.text = f"{self.score}"
        self.heart_label.text = f"x {self.hearts}"
        self.timer_label.text = f"{self.time_left}s"
        self.restart_label.text = f"x {self.restarts}"
        self.level_label.text = f"Level {self.current_level_index}"
        
        
    def animate_button_pop(button):
        # Animate size slightly bigger then back to normal
        pop = Animation(size=(90, 90), duration=0.1) + Animation(size=(80, 80), duration=0.1)
        pop.start(button)
        
        
        
    def create_keypad(self):
        self.keypad = GridLayout(cols=3, rows=4,
                                 spacing=10,
                                 size_hint=(None, None),
                                 size=(280, 370),
                                 pos_hint={"center_x": 0.5, "y": 0.1})

        image_keys = {
            '1': 'one.png',
            '2': 'two.png',
            '3': 'three.png',
            '4': 'four.png',
            '5': 'five.png',
            '6': 'six.png',
            '7': 'seven.png',
            '8': 'eight.png',
            '9': 'nine.png',
            '0': 'zero.png',
            'C': 'cancel.png',
            'OK': 'ok.png'
        }

        self.button_click_sound = SoundLoader.load('assets/sounds/button_click.wav')

        for key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', 'OK']:
            img_path = f"assets/images/{image_keys[key]}"
            img_button = ImageButton(source=img_path,
                                     size_hint=(None, None),
                                     size=(80, 80))

            # Disable OK button completely
            if key == 'OK':
                img_button.disabled = True  # Makes it non-clickable
                # PULSE ANIMATION
           
            def on_click(instance, k=key):
                if self.button_click_sound:
                    self.button_click_sound.play()

                anim = Animation(size=(100, 100), duration=0.1) + Animation(size=(80, 80), duration=0.1)
                anim.start(instance)

                if k == 'C':
                    self.clear_input(None)
                elif k != 'OK':
                    self.on_key_press_custom(k)  # will handle input logic

            img_button.bind(on_release=on_click)
            self.keypad.add_widget(img_button)

        self.layout.add_widget(self.keypad)
        
       
    def on_key_press_custom(self, key):
        self.answer += key
        self.input_label.text = self.answer

        # Auto-submit if length matches correct answer
        if len(self.answer) == len(str(self.correct_answer)):
            # Cancel any existing scheduled check to prevent double triggers
            if hasattr(self, 'auto_check_event') and self.auto_check_event:
                self.auto_check_event.cancel()

            # Schedule answer check after 10 milliseconds (0.01 sec)
            self.auto_check_event = Clock.schedule_once(self.auto_check_answer, 0.25)


    def generate_question(self):
        
        if self.question_count >= 9:
            self.level_complete = True
            Clock.unschedule(self.update_timer)

            # --- Show end-of-level feedback ---
            if self.correct_count == 9:
                self.question_label.text = "🎉 Woohoo! You are King!"
            elif self.correct_count == 8:
                self.question_label.text = "🥈 So Close!"
            else:
                self.question_label.text = "✅ Level Completed"

            next_level = self.current_level_index + 1
            app = App.get_running_app()
            user_is_premium = getattr(app, 'is_premium_user', False)

            if next_level <= 15:
                if next_level not in app.unlocked_levels:
                    app.unlocked_levels.append(next_level)
                    app.save_progress()
                    print(f"[Progress] Unlocked Level {next_level}")
            else:
                # 🎯 Level 15 completed — FULL RESET
                            
                print("[GAME COMPLETE] Resetting to Level 1.")
                app.unlocked_levels = [1]
                app.total_score = 0         # ✅ Reset total score
                app.hearts = 5              # ✅ Reset hearts
                app.restarts = 3            # ✅ Reset restarts
                app.level_score_checkpoints = {}
                app.level_timer_checkpoints = {}
                app.save_progress()

                Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'level_select'), 2)
                return

        # --- Generate Question ---
        if not hasattr(self, 'question_pool') or not self.question_pool:
            if self.current_level_index <= 11:
                # Regular mode
                self.question_pool = list(range(0, 10))
                random.shuffle(self.question_pool)
            else:
                # Mixed mode (levels 12–15): generate 9 random questions from level 1–11
                self.mixed_questions = [
                    (random.randint(0, 11), random.randint(0, 9)) for _ in range(9)
                ]

        if self.current_level_index <= 11:
            a = self.question_pool.pop()
            b = self.current_level_index
        else:
            a, b = self.mixed_questions[self.question_count]

        self.correct_answer = str(a * b)
        self.question_label.text = f"{a} × {b} = ?"
        self.question_count += 1

        self.animate_question_label()

    def animate_question_label(self):
        # Stop existing animations first (if needed)
        Animation.cancel_all(self.question_label)

        # Bounce effect
        bounce = Animation(font_size=90, duration=0.25) + Animation(font_size=70, duration=0.25)
        bounce.start(self.question_label)

        # Glowing color cycle
        colors = ['#FF5733', '#FFC300', '#DAF7A6', '#33FFBD', '#339BFF', '#A633FF']
        total_anim = None

        for hex_color in colors:
            step = Animation(color=rgb(hex_color), duration=0.1)
            total_anim = step if total_anim is None else total_anim + step

        # Loop the color animation
        if total_anim:
            total_anim.repeat = True
            total_anim.start(self.question_label)
            
    def rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [1]

    def on_key_press(self, instance):
        self.answer += instance.text
        self.input_label.text = self.answer

        # Cancel any previous scheduled check
        if self.auto_check_event:
            Clock.unschedule(self.auto_check_event)
            self.auto_check_event = None

        # If input length equals correct answer length, schedule auto-check after 1 second
        if len(self.answer) == len(self.correct_answer):
            self.auto_check_event = Clock.schedule_once(self.auto_check_answer, 1)
        elif len(self.answer) > len(self.correct_answer):
            # If user types more than expected length, clear input and no check
            self.answer = ""
            self.input_label.text = ""

         

            
    def auto_check_answer(self, dt):
        self.auto_check_event = None

        if not hasattr(self, 'correct_sound'):
            self.correct_sound = SoundLoader.load('assets/sounds/correct_sound.mp3')
        if not hasattr(self, 'wrong_sound'):
            self.wrong_sound = SoundLoader.load('assets/sounds/wrong_sound.mp3')

        app = App.get_running_app()

        if self.answer == self.correct_answer:
            self.feedback_image.source = "assets/images/tick.png"
            self.feedback_image.opacity = 1
            self.score += 10
            app.total_score += 10
            self.score = app.total_score
            self.correct_count += 1

            if self.correct_sound:
                self.correct_sound.stop()
                self.correct_sound.play()

        else:
            self.feedback_image.source = "assets/images/wrong.png"
            self.feedback_image.opacity = 1
            self.score = max(0, self.score - 10)
            app.total_score = max(0, app.total_score - 10)
            self.score = app.total_score

            if self.wrong_sound:
                self.wrong_sound.stop()
                self.wrong_sound.play()

            # ❗ Reduce hearts for non-premium users
            if not getattr(app, 'is_premium_user', False):
                self.hearts -= 1
                print(f"Wrong answer. Hearts remaining: {self.hearts}")

                # 🔁 Check if hearts are depleted
                if self.hearts <= 0:
                    print("Out of hearts — non-premium user sent to 'out_of_hearts' screen.")
                    Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'out_of_hearts'), 1)
                    return
            else:
                print("Premium user — no heart reduction.")

        self.update_top_label()
        Clock.schedule_once(lambda dt: self.generate_question(), 1)
        Clock.schedule_once(lambda dt: self.hide_feedback_image(), 0.9)

        self.answer = ""
        self.input_label.text = ""



    def remove_label(*args):
        self.remove_widget(message_label)

        # Chain animations: In → wait → out → remove
        anim_in.bind(on_complete=lambda *a: Clock.schedule_once(lambda dt: anim_out.start(message_label), 0.8))
        anim_out.bind(on_complete=remove_label)

        anim_in.start(message_label)  
           
    def hide_feedback_image(self):
        self.feedback_image.opacity = 0


    def clear_input(self, instance):
        self.answer = ""
        self.input_label.text = ""
       
        
    def submit_answer(self, instance):
        
        if self.answer == self.correct_answer:
            self.question_label.text = "✅ Correct!"
            self.score += 10
           
            if self.correct_sound:
                self.correct_sound.stop()  # Reset if already playing
                self.correct_sound.play()
        else:
            self.question_label.text = "❌ Wrong!"
            self.score = max(0, self.score - 10)
            
            if self.wrong_sound:
                self.wrong_sound.stop()
                self.wrong_sound.play()

        self.update_top_label()
        Clock.schedule_once(lambda dt: self.generate_question(), 1)

        self.answer = ""
        self.input_label.text = ""
        
    def save_timer_checkpoint(self):
        app = App.get_running_app()
        app.level_timer_checkpoints[self.current_level] = self.time_left

      
    def go_back_to_levels(self):
        self.save_timer_checkpoint()
        self.manager.current = "level_select"

   
  
    def update_timer(self, dt):
        self.time_left -= 1
        self.update_top_label()
        
        if self.time_left <= 0:
            Clock.unschedule(self.update_timer)
            self.save_timer_checkpoint()  # Save 0 before timeout
            self.manager.current = "time_up"


    def quit_game(self, *args):
        self.save_timer_checkpoint()
        App.get_running_app().stop()
        sys.exit()


    
        
        
        
        
        
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import BooleanProperty
from kivy.core.window import Window

class HoverLabel(ButtonBehavior, Label):
    hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.original_color = (0, 1, 1, 1)  # Aqua color
        self.hover_color = (0, 0, 0.5, 1)   # Dark blue for underline
        self.color = self.original_color
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.markup = True  # Enable markup for underline

    def on_mouse_pos(self, window, pos):
        if not self.get_root_window():
            return
        collide = self.collide_point(*self.to_widget(*pos))
        self.hovered = collide
        self.update_text_style()

    def update_text_style(self):
        if self.hovered:
            self.text = f"[u][color=000080]{self.text.strip('[]')}</color][/u]"
        else:
            self.text = f"[color=00FFFF]{self.text.strip('[]')}[/color]"
       


        
class OutOfRestartsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        self.remaining_time = timedelta(minutes=60)

        # Countdown display
        self.countdown_label = Label(
            markup=True,
            font_size='40sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.8, None),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        self.layout.add_widget(self.countdown_label)

        # "Upgrade" button-like label with hover
        self.upgrade_label = HoverLabel(
            text="[color=00FFFF]Upgrade[/color]",  # Aqua default
            font_size='42sp',
            markup=True,
            pos_hint={"center_x": 0.5, "center_y": 0.47},
            size_hint=(None, None),
        )

        self.upgrade_label.bind(on_release=self.go_to_payment)
        self.layout.add_widget(self.upgrade_label)

        self.set_label_text()
        Clock.schedule_interval(self.update_countdown, 1)

    def set_label_text(self):
        mins, secs = divmod(self.remaining_time.seconds, 60)
        countdown_time = f"{mins:02d}:{secs:02d}"
        self.countdown_label.text = (
            "Oops! Out of restarts\n"
            "Upgrade or play again after: " + countdown_time + " min"
        )

    def update_countdown(self, dt):
        if self.remaining_time.total_seconds() > 0:
            self.remaining_time -= timedelta(seconds=1)
            self.set_label_text()
        else:
            self.countdown_label.text = "Restarts restored! You can play again."
            return False

    def go_to_payment(self, *args):
        print("Navigating to payment screen...")
        self.manager.current = "payment_screen"  # screen name must match your ScreenManager

    def on_leave(self):
        if hasattr(self, 'event'):
            self.event.cancel()
                        
class OutOfHeartsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

        # Enable markup for clickable text coloring
        self.countdown_label = Label(
            markup=True,
            font_size='40sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.8, None),  # wrap text to 80% of window width
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Text with a colored word "Upgrade"
        self.set_label_text()

        self.layout.add_widget(self.countdown_label)

        # Bind touch on the label
        self.countdown_label.bind(on_ref_press=self.on_ref_press)

    def set_label_text(self, countdown_time="60:00"):
        # \n for new line; [ref=upgrade] for clickable word
        self.countdown_label.text = (
            "Oops! Out of hearts\n"
            "[ref=upgrade][color=0000ff]Upgrade[/color][/ref] or play again after: "
            f"{countdown_time} min"
        )

    def update_countdown(self, dt):
        # Example countdown logic
        mins = 59  # replace with your logic
        secs = 59  # replace with your logic
        countdown_time = f"{mins:02d}:{secs:02d}"
        self.set_label_text(countdown_time)

    def on_ref_press(self, instance, ref):
        if ref == "upgrade":
            self.go_to_payment()

    def go_to_payment(self):
        self.manager.current = "payment_screen"

    def on_leave(self):
        if hasattr(self, 'event'):
            self.event.cancel()
            
# --- Time Up Screen ---
class TimeUpScreen(Screen):
    def __init__(self, **kwargs):
        super(TimeUpScreen, self).__init__(**kwargs)
        layout = FloatLayout()
        self.add_widget(layout)

        label = Label(text="⏰ Time's Up!",
                      font_size='48sp',
                      color=(1, 0, 0, 1),
                      pos_hint={"center_x": 0.5, "center_y": 0.7})
        layout.add_widget(label)

        try_again_btn = Button(text="Try Again",
                               size_hint=(0.3, 0.1),
                               pos_hint={"center_x": 0.5, "center_y": 0.5})
        try_again_btn.bind(on_release=self.try_again)
        layout.add_widget(try_again_btn)

        back_btn = Button(text="Back to Levels",
                          size_hint=(0.3, 0.1),
                          pos_hint={"center_x": 0.5, "center_y": 0.35})
        back_btn.bind(on_release=lambda *args: setattr(self.manager, 'current', 'level_select'))
        layout.add_widget(back_btn)

    def try_again(self, *args):
        app = App.get_running_app()
        game_screen = self.manager.get_screen('game')

        if not getattr(app, 'is_premium_user', False):
            game_screen.restarts -= 1
            game_screen.update_top_label()

            if game_screen.restarts <= 0:
                self.manager.current = 'out_of_restarts'
                return  # Don't continue to start level

        # If user is premium or has restarts left, start level
        game_screen.start_level(game_screen.current_level_index)

            
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

def show_dev_tools(self):
    layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

    reset_btn = Button(text="🔁 Reset Progress")
    toggle_premium_btn = Button(text="🧪 Toggle Premium Mode")
    clear_data_btn = Button(text="🧹 Clear All Data")
    close_btn = Button(text="❌ Close", size_hint_y=None, height="40dp")

    layout.add_widget(reset_btn)
    layout.add_widget(toggle_premium_btn)
    layout.add_widget(clear_data_btn)
    layout.add_widget(close_btn)

    popup = Popup(title="Developer Tools (Debug Mode)", content=layout,
                  size_hint=(None, None), size=("400dp", "400dp"))

    def reset_progress(instance):
        self.unlocked_levels = [1]
        self.save_progress()
        popup.dismiss()

    def toggle_premium(instance):
        self.is_premium_user = not getattr(self, 'is_premium_user', False)
        print(f"Premium mode is now: {self.is_premium_user}")
        popup.dismiss()

    def clear_data(instance):
        import os
        if os.path.exists("progress.json"):
            os.remove("progress.json")
        self.unlocked_levels = [1]
        self.save_progress()
        print("All data cleared.")
        popup.dismiss()

    reset_btn.bind(on_release=reset_progress)
    toggle_premium_btn.bind(on_release=toggle_premium)
    clear_data_btn.bind(on_release=clear_data)
    close_btn.bind(on_release=lambda x: popup.dismiss())

    popup.open()


class MultiFlyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_state = {
            'refill_start_time': None,
            'hearts': 0
            
            # TEMP: Reset saved progress to Level 1

        }
        
        self.hearts = 5
        self.restarts = 3
        self.total_score = 0
        self.unlocked_levels = [1]
        self.level_score_checkpoints = {}
        self.level_timer_checkpoints = {}

        self.is_premium_user = False # Set True to test premium behavior
        self.debug_mode = True  # Set to False before publishing

        self.unlocked_levels = [1]  # Default for both, may be overwritten by load_progress
        self.level_score_checkpoints = {}
        
        self.level_timer_checkpoints = {}  # e.g., { 'level2': 37 }


        self.correct_sound = SoundLoader.load("assets/sounds/correct_sound.mp3")
        self.wrong_sound = SoundLoader.load("assets/sounds/wrong_sound.mp3")

        self.music = SoundLoader.load('assets/sounds/main_music.wav')
        if self.music:
            self.music.loop = True
            self.music.volume = 1.0
        else:
            print("❌ Failed to load main music.")

        self.level_select_sound = SoundLoader.load('assets/sounds/level_select.wav')
        if self.level_select_sound:
            self.level_select_sound.loop = True
            self.level_select_sound.volume = 1.0
        else:
            print("❌ Failed to load level_select.wav")

        self.level_button_click_sound = SoundLoader.load('assets/sounds/level_button_click.wav')
        if not self.level_button_click_sound:
            print("❌ Failed to load level_button_click.wav")

        # Only load progress if user is premium
        self.load_progress()
        



    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(WelcomeScreen(name="welcome"))
        self.screen_manager.add_widget(LoadingScreen(name="loading_screen"))
        self.screen_manager.add_widget(LevelSelectScreen(name="level_select"))
        self.screen_manager.add_widget(GameScreen(name="game"))
        self.screen_manager.add_widget(TimeUpScreen(name="time_up"))
        self.screen_manager.add_widget(OutOfHeartsScreen(name="out_of_hearts"))
        self.screen_manager.add_widget(OutOfRestartsScreen(name="out_of_restarts"))
        self.screen_manager.add_widget(PaymentScreen(name="payment_screen"))

        return self.screen_manager

    def play_music(self):
        if self.music and self.music.state != 'play':
            self.music.play()

    def reduce_main_volume(self):
        if self.music:
            self.music.volume = 0.5

    def restore_main_volume(self):
        if self.music:
            self.music.volume = 1.0
            
    def load_progress(self):
        if self.is_premium_user and os.path.exists("progress.json"):
            try:
                with open("progress.json", "r") as f:
                    data = f.read().strip()
                    if data:
                        progress = json.loads(data)
                        self.unlocked_levels = progress.get("unlocked_levels", [1])
                        self.total_score = progress.get("total_score", 0)
                        self.level_score_checkpoints = progress.get("level_score_checkpoints", {})
                        self.level_timer_checkpoints = progress.get("level_timer_checkpoints", {})
                        self.hearts = progress.get("hearts", 5)
                        self.restarts = progress.get("restarts", 3)

                    else:
                        self.unlocked_levels = [1]
                        self.total_score = 0
                        self.level_score_checkpoints = {}
                        self.level_timer_checkpoints = {}
            except json.JSONDecodeError:
                print("⚠️ progress.json is corrupted or invalid. Resetting progress.")
                self.unlocked_levels = [1]
                self.total_score = 0
                self.level_score_checkpoints = {}
                self.level_timer_checkpoints = {}
        else:
            # Non-premium or missing file: default values
            self.total_score = 0

    def save_progress(self):
        if self.is_premium_user:
            with open("progress.json", "w") as f:
                json.dump({
                    "unlocked_levels": list(self.unlocked_levels),
                    "total_score": self.total_score,
                    "level_score_checkpoints": self.level_score_checkpoints,
                    "level_timer_checkpoints": self.level_timer_checkpoints,
                    "hearts": self.hearts,
                    "restarts": self.restarts
                }, f)



if __name__ == '__main__':
    MultiFlyApp().run()

