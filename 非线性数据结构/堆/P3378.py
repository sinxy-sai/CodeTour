# 堆 / 优先队列
# 小根堆
import sys

class MinHeap:
    def __init__(self):
        self.heap = [0]

    def top(self):
        return self.heap[1]

    def push(self,x):
        self.heap.append(x)

        idx = len(self.heap) - 1

        while idx > 1:
            parent = idx //2

            if self.heap[parent] <= self.heap[idx]:
                break

            self.heap[parent],self.heap[idx] = self.heap[idx],self.heap[parent]
            idx = parent

    def pop(self):
        last = self.heap.pop()

        if (len(self.heap) == 1):
            return 
        
        self.heap[1] = last
        idx = 1

        while True:
            left = idx * 2
            right = left + 1

            smallest = idx

            if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
                smallest = left

            if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest == idx:
                break

            self.heap[idx],self.heap[smallest] = self.heap[smallest],self.heap[idx]

            idx = smallest


def main():
    n = int(sys.stdin.buffer.readline())
    heap = MinHeap()
    out = []

    for _ in range(n):
        op = sys.stdin.buffer.readline().split()

        if op[0] == b'1':
            x = int(op[1])
            heap.push(x)

        elif op[0] == b'2':
            out.append(str(heap.top()))

        elif op[0] == b'3':
            heap.pop()

    sys.stdout.write('\n'.join(out))
    
if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、优先队列是什么
#
# 普通队列是先进先出：
#
#     谁先进入队列，谁先出队
#
# 优先队列不是按进入顺序出队，
# 而是按“优先级”出队：
#
#     优先级最高的元素先出队
#
# 如果规定“数值越小，优先级越高”，
# 那么每次出队的就是当前最小值。
#
# 如果规定“数值越大，优先级越高”，
# 那么每次出队的就是当前最大值。
#
# 本题的三个操作是：
#
#     1. 插入一个数
#     2. 查询当前最小值
#     3. 删除当前最小值
#
# 所以本题本质上是在实现一个：
#
#     最小优先队列
#
#
# 二、优先队列和堆的关系
#
# 优先队列是一种抽象数据结构。
# 它规定的是“要支持什么功能”：
#
#     push   插入元素
#     top    查询优先级最高的元素
#     pop    删除优先级最高的元素
#
# 但它不规定底层必须怎么实现。
#
# 堆是一种具体的数据结构，
# 是实现优先队列最常见、最常用的方法。
#
# 也就是说：
#
#     优先队列是功能
#     堆是实现
#
# 类似于：
#
#     队列是功能
#     数组、链表、deque 都可以实现队列
#
# 优先队列也可以用多种方式实现：
#
#     1. 无序数组
#        插入 O(1)，查询/删除最值 O(n)
#
#     2. 有序数组
#        查询最值 O(1)，插入 O(n)
#
#     3. 平衡树
#        插入、删除、查询通常是 O(log n)
#
#     4. 堆
#        插入 O(log n)，删除最值 O(log n)，查询最值 O(1)
#
# 竞赛里说“优先队列”，多数时候底层就是堆。
#
#
# 三、堆是什么
#
# 堆是一种特殊的完全二叉树。
#
# 完全二叉树的意思是：
#
#     除了最后一层，其他层都是满的；
#     最后一层的节点从左到右依次排列。
#
# 小根堆满足：
#
#     每个父节点的值 <= 它的左右儿子的值
#
# 所以小根堆的根节点一定是整棵树中的最小值。
#
# 本题需要支持：
#
#     1. 插入一个数
#     2. 查询当前最小值
#     3. 删除当前最小值
#
# 因此正好适合使用小根堆。
#
#
# 四、为什么可以用数组存堆
#
# 因为堆是一棵完全二叉树。
# 完全二叉树可以很方便地用数组表示。
#
# 本程序中：
#
#     self.heap = [0]
#
# 第 0 个位置不用，真实元素从下标 1 开始。
# 这样父子关系非常清楚：
#
#     当前节点 idx
#     父节点 parent = idx // 2
#     左儿子 left = idx * 2
#     右儿子 right = idx * 2 + 1
#
# 例如数组：
#
#     下标： 1  2  3  4  5
#     值：   1  3  2  7  5
#
# 对应的树是：
#
#             1
#           /   \
#          3     2
#         / \
#        7   5
#
# 堆顶就是：
#
#     heap[1]
#
#
# 五、top()
#
# 小根堆的最小值永远在堆顶，
# 所以查询最小值只需要：
#
#     return self.heap[1]
#
# 时间复杂度是 O(1)。
#
#
# 六、push(x)：插入元素
#
# 插入新元素时，先把它放到数组最后：
#
#     self.heap.append(x)
#
# 这样可以保证完全二叉树的形状不被破坏。
#
# 但是新元素可能比父节点更小，
# 会破坏小根堆性质。
#
# 所以需要让它不断向上调整，叫“上浮”。
#
# 当前节点下标是 idx：
#
#     parent = idx // 2
#
# 如果：
#
#     heap[parent] <= heap[idx]
#
# 说明父节点已经不大于当前节点，
# 小根堆性质满足，停止上浮。
#
# 如果：
#
#     heap[parent] > heap[idx]
#
# 说明父节点比当前节点大，
# 要交换它们：
#
#     heap[parent], heap[idx] = heap[idx], heap[parent]
#
# 然后继续从 parent 位置往上检查。
#
# 例子：
#
# 原堆：
#
#             2
#           /   \
#          5     4
#
# 插入 1，先放到最后：
#
#             2
#           /   \
#          5     4
#         /
#        1
#
# 1 比父节点 5 小，交换：
#
#             2
#           /   \
#          1     4
#         /
#        5
#
# 1 又比父节点 2 小，继续交换：
#
#             1
#           /   \
#          2     4
#         /
#        5
#
# 此时小根堆恢复。
#
#
# 七、pop()：删除最小值
#
# 小根堆的最小值在 heap[1]。
# 删除堆顶时，不能直接删除数组中间的 heap[1]，
# 否则完全二叉树的结构会乱。
#
# 常见做法是：
#
#     1. 取出最后一个元素 last
#     2. 把 last 放到堆顶 heap[1]
#     3. 让 heap[1] 不断向下调整
#
# 代码：
#
#     last = self.heap.pop()
#
# 先删除并取出数组最后一个元素。
#
# 如果 pop 之后只剩下占位的 0：
#
#     if len(self.heap) == 1:
#         return
#
# 说明原来堆里只有一个真实元素，
# 删除后堆已经空了，不需要继续调整。
#
# 否则把最后一个元素放到堆顶：
#
#     self.heap[1] = last
#
# 这时完全二叉树的形状是对的，
# 但小根堆性质可能被破坏。
#
# 所以从 idx = 1 开始下沉。
#
# 每次比较当前节点、左儿子、右儿子，
# 找到三者中最小的位置：
#
#     smallest = idx
#
#     if left 存在且 heap[left] < heap[smallest]:
#         smallest = left
#
#     if right 存在且 heap[right] < heap[smallest]:
#         smallest = right
#
# 如果 smallest 还是 idx，
# 说明当前节点已经比两个孩子都小，
# 小根堆性质满足，可以停止。
#
# 如果 smallest 不是 idx，
# 说明某个孩子更小，
# 当前节点要和更小的孩子交换：
#
#     heap[idx], heap[smallest] = heap[smallest], heap[idx]
#
# 然后 idx 移动到 smallest，
# 继续向下检查。
#
# 例子：
#
# 原堆：
#
#             1
#           /   \
#          3     2
#         / \
#        7   5
#
# 删除堆顶 1。
# 先取最后一个元素 5 放到堆顶：
#
#             5
#           /   \
#          3     2
#         /
#        7
#
# 5 比左右儿子都大，其中右儿子 2 最小，
# 交换 5 和 2：
#
#             2
#           /   \
#          3     5
#         /
#        7
#
# 此时 5 没有孩子了，调整结束。
#
#
# 八、为什么插入和删除是 O(log n)
#
# 堆是一棵完全二叉树。
# 如果堆里有 n 个元素，树高大约是：
#
#     log2(n)
#
# push 时，一个元素最多从最后一层一路上浮到根。
# pop 时，一个元素最多从根一路下沉到最后一层。
#
# 所以：
#
#     push: O(log n)
#     pop:  O(log n)
#     top:  O(1)
#
# 本题一共有 n 次操作，
# 最坏情况下每次都是插入或删除，
# 总时间复杂度是：
#
#     O(n log n)
#
#
# 九、空间复杂度
#
# 堆里最多保存 n 个数，
# 输出数组 out 最多也可能保存 O(n) 个答案。
#
# 所以整体空间复杂度是：
#
#     O(n)
#
#
# 十、细节提醒
#
# 1. 为什么 heap = [0]
#
#    这是为了让真实节点从下标 1 开始。
#    这样父子关系更简单：
#
#        parent = idx // 2
#        left = idx * 2
#        right = idx * 2 + 1
#
# 2. 为什么 pop 时用最后一个元素补堆顶
#
#    因为堆必须保持完全二叉树形状。
#    删除最后一个节点不会破坏完全二叉树结构，
#    把最后一个节点放到根，再下沉调整即可。
#
# 3. 为什么小根堆能处理重复元素
#
#    堆只要求父节点 <= 子节点。
#    如果有多个相同的最小值，
#    heap[1] 是其中一个。
#    pop 删除其中一个即可，符合题意。
