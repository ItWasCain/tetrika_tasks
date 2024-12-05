def strict(func):
    def wrapper(*args):
        annotations = list(func.__annotations__.values())

        check_args = True
        for arg_id in range(len([*args])):
            if type([*args][arg_id]) is not annotations[arg_id]:
                check_args = False
        if check_args:
            return func(*args)
        raise TypeError
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


# print(sum_two(1, 2))  # >>> 3
# print(sum_two(1, 2.4))  # >>> TypeError
