def is_integer(string):
    try:
        value = int(string)
        return value == float(string)
    except ValueError:
        return False


def check_dice_format(dice):
    try:
        if dice[0] == "1" and dice[1] == "d":
            dice = dice[2:]  # Retrieves "number" from message
            if not is_integer(dice): return False  # Checks if "number" is integer
            dice = int(dice)  # Converts dice var to integer
            if dice < 1: return False  # Tests if dice var is at least 1
            return True  # Good input
        else:
            return False
    except Exception:
        return False


def check_range_format(range_input):
    for num in range_input:
        if not is_integer(num):
            return False
    return True