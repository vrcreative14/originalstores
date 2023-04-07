import random

def otp_generator(no_of_digits):
    if no_of_digits == 6:
            otp = random.randint(99999, 999999)
    elif no_of_digits == 4:
            otp = random.randint(999, 9999)

    return otp


def convert_toWords(number):
        switcher={
                1:'one',
                2:'two',
                3:'three',
                4:'four',
                5:'five',
                6:'six',
                7:'seven',
                8:'eight',
                9:'nine',
                10:'ten',
                11:'eleven',
                12:'twelve',
                13:'thirteen',
                14:'fourteen',
                15:'fifteen',
                16:'sixteen',
                17:'seventeen',
                18:'eighteen',
                19:'nineteen',
                20:'twenty'
        }
        
        return switcher.get(number, "invalid")