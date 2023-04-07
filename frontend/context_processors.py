
from products.models import ProductCategory


def base(request):
    #user_name = request.session['user_name']
    categories = ProductCategory.objects.all()
    categories_div_class = "ui " + convert_toWords(len(categories)) + " item menu"
    return {'product_categories': categories,'user_name': 'Daya','categories_div_class':categories_div_class }


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
        
        return switcher.get(number, "Invalid month")