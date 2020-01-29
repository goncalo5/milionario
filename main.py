
# kivy modules:
from kivy.app import App
    # uix:
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.relativelayout import RelativeLayout



class GameApp(App):

    def build(self):
        self.game = Screen()
        return self.game


if __name__ == "__main__":
    GameApp().run()
