import random

KAOMOJI_LIST = [
    '( ͡° ͜ʖ ͡°)',
    '¯\_(ツ)_/¯',
    '༼ つ ◕_◕ ༽つ',
    '(╯°□°)╯︵ ┻━┻',
    '┬─┬ノ( º _ ºノ)',
    '(ง •̀_•́)ง',
    '(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧',
    '(╥_╥)',
    'ᕕ( ᐛ )ᕗ',
]

def get_random_kaomoji():
    return random.choice(KAOMOJI_LIST)