from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Color, Rectangle
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

Window.size = (600, 400)

class KingScreen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_score = 100
        self.reward_score = 50
        self.reward_current = 0
        self.angle = 0

        # Load sound
        self.crown_sound = SoundLoader.load("assets/sounds/crown.mp3")
        if self.crown_sound:
            self.crown_sound.play()

        # Background
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)  # dark grey
            self.bg_rect = Rectangle(pos=self.pos, size=Window.size)

        # Tilt image (rotates)
        self.tilt = Image(source="assets/images/tilt.png", size_hint=(None, None),
                          size=(150, 150), pos_hint={"center_x": 0.5, "center_y": 0.6}, opacity=0)
        self.add_widget(self.tilt)

        # King image (starts hidden)
        self.king = Image(source="assets/images/king.png", size_hint=(None, None),
                          size=(200, 200), pos_hint={"center_x": 0.5, "center_y": 0.6}, opacity=0)
        self.add_widget(self.king)

        # Text labels
        self.title_label = Label(text="You Are King!",
                                 font_size=48, bold=True, color=(1, 1, 1, 1),
                                 pos_hint={"center_x": 0.5, "center_y": 0.85}, opacity=0)

        self.score_label = Label(text=f"Your Score: {self.player_score}",
                                 font_size=32, color=(0, 1, 0, 1),
                                 pos_hint={"center_x": 0.5, "center_y": 0.25}, opacity=1)

        self.reward_label = Label(text=f"+{self.reward_current}",
                                  font_size=28, color=(1, 0.84, 0, 1),
                                  pos_hint={"center_x": 0.5, "center_y": 0.18}, opacity=0)

        self.add_widget(self.title_label)
        self.add_widget(self.score_label)
        self.add_widget(self.reward_label)

        Clock.schedule_interval(self.update_rotation, 1 / 60)
        Clock.schedule_once(self.start_animations, 0.5)

    def start_animations(self, dt):
        # Show tilt and start counting reward
        Animation(opacity=1, d=1).start(self.tilt)
        anim = Animation(opacity=1, d=1)
        anim.bind(on_complete=lambda *a: self.start_reward_count())
        anim.start(self.reward_label)

    def update_rotation(self, dt):
        self.angle += 1
        self.tilt.canvas.before.clear()
        with self.tilt.canvas.before:
            PushMatrix()
            Rotate(origin=self.tilt.center, angle=self.angle, axis=(0, 0, 1))
        self.tilt.canvas.after.clear()
        with self.tilt.canvas.after:
            PopMatrix()

    def start_reward_count(self):
        self.reward_event = Clock.schedule_interval(self.increment_reward, 0.03)

    def increment_reward(self, dt):
        if self.reward_current < self.reward_score:
            self.reward_current += 1
            self.reward_label.text = f"+{self.reward_current}"
        else:
            Clock.unschedule(self.reward_event)
            Animation(opacity=0, d=0.5).start(self.tilt)
            Clock.schedule_once(self.show_king_and_label, 0.6)

    def show_king_and_label(self, dt):
        # Bounce king image and fade in label
        king_anim = Animation(scale=1.2, d=0.15) + Animation(scale=1.0, d=0.15)
        king_anim += Animation(opacity=1, d=0.5)
        self.king.opacity = 1  # Make visible before animating
        king_anim.start(self.king)

        Animation(opacity=1, d=1).start(self.title_label)


class KingApp(App):
    def build(self):
        return KingScreen()


if __name__ == '__main__':
    KingApp().run()
