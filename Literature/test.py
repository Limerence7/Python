import os
import re

s = "(C)23234 2nnd ssd"
ret = re.match(r"[(（][A-Z]+[）)]", s)
print(ret)
i = 0
