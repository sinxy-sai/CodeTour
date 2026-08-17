# 双端队列

import sys
from collections import deque, defaultdict

def main():
    q = int(sys.stdin.buffer.readline())

    deques = defaultdict(deque)
    out = []

    for _ in range(q):
        op = sys.stdin.buffer.readline().split()
        cmd = op[0]
        a = int(op[1])
        dq = deques[a]

        if cmd == b'push_back':
            x = int(op[2])
            dq.append(x)

        elif cmd == b'pop_back':
            if dq:
                dq.pop()

        elif cmd == b'push_front':
            x = int(op[2])
            dq.appendleft(x)

        elif cmd == b'pop_front':
            if dq:
                dq.popleft()

        elif cmd == b'size':
            out.append(str(len(dq)))

        elif cmd == b'front':
            if dq:
                out.append(str(dq[0]))

        elif cmd == b'back':
            if dq:
                out.append(str(dq[-1]))

    sys.stdout.write('\n'.join(out))
    
if __name__ == '__main__':
    main()


# 思路说明：
#
# 这题要同时维护很多个双端队列，第 a 个队列支持：
#
#     push_back    队尾插入
#     pop_back     队尾弹出
#     push_front   队首插入
#     pop_front    队首弹出
#     size         查询大小
#     front        查询队首
#     back         查询队尾
#
# Python 里可以直接使用 collections.deque。
# deque 是“双端队列”，两头操作都是 O(1)：
#
#     dq.append(x)       在队尾插入 x
#     dq.appendleft(x)   在队首插入 x
#     dq.pop()           弹出队尾
#     dq.popleft()       弹出队首
#     dq[0]              队首元素
#     dq[-1]             队尾元素
#     len(dq)            队列大小
#
# 本程序是一个方便理解的 ez 版本。
# 它使用 defaultdict(deque) 保存所有出现过的队列编号。
# 每次读入操作后，先通过：
#
#     dq = deques[a]
#
# 找到第 a 个双端队列，然后再对 dq 做对应操作。
#
#
# 关于 defaultdict(deque)：
#
# defaultdict 是“带默认生成函数的字典”。
# 普通 dict 访问不存在的 key 会报 KeyError：
#
#     d = {}
#     d[5].append(10)   # 错误，d[5] 不存在
#
# 如果写成：
#
#     from collections import defaultdict, deque
#     d = defaultdict(deque)
#     d[5].append(10)
#
# 那么第一次访问 d[5] 时，Python 会自动执行 deque()，
# 创建一个新的空双端队列：
#
#     d[5] = deque()
#
# 所以 defaultdict(deque) 的默认值可以理解成“新的空队列”。
#
# 但 defaultdict(10) 是错误的。
# defaultdict 里面要放“函数”，不能直接放具体值。
#
# 常见写法：
#
#     defaultdict(int)          默认 int() -> 0
#     defaultdict(str)          默认 str() -> ''
#     defaultdict(list)         默认 list() -> []
#     defaultdict(set)          默认 set() -> set()
#     defaultdict(deque)        默认 deque() -> 空双端队列
#     defaultdict(lambda: 10)   默认 10
#
# 也就是说，如果想让默认值是 10，要写：
#
#     defaultdict(lambda: 10)
#
#
# 为什么这个 ez 版本可能 MLE：
#
# 如果每次操作开头都写：
#
#     dq = deques[a]
#
# 那么 pop、front、back、size 这些操作也会创建空队列。
# 例如：
#
#     pop_back 999999
#     front 888888
#
# 这些队列本来是空的，不需要真的创建。
# 但 defaultdict(deque) 会因为访问 deques[a] 而自动生成空 deque。
#
# 当测试数据里有很多不同编号的空操作时，
# 就可能创建大量没用的空队列，从而 MLE。
#
# 所以这个程序适合理解 deque 的基本用法，
# 但不一定能通过本题所有测试点。
# 想过极限数据，需要用更省内存的写法，例如数组模拟多双端队列。
