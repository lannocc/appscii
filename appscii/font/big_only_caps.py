# limit to codepage 437 symbols:
from . import big

matrix = big.matrix

chars = dict(filter(lambda ci: ci[0].islower(), big.chars.items()))

