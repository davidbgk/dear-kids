"""
From @simonw https://www.djangosnippets.org/snippets/1431/

Convert numbers from base 10 integers to base X strings and back again.

Sample usage:

>>> base20 = BaseConverter('0123456789abcdefghij')
>>> base20.from_decimal(1234)
'31e'
>>> base20.to_decimal('31e')
1234
"""
from typing import Union


class BaseConverter:
    decimal_digits = "0123456789"

    def __init__(self, digits: str) -> None:
        self.digits = digits

    def from_decimal(self, i: int) -> str:
        return self.convert(i, self.decimal_digits, self.digits)

    def to_decimal(self, s: str) -> int:
        return int(self.convert(s, self.digits, self.decimal_digits))

    @staticmethod
    def convert(number: Union[str, int], fromdigits: str, todigits: str) -> str:
        # Based on http://code.activestate.com/recipes/111286/
        if str(number)[0] == "-":
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0

        # make an integer out of the number
        x = 0
        for num in str(number):
            x = x * len(fromdigits) + fromdigits.index(num)

        # create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ""
            while x > 0:
                digit: int = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))
            if neg:
                res = "-" + res
        return res


bin = BaseConverter("01")
hexconv = BaseConverter("0123456789ABCDEF")
base57 = BaseConverter("ABCDEFGHIJKLMNPQRSTUVWXYZ23456789abcdefghijkmnpqrstuvwxyz")
base62 = BaseConverter("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz")
