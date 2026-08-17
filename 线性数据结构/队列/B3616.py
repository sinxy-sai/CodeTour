# 手写队列
import sys

class Queue:
    def __init__(self,capacity):
        self.queue = [0]*capacity
        self.head = 0
        self.tail = 0

    def push(self,x):
        self.queue[self.tail] = x
        self.tail += 1

    def pop(self):
        if self.head == self.tail:
            return False
        self.head += 1
        return True

    def size(self):
        return self.tail - self.head

    def query(self):
        if self.head == self.tail:
            return None
        return self.queue[self.head]


def main():
    n = int(sys.stdin.buffer.readline())

    queue = Queue(n)
    out = []

    for _ in range(n):
        op = sys.stdin.buffer.readline().strip().split()

        if op[0] == b'1':
            queue.push(int(op[1]))

        elif op[0] == b'2':
            if not queue.pop():
                out.append('ERR_CANNOT_POP')

        elif op[0] == b'3':
            value = queue.query()
            if value is None:
                out.append('ERR_CANNOT_QUERY')
            else:
                out.append(str(value))
            
        elif op[0] == b'4':
            out.append(str(queue.size()))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 这题要求实现一个队列。
# 队列的特点是“先进先出”，也就是先 push 进去的元素，
# 会最先被 query 查到，也会最先被 pop 弹出。
#
# 本程序使用“数组 + head/tail 指针”手写队列。
#
# 队列的存储：
#
#     self.queue = [0] * capacity
#     self.head = 0
#     self.tail = 0
#
# queue 是提前开好的数组。
# head 指向当前队首元素的位置。
# tail 指向下一个应该插入的位置。
#
# 队列为空的条件：
#
#     head == tail
#
# 当前队列大小：
#
#     tail - head
#
# push(x)：
#
#     queue[tail] = x
#     tail += 1
#
# 把元素放到队尾，然后 tail 后移。
#
# pop()：
#
#     如果 head == tail，说明队列为空，返回 False。
#     否则 head += 1，表示弹出队首，返回 True。
#
# 这里不需要真的删除 queue[head]。
# 因为 head 已经向后移动，原来的位置就不再属于当前队列。
#
# query()：
#
#     如果 head == tail，说明队列为空，返回 None。
#     否则返回 queue[head]，也就是当前队首。
#
# size()：
#
#     直接返回 tail - head。
#
# 为什么容量开 n：
# 总共只有 n 次操作，即使所有操作都是 push，队列里最多也只有 n 个元素。
# 所以 Queue(n) 足够。
#
# 输入输出细节：
#
# 数据量虽然不如一些大模板题夸张，但使用 buffer 读入更稳：
#
#     sys.stdin.buffer.readline()
#
# buffer 读入得到的是 bytes，所以操作编号判断写成：
#
#     b'1'
#     b'2'
#     b'3'
#     b'4'
#
# 输出时不频繁 print，而是先存入 out：
#
#     out.append(...)
#
# 最后统一输出：
#
#     sys.stdout.write('\n'.join(out))
#
# 这样可以减少 I/O 次数。
#
# 和栈的区别：
#
# 栈只需要一个 top 指针，操作都发生在同一端。
# 队列需要 head 和 tail 两个指针，一端入队，一端出队。
