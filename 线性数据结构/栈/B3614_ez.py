import sys

def main():
    T = int(sys.stdin.readline())

    for _ in range(T):
        n = int(sys.stdin.readline())
        stack = []
        for __ in range(n):
            op = sys.stdin.readline().strip().split()

            if op[0] == 'push':
                stack.append(int(op[1]))

            elif op[0] == 'pop':
                if not stack:
                    print('Empty')
                else:
                    stack.pop()

            elif op[0] == 'query':
                if not stack:
                    print('Anguei!')
                else:
                    print(stack[-1])

            elif op[0] == 'size':
                print(len(stack))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 这题要求实现一个栈。
# 栈的核心特点是“后进先出”，也就是最后 push 进去的元素，
# 会最先被 query 查到，也会最先被 pop 弹出。
#
# Python 中可以用 list 模拟栈：
#
#     stack = []
#     stack.append(x)   # push，把 x 加到栈顶
#     stack.pop()       # pop，删除栈顶
#     stack[-1]         # query，查看栈顶
#     len(stack)        # size，查看元素个数
#
# 为什么 list 可以当栈：
# Python 的 list 底层更接近“动态数组”，不是链表。
# 它既可以像数组一样用下标 O(1) 访问元素，也可以在末尾高效加入和删除元素。
# 当我们只在末尾 append 和 pop 时，list 就能很好地模拟栈。
#
# list 和数组的关系：
# 数组支持通过下标快速访问，例如 stack[i]。
# Python 的 list 也支持这种访问，所以它有数组的特点。
# 但 list 的长度可以动态变化，所以更准确地说，它像“动态数组”。
#
# list 和栈的关系：
# 栈是一种操作受限制的数据结构，只关心栈顶。
# 如果只使用 list 的 append、pop、[-1]，那么这个 list 就表现得像一个栈。
#
# 需要注意：
#     stack.pop()
# 是从末尾删除，复杂度是 O(1)。
#     stack.pop(0)
# 是从开头删除，会导致后面的元素整体前移，复杂度是 O(N)，不适合用来模拟队列。
#
# 关于 'pop' 和 b'pop'：
# 本程序使用的是：
#
#     sys.stdin.readline()
#
# 它读入的是普通字符串 str，所以 split 后得到的是：
#
#     ['pop']
#
# 因此判断时写：
#
#     op[0] == 'pop'
#
# 如果使用更快的二进制读入：
#
#     sys.stdin.buffer.readline()
#
# 它读入的是 bytes，split 后得到的是：
#
#     [b'pop']
#
# 这时判断就要写：
#
#     op[0] == b'pop'
#
# 'pop' 是 str，b'pop' 是 bytes，二者类型不同，不能直接混用。
#
# 为什么有时使用 sys.stdin.buffer.readline：
# 数据量很大时，二进制读入通常更快。
# 但它读出来的是 bytes，所以命令字符串要和 b'push'、b'pop'、b'query'、b'size' 比较。
#
# 本 ez 版本为了容易理解，使用普通字符串读入。
