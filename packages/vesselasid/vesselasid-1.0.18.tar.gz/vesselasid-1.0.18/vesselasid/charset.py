import copy
import scipy as sp
import numpy as np


class Charset:
    def __init__(self, charset):
        self.charset = charset

    def right_roll(self, fromchars, tochars, roll):
        new_charset = copy.deepcopy(self.charset)
        for line in range(8):
            orig_line_bits = np.unpackbits(
                np.array(
                    [self.charset[x * 8 + line :][:1] for x in fromchars],
                    dtype=np.uint8,
                )
            )
            new_line_bits = np.packbits(
                np.concatenate([orig_line_bits[-1:], np.roll(orig_line_bits, roll)[1:]])
            )
            for y, x in enumerate(tochars):
                new_charset[x * 8 + line] = new_line_bits[y]
        self.charset = new_charset

    def down_roll(self, fromchars, tochars, roll):
        chars_column = np.concatenate(
            [self.charset[x * 8 : x * 8 + 8] for x in fromchars]
        )
        chars_column = np.concatenate(
            [chars_column[-roll:], np.roll(chars_column, roll)[roll:]]
        )
        for y, x in enumerate(tochars):
            self.charset[x * 8 : x * 8 + 8] = chars_column[y * 8 : y * 8 + 8]

    def rotate_square(self, fromchars, tochars, degrees):
        sqrt = int(np.sqrt(len(fromchars)))
        chars_square = np.reshape(
            np.unpackbits(
                np.concatenate([self.charset[x * 8 : x * 8 + 8] for x in fromchars])
            ),
            (len(fromchars) * 8, 8),
        )
        chars_square = np.concatenate(
            [
                chars_square[i * sqrt * 8 : (i * sqrt * 8) + (sqrt * 8), 0:8]
                for i in range(sqrt)
            ],
            axis=1,
        )
        chars_square = sp.ndimage.rotate(chars_square, degrees, reshape=True)
        for y in range(sqrt):
            for x in range(sqrt):
                c = tochars[y * sqrt + x]
                self.charset[c * 8 : c * 8 + 8] = np.packbits(
                    chars_square[x * 8 : x * 8 + 8, y * 8 : y * 8 + 8]
                )
