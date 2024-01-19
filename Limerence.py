import math

import unicodedata


def find_sequence_by_index(index, n, k):
    result = []

    for i in range(n, 0, -1):
        current_combinations = math.comb(i, k)

        if index > current_combinations:
            index -= current_combinations
        else:
            result.append(i)
            k -= 1
        print(result)

    return result[::-1]


def fullwidth_to_halfwidth(input_str):
    result_str = ""
    for char in input_str:
        # 判断字符是否是全角字符
        if unicodedata.east_asian_width(char) == 'F':
            # 获取半角字符的 Unicode 编码
            halfwidth_char = unicodedata.normalize('NFKC', char)
            result_str += halfwidth_char
        else:
            result_str += char
    return result_str


# 示例
index = 6
n = 4
k = 2
s = input()
f = open('easy.txt', 'w', encoding='utf-8')
f.write(fullwidth_to_halfwidth(s.replace(' ', '')))
