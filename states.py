from aiogram.utils.helper import Helper, HelperMode, ListItem


class RegisterStates(Helper):
    mode = HelperMode.snake_case

    FULL_NAME = ListItem()
    DATEBIRTH = ListItem()
    PLACEOFRESIDENCE = ListItem()
    PHONENUM = ListItem()
    PASSSERIES = ListItem()
    PASSNUM = ListItem()
    PASSDATEOFISSUE = ListItem()
    PASSISSUEDBY = ListItem()
    REGISTRADDR = ListItem()
    EMAIL = ListItem()
    MAJOR = ListItem()
    REGISTERED = ListItem()
