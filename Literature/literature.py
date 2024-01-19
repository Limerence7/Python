import random
import re
import time

info = []
num2filename = ["机考出题", "出题-王立君", "文件检索计算机考试"]
question_type = ['单选题', '多选题', '判断题', '任意题型']
range_of_que = []
last_order = 0
last_index = 0
my_shuffle_list = []


def extract_number(s):
    match = re.match(r'\d+', s)
    if match:
        return int(match.group())
    else:
        return None


def storage_lite(file_name):
    file_suffix = ".txt"
    file_path = file_name + file_suffix

    select_pattern = re.compile(r"[(（].*[A-Z]+.*[）)]")
    check_pattern = re.compile(r"[(（].*[√xX×]+.*[）)]")
    options_pattern = re.compile(r"[A-Z][、.．]")
    with open(file_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        typ = "单选题"
        all_len = len(lines)
        range_record = [0]
        idx = 0
        while idx < all_len:
            current = {}
            line = lines[idx]
            if line in ["判断题", "多选题"]:
                range_record.append(len(info) - 1)
                range_of_que.append(range_record)
                range_record = [len(info)]
                typ = line
                idx += 1
                continue
            ret = extract_number(line)
            if ret is None:
                idx += 1
                continue
            current["No"] = ret
            current["type"] = typ
            if current["type"] != "判断题":
                matches = select_pattern.search(line)
                current["question"] = line.replace(matches.group(), "( )")
                current["answer"] = ""
                for st in matches.group():
                    if st.isupper():
                        current["answer"] += st + " "
                idx += 1
                offered = []
                while idx < all_len and lines[idx] and (lines[idx][0].isupper() or lines[idx][0] == '①'):
                    offered.append(lines[idx])
                    idx += 1

                # make options more good-looking
                opts = []
                sum_options = ""
                for item in offered:
                    if item[0].isupper():
                        sum_options += item.replace(' ', '')
                    else:
                        opts.append(item)
                matches = options_pattern.finditer(sum_options)
                pos_list = [(match.start(), match.end()) for match in matches]
                pos_list.append((len(sum_options), 0))
                pos_list = [(pos_list[i][1], pos_list[i+1][0]) for i in range(len(pos_list) - 1)]
                for i in range(len(pos_list)):
                    ans = chr(ord('A') + i) + '.' + sum_options[pos_list[i][0]:pos_list[i][1]]
                    opts.append(ans)
                current["options"] = opts


            else:
                matches = check_pattern.search(line)
                current["question"] = line.replace(matches.group(), "( )")
                current["answer"] = ""
                current["options"] = []
                for st in matches.group():
                    if st in ['√', 'x', 'X', '×']:
                        current["answer"] = st
                idx += 1
            info.append(current)
        range_record.append(len(info) - 1)
        range_of_que.append(range_record)

        range_of_que.append([0, len(info) - 1])


def question_begin(que_type, order):
    global last_index
    global last_order
    global my_shuffle_list

    left = range_of_que[que_type][0]
    right = range_of_que[que_type][1]
    if order == 1 and last_order == 0:
        my_shuffle_list = random.sample(info[left:right+1], len(info[left:right+1]))
        last_index = 0
    ready = {}
    if order:
        ready = my_shuffle_list[last_index]
        print("顺序", "{} / {}".format(last_index + 1, right - left + 1), end='  ')
        last_index = (last_index + 1) % (right - left + 1)
    else:
        # 使用当前时间作为随机种子
        seed_value = int(time.time())
        random.seed(seed_value)
        # 生成随机数
        random_number = random.randint(left, right)
        ready = info[random_number]
        print("随机", end='  ')

    print(ready["type"])
    print(ready["question"])
    if ready["options"]:
        for item in ready["options"]:
            print(item)
    nonsense = input("👻输入回车显示答案👻")
    print(ready["answer"])
    print("👻下一题或者改变题型👻")
    last_order = order


print("请输入需要的word文档对应的编号：(1.机考出题  2.出题-王立君  3.文件检索计算机考试)")
No_file = int(input())
file_name = num2filename[No_file - 1]
storage_lite(file_name)

que_type = 3
if_order = 0
print("将根据你的输入选择不同的文件，测试你的背诵程度，当前默认为任意题型，输入0表示单选，1表示多选，2表示判断，4表示当前模式的顺序模式，q表示停止，其余都表示为任意题型")
print("输入回车则和表示不变，题型还是和上一次一样")
print()
op = input()
while op != 'q':
    if op == '':
        que_type = que_type
        if_order = if_order
    else:
        op_num = extract_number(op)
        if op_num is None:
            que_type = 3
            if_order = 0
        elif op_num == 4:
            if_order = 1
        elif 3 <= op_num < 0:
            que_type = 3
            if_order = 0
        else:
            que_type = op_num
            if_order = 0
    question_begin(que_type, if_order)
    op = input()
