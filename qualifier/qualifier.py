from enum import auto, StrEnum
import re
import warnings

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode

    def __str__(self) -> str:
        # self.quote = self._create_variant()
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if self.mode == "normal":
            return self.quote
        if self.mode == VariantMode.UWU:
            uwu_quote = self.quote.replace('r', 'w').replace('l', 'w').replace('R', 'W').replace('L', 'W')
            words = uwu_quote.split(" ")
            for i in range(len(words)):
                if words[i].startswith("u") or words[i].startswith("U"):
                    words[i] = words[i][0]+"-"+words[i][0]+words[i][1:]
            final_uwu = " ".join(words)
            if len(final_uwu) > 50:
                final_uwu = self.quote.replace('r', 'w').replace('l', 'w').replace('R', 'W').replace('L', 'W')
                warnings.warn("Quote too long, only partially transformed")
            if final_uwu == self.quote:
                raise ValueError("Quote was not modified")
            # self.quote = final_uwu
            return final_uwu

        if self.mode == VariantMode.PIGLATIN:
            # splitted = self.quote.lower().split()
            # new = [f'{word}way' if word[0] in 'aeiou' else f'{word.lstrip('bcdfghjklmnpqrstvwxyz')}{word[0:len(word)-len(word.lstrip('bcdfghjklmnpqrstvwxyz'))]}ay' for word in splitted]
            # final_pig = ' '.join(new).capitalize()

            def convert_word(word):
                vowels = "aeiouAEIOU"
                if word[0] in vowels:
                    return word + "way"
                else:
                    consonant_cluster = ""
                    for char in word:
                        if char not in vowels:
                            consonant_cluster += char
                        else:
                            break
                    return word[len(consonant_cluster):] + consonant_cluster + "ay"
            
            words = self.quote.lower().split()
            pig_latin_words = [convert_word(word) for word in words]
            final_pig = ' '.join(pig_latin_words).capitalize()
            if len(final_pig) > 50:
                raise ValueError("Quote was not modified")
            # self.quote = final_pig
            return final_pig
            
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)

def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    command_match = re.match(r'quote ((uwu|piglatin) )?("|“)([A-Za-z0-9\W_]+( [A-Za-z0-9\W_]+)*)("|”)', command)
    if command == "quote list":
        # qlist = Database.get_quotes()
        # display = ""
        # for q in qlist:
        #         display += "- " + q + "\n"
        # print(display)
        print("\n".join([f"- {q}" for q in Database.get_quotes()]))
        return None

    if command_match:
        if len(command_match.groups()[3]) > 50:
            raise ValueError("Quote is too long")
        command_quote = command_match.groups()[3]
        if command_match.groups()[1] is None:
            command_mode = VariantMode.NORMAL
        elif command_match.groups()[1] == "uwu":
            command_mode = VariantMode.UWU
        else:
            command_mode = VariantMode.PIGLATIN
        command_instance = Quote(command_quote, command_mode)
        try:
            Database.add_quote(command_instance)
        except DuplicateError:
            print("Quote has already been added previously")
        return None
        # return command_instance

    else:
        raise ValueError("Invalid command")

# user_quote = input("enter quote:")
# print(run_command(user_quote))
# print(run_command("quote list"))
# print(Database.get_quotes())


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
