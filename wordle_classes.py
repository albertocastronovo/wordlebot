from discord.ui import Button
from random import randrange
from discord import ButtonStyle as Bs
from discord.ui import View


class WordleBoard:
    def __init__(self, word_length: int = 5, attempts: int = 6):
        self.__length = word_length
        self.__attempt = 0
        self.__board = [
            [
                Button(
                    style=Bs.gray,
                    label=u"\u200B"
                ) for _ in range(word_length)
            ] for _ in range(attempts-1)
        ]

    @property
    def board(self):
        return self.__board

    @property
    def length(self):
        return self.__length

    @property
    def attempt(self):
        return self.__attempt

    def inc_attempt(self):
        self.__attempt += 1

    def set_board_line(self, new_line: list[Button]):
        self.__board[self.__attempt - 1] = new_line

    def get_board_view(self):
        new_view = View()
        for line in self.__board:
            for button in line:
                new_view.add_item(button)
        return new_view


class Game:
    def __init__(self, language: str = "ita", length: int = 5, word: str | None = None, attempts: int = 6):
        self.__board: WordleBoard = WordleBoard(word_length=length, attempts=attempts)
        if word is None:
            self.__word = self.random_word_from_file(language=language, length=length).lower()
        else:
            self.__word = word
        self.__length = length
        self.__max_attempts = attempts

    @staticmethod
    def random_word_from_file(language: str = "ita", length: int = 5) -> str:
        filename = f"words/{language}_{length}_less.txt"
        with open(filename, "r") as f:
            line = next(f)
            for i, new_line in enumerate(f, start=2):
                if randrange(i) == 0:
                    line = new_line
        return line[:-1]

    def guess_word(self, guessed_word: str = "lezzo"):

        guessed_word = guessed_word.lower()
        original_list = [x for x in self.__word]
        guessed_index = list(range(len(guessed_word)))
        guessed_list = [x for x in guessed_word]
        color_list = []
        # check for all right letters in the right place
        for i in range(len(original_list)-1, -1, -1):
            if guessed_list[i] == original_list[i]:
                del original_list[i]
                del guessed_list[i]
                del guessed_index[i]
                color_list.append(Bs.green)
            else:
                color_list.append(None)
        color_list.reverse()
        # check for all right letters in the wrong place
        for i in range(len(original_list)-1, -1, -1):
            if guessed_list[i] in original_list:
                try:
                    index_o = original_list.index(guessed_list[i])
                    color_list[guessed_index[i]] = Bs.blurple
                    del original_list[index_o]
                except ValueError:
                    continue
        color_list[:] = [c if c is not None else Bs.gray for c in color_list]
        self.__board.inc_attempt()
        no_green = color_list.count(Bs.green)

        if no_green < self.__length and self.__board.attempt >= self.__max_attempts:    # EOG fail
            content = f"You couldn't guess the word right! :( The word was '{self.__word.upper()}'"
            return -1, View(), content
        elif no_green == self.__length and self.__board.attempt < self.__max_attempts:  # EOG success
            content = "Congratulations! You guessed right!"
            return 1, View(), content

        button_list = [Button(style=color_list[i],
                              label=guessed_word[i].upper(),
                              emoji=None,
                              row=self.__board.attempt - 1
                              )
                       for i in range(len(guessed_word))]
        if self.__board.attempt < self.__max_attempts:
            self.__board.set_board_line(button_list)
        content = "Keep guessing!"
        return 0, self.__board.get_board_view(), content



