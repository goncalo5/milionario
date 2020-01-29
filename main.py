
# kivy modules:
from kivy.app import App
from kivy import properties as kp
    # uix:
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.relativelayout import RelativeLayout
# self modules:
from settings import QUESTIONS


class Game(Screen):
    question = kp.StringProperty()
    A = kp.StringProperty()
    B = kp.StringProperty()
    C = kp.StringProperty()
    D = kp.StringProperty()
    current_question = 0

    def __init__(self, **kwargs):
        super().__init__()
        self.update_question()

    def update_question(self):
        question_dict = QUESTIONS[self.current_question]
        self.question = question_dict.get("question")
        self.A = question_dict.get("A")
        self.B = question_dict.get("B")
        self.C = question_dict.get("C")
        self.D = question_dict.get("D")
        self.solution = question_dict.get("solution")

    def check(self, *args):
        print("check", args)
        answer = args[0]
        if answer == self.solution:
            print("correct")
            self.current_question += 1
            if self.current_question == len(QUESTIONS):
                print("YOU WIN", self.manager.current)
                self.manager.current = "game_over_screen"
                print("YOU WIN", self.manager.current)
                return
        else:
            print("incorrect")
            self.current_question = 0
        self.update_question()


class MetaGame(ScreenManager):
    pass


class GameApp(App):

    def build(self):
        self.metagame = MetaGame()
        return self.metagame


if __name__ == "__main__":
    GameApp().run()
