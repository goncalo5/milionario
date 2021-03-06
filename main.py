# python modules:
import random
# kivy modules:
from kivy.app import App
from kivy import properties as kp
from kivy.clock import Clock
    # uix:
from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
# self modules:
from settings import QUESTIONS, FRIENDS, PRETTY_ANSWERS, PRIZES, TIME_TO_CHANGE_MONEY_SCREEN, PROB_OF_A_FRIEND_GETTING_IT_RIGHT


class MoneyScreen(Screen):
    current_money_i = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__()
        self.n_questions = len(PRIZES)

        box = BoxLayout(orientation="vertical")
        self.add_widget(box)

        PRIZES.reverse()
        self.all_prize_labels = []
        for i, prize in enumerate(PRIZES):
            print(prize, self.n_questions - i)
            prize_label = Button(text="€%s" % prize)
            prize_label.is_current = False
            if self.n_questions - i - 1 == self.current_money_i:
                color = 1,0,0,1
            else:
                color = 0,0,1,1
            prize_label.background_color = color
            self.all_prize_labels.append(prize_label)
            box.add_widget(prize_label)

    def add_one(self):
        print("add_one()")
        self.current_money_i += 1
        print("self.current_money_i: %s" % self.current_money_i)
        self.update()

    def start_over(self):
        print("start_over()")
        self.current_money_i = 0
        print("self.current_money_i: %s" % self.current_money_i)
        self.update()

    def update(self):
        for i, prize_label in enumerate(self.all_prize_labels):
            if self.n_questions - i - 1 == self.current_money_i:
                color = 1,0,0,1
            else:
                color = 0,0,1,1
            prize_label.background_color = color



class QuestionsScreen(Screen):
    question = kp.StringProperty()
    options = kp.DictProperty({
        "A": "", "B": "", "C": "", "D": ""
    })
    available_choices = kp.ListProperty(["A", "B", "C", "D"])
    current_question = 0
    option_button_disabled = kp.DictProperty({
        "A": False,
        "B": False,
        "C": False,
        "D": False
    })
    help_button_disabled = kp.DictProperty({
        "public": False,
        "phone": False,
        "skip": False,
        "50:50": False
    })
    current_button_selected = kp.StringProperty("")
    public_perc = kp.DictProperty()
    random_friends = kp.ListProperty(["", "", ""])
    chosen_friend = kp.StringProperty("")
    friend_answer = kp.StringProperty()
    pretty_solution = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__()
        self.update_question()

    def update_question(self):
        question_dict = QUESTIONS[self.current_question]
        self.question = question_dict.get("question")
        self.options = question_dict
        self.solution = question_dict.get("solution")

    def check(self, *args):
        print("check", args)
        answer = self.current_button_selected
        if answer == self.solution:
            print("correct")
            self.current_question += 1
            self.parent.money_screen.add_one()
            if self.current_question == len(QUESTIONS):
                print("YOU WIN", self.manager.current)
                self.manager.current = "game_over_screen"
                print("YOU WIN", self.manager.current)
                return
        else:
            print("incorrect")
            self.current_question = 0
            self.parent.money_screen.start_over()
            self.help_button_disabled = {
                "public": False,
                "phone": False,
                "skip": False,
                "50:50": False
            }
        self.update_question()
        print("self.option_button_disabled", self.option_button_disabled)
        self.option_button_disabled = {
            "A": False,
            "B": False,
            "C": False,
            "D": False
        }
        print("self.option_button_disabled", self.option_button_disabled)
        self.manager.current = "money_screen"
        Clock.schedule_once(self.parent.change_to_game_screen_after_some_time, TIME_TO_CHANGE_MONEY_SCREEN)

    def use_50_50(self, *args):
        print("use_50_50()", args)
        choices_to_disable = ["A", "B", "C", "D"]
        choices_to_disable.remove(self.solution)
        print("choices_to_disable", choices_to_disable)
        random.shuffle(choices_to_disable)
        choices_to_disable = choices_to_disable[0:2]
        print("choices_to_disable", choices_to_disable)
        for choice_to_disable in choices_to_disable:
            self.option_button_disabled[choice_to_disable] = True

    def skip_question(self):
        self.current_question += 1
        self.update_question()

    def help(self, help_name):
        print("self.help_button_disabled", self.help_button_disabled)
        self.help_button_disabled[help_name] = True
        print("self.help_button_disabled", self.help_button_disabled)
        if help_name == "public":
            self.public_help()
        if help_name == "phone":
            self.generate_random_friends()
        if help_name == "skip":
            self.skip_question()
        if help_name == "50:50":
            self.use_50_50()

    def public_help(self):
        print("public_help()")
        print("self.public_perc", self.public_perc)
        remaining_perc = 100
        public_perc = {}
        public_perc[self.solution] = random.randint(0, remaining_perc)
        remaining_perc -= public_perc[self.solution]
        available_choices = self.available_choices.copy()
        available_choices.remove(self.solution)
        random.shuffle(available_choices)
        while available_choices:
            option = available_choices.pop()
            public_perc[option] = random.randint(0, remaining_perc)
            remaining_perc -= public_perc[option]
        public_perc[self.solution] += remaining_perc
        self.public_perc = public_perc
        print("perc", self.public_perc)

    def generate_random_friends(self):
        friends = FRIENDS
        random.shuffle(friends)
        self.random_friends = friends[:3]

    def generate_random_friend_answer(self):
        if random.random() < PROB_OF_A_FRIEND_GETTING_IT_RIGHT:
            answer = self.solution
        else:
            print("self.available_choices.copy()", self.available_choices.copy())
            print("self.solution", self.solution)
            print("self.available_choices", self.available_choices)
            bad_answers = self.available_choices.copy()
            print("self.available_choices", self.available_choices)
            bad_answers.remove(self.solution)
            print("bad_answers", bad_answers)
            answer = random.choice(bad_answers)
        answer = QUESTIONS[self.current_question][answer]
        self.pretty_solution = "%s %s" % (random.choice(PRETTY_ANSWERS), answer)

class Game(ScreenManager):
    def change_to_game_screen(self):
        print("change_to_game_screen()")
        Clock.schedule_once(self.change_to_game_screen_after_some_time, TIME_TO_CHANGE_MONEY_SCREEN)

    def change_to_game_screen_after_some_time(self, dt):
        self.current = "questions_screen"


class GameApp(App):

    def build(self):
        self.game = Game()
        return self.game


if __name__ == "__main__":
    GameApp().run()
