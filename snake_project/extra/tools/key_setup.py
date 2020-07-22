from .os_initializer import init_os


def set_keyboard_keys() -> dict:
    key_dict = {}
    if init_os() == 'Windows':
        key_dict["UP_1"] = [119, 87]  # w W
        key_dict["DOWN_1"] = [115, 83]  # s S
        key_dict["LEFT_1"] = [97, 65]  # a A
        key_dict["RIGHT_1"] = [100, 68]  # d D

        key_dict["UP_2"] = 72  # ^
        key_dict["DOWN_2"] = 80  # v
        key_dict["LEFT_2"] = 75  # <
        key_dict["RIGHT_2"] = 77  # >
        return key_dict

    else:
        key_dict["UP_1"] = [119, 87]  # w W
        key_dict["DOWN_1"] = [115, 83]  # s S
        key_dict["LEFT_1"] = [97, 65]  # a A
        key_dict["RIGHT_1"] = [100, 68]  # d D

        key_dict["UP_2"] = 65  # ^
        key_dict["DOWN_2"] = 66  # v
        key_dict["LEFT_2"] = 68  # <
        key_dict["RIGHT_2"] = 67  # >
        return key_dict
