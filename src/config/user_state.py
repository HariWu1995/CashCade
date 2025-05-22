from .exp import INDATED

if INDATED:
    LIFETIME = 86400  # 1 day to live
    LIFESPEED = 100
    MOVEMENT = 5
    STRENGTH = 20
    PROPERTY = 0

else:
    LIFETIME = 100
    LIFESPEED = 100
    MOVEMENT = 5
    STRENGTH = 0
    PROPERTY = 0

