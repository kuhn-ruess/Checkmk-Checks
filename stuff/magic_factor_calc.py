#!/usr/bin/env python3

filesystem_size = int(input("Input Filesystem Size in GB: ").strip())
referenze_size = int(input("Input reference Size in GB default 20: ").strip() or 20)
factor = float(input("Input Magic Factor: "))
level = int(input("Input basic level default 90: ") or 90)


def adjust_level(level, factor):
    """
    """
    return 100 - ((100  - level) * factor)


def adjust_levels(level, factor, filesystem_size, referenze_size):
    """
    """

    relative_size = filesystem_size / referenze_size
    true_factor = (relative_size**factor) / relative_size

    return adjust_level(level, true_factor)



new_level = adjust_levels(level, factor, filesystem_size, referenze_size)


print(f'New Level is {new_level}')
