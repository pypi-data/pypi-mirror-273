from enum import auto
from omniblack.utils import Enum
from public import public

try:
    from regex import compile
    unicode_re = True
except ImportError:
    from re import compile
    unicode_re = False

if unicode_re:
    word_pattern = compile(
        r'[\. \-_]+|'
        r'(?<=\p{Lowercase=true})(?=\p{Uppercase=true})',
    )
else:
    word_pattern = compile(r'[\. \-_]+|(?<=[a-z])(?=[A-Z])')

public(word_pattern=word_pattern)


@public
def words(string):
    yield from word_pattern.split(string)


@public
class Cases(Enum):
    Camel = auto(), 'Camel'
    CapKebab = auto(), 'CapKebab'
    CapSnake = auto(), 'CapSnake'
    Kebab = auto(), 'Kebab'
    Pascal = auto(), 'Pascal'
    Snake = auto(), 'Snake'
    Title = auto(), 'Title'

    Cobol = CapKebab

    def __init__(self, value, name):
        self.cap_boundary = name in {'Camel', 'Pascal', 'Title'}
        self.cap_first = name in {'Pascal', 'Title'}
        self.cap_all = name in {'CapSnake', 'CapKebab'}

        match name:
            case 'Snake' | 'CapSnake':
                self.seperator = '_'
            case 'Kebab' | 'CapKebab':
                self.seperator = '-'
            case 'Title':
                self.seperator = ' '
            case 'Pascal' | 'Camel':
                self.seperator = ''

    def handle_word(self, word, first):
        if (self.cap_boundary and not first) or self.cap_first:
            return word.title()
        elif self.cap_all:
            return word.upper()
        else:
            return word.lower()

    def to(self, string):
        words = [
            self.handle_word(word, index == 0)
            for index, word in enumerate(words(string))
        ]

        return self.seperator.join(words)
