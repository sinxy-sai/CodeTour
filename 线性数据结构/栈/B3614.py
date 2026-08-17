# 手写栈
import sys

class Stack:
    def __init__(self,capacity):
        self.stack = [0] * capacity
        self.top = 0

    def push(self,x):
        self.stack[self.top] = x
        self.top += 1

    def pop(self):
        if self.top == 0:
            return False
        self.top -= 1
        return True

    def size(self):
        return self.top

    def query(self):
        if self.top == 0:
            return None
        return self.stack[self.top-1]

def main():
    T = int(sys.stdin.buffer.readline())

    out = []
    for _ in range(T):
        n = int(sys.stdin.buffer.readline())
        stack = Stack(n)

        for __ in range(n):
            op = sys.stdin.buffer.readline().strip().split()

            if op[0] == b'push':
                stack.push(int(op[1]))

            elif op[0] == b'pop':
                if not stack.pop():
                    out.append('Empty')

            elif op[0] == b'query':
                value = stack.query()
                if value is None:
                    out.append('Anguei!')
                else:
                    out.append(str(value))

            elif op[0] == b'size':
                out.append(str(stack.size()))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 这题要求实现一个栈。
# 栈的特点是“后进先出”，最后 push 进去的元素，会最先被 query 查到，
# 也会最先被 pop 弹出。
#
# 本程序没有直接使用 list 的 append/pop 来模拟栈，
# 而是用“数组 + top 指针”的方式手写栈，更接近栈的底层实现。
#
# 栈的存储：
#
#     self.stack = [0] * capacity
#     self.top = 0
#
# stack 是提前开好的数组。
# top 表示当前栈内元素个数，也表示下一个元素应该插入的位置。
# 如果 top == 0，说明栈为空。
# 如果 top > 0，栈顶元素在 stack[top - 1]。
#
# push(x)：
#
#     stack[top] = x
#     top += 1
#
# 把新元素放到 top 指向的位置，然后 top 后移。
#
# pop()：
#
#     如果 top == 0，说明栈为空，返回 False。
#     否则 top -= 1，表示删除栈顶，返回 True。
#
# 这里不需要真的清空 stack[top - 1]。
# 因为 top 已经变小了，top 之后的位置会被视为不属于当前栈。
#
# query()：
#
#     如果 top == 0，返回 None。
#     否则返回 stack[top - 1]。
#
# size()：
#
#     直接返回 top。
#
# 为什么数组容量开 n：
# 每组数据最多只有 n 次操作。
# 即使所有操作都是 push，栈内最多也只有 n 个元素。
# 所以 Stack(n) 足够，不需要开更大的数组。
#
# 输入细节：
#
# 数据量较大，使用：
#
#     sys.stdin.buffer.readline()
#
# 它比普通 input() 更快。
# 但 buffer 读入的是 bytes，所以命令判断要写：
#
#     b'push'
#     b'pop'
#     b'query'
#     b'size'
#
# 如果使用 sys.stdin.readline()，读入的是 str，才写 'push'、'pop'。
#
# 输出细节：
#
# 数据量大时，频繁 print 会比较慢。
# 所以本程序用 out 列表收集所有输出：
#
#     out.append(...)
#
# 最后统一输出：
#
#     sys.stdout.write('\n'.join(out))
#
# 这样可以减少大量 I/O 调用，避免最后一个测试点 TLE。
