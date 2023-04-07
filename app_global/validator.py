from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from .ImageProcess import Resize_Image

def check_thumbnail(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width > 260 :
        pass
        #Resize_Image(image)
        #raise ValidationError('Image width needs to be less than 260px')
    elif image_height > 320 :
        pass
        #Resize_Image(image)
        #raise ValidationError('Image height needs to be less than 320px')


def check_detailed_image(image):
    image_width, image_height = get_image_dimensions(image)
    if image_width > 2500 :
        raise ValidationError('Image width needs to be less than 2500px')
    elif image_height > 3000 :
        raise ValidationError('Image height needs to be less than 3000px')