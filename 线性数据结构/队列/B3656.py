# 双端队列

import sys
from array import array

MAX_A = int(1e6)

class MultiDeque:
    def __init__(self,max_a):
        self.head = array('i',[0]) *(max_a+1)
        self.tail = array('i',[0]) *(max_a+1)
        self.size = array('i',[0]) *(max_a+1)

        self.val = array('q',[0])
        self.pre = array('i',[0])
        self.nxt = array('i',[0])

    def new_node(self,x):
        idx = len(self.val)
        self.val.append(x)
        self.pre.append(0)
        self.nxt.append(0)
        return idx

    def push_back(self,a,x):
        idx = self.new_node(x)
        old_tail = self.tail[a]
        self.pre[idx] = old_tail
        if old_tail:
            self.nxt[old_tail] = idx
        else:
            self.head[a] = idx

        self.tail[a] = idx
        self.size[a] += 1

    def push_front(self,a,x):
        idx = self.new_node(x)
        old_head = self.head[a]
        self.nxt[idx] = old_head
        if old_head:
            self.pre[old_head] = idx
        else:
            self.tail[a] = idx

        self.head[a] = idx
        self.size[a] += 1

    def pop_back(self,a):
        old_tail = self.tail[a]
        if not old_tail:
            return
        new_tail = self.pre[old_tail]
        self.tail[a] = new_tail

        if new_tail:
            self.nxt[new_tail] = 0
        else:
            self.head[a] = 0

        self.size[a] -= 1

    def pop_front(self,a):
        old_head = self.head[a]
        if not old_head:
            return
        new_head = self.nxt[old_head]
        self.head[a] = new_head

        if new_head:
            self.pre[new_head] = 0
        else:
            self.tail[a] = 0

        self.size[a] -= 1

    def get_size(self,a):
        return self.size[a]

    def front(self,a):
        h = self.head[a]
        if h:
            return self.val[h]
        return None

    def back(self,a):
        t = self.tail[a]
        if t:
            return self.val[t]
        return None



def main():
    q = int(sys.stdin.buffer.readline())

    deques = MultiDeque(MAX_A)
    out = []

    for _ in range(q):
        op = sys.stdin.buffer.readline().split()
        cmd = op[0]
        a = int(op[1])

        if cmd == b'push_back':
            x = int(op[2])
            deques.push_back(a,x)

        elif cmd == b'pop_back':
            deques.pop_back(a)

        elif cmd == b'push_front':
            x = int(op[2])
            deques.push_front(a,x)

        elif cmd == b'pop_front':
            deques.pop_front(a)

        elif cmd == b'size':
            out.append(str(deques.get_size(a)))

        elif cmd == b'front':
            value = deques.front(a)
            if value is not None:
                out.append(str(value))

        elif cmd == b'back':
            value = deques.back(a)
            if value is not None:
                out.append(str(value))

    sys.stdout.write('\n'.join(out))
    
if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、双端队列是什么
#
# 双端队列叫 deque，全称是 Double-Ended Queue。
# 普通队列通常只支持：
#
#     队尾插入 push_back
#     队首弹出 pop_front
#
# 也就是先进先出。
#
# 双端队列比普通队列更灵活，它的两端都能操作：
#
#     push_front   队首插入
#     push_back    队尾插入
#     pop_front    队首弹出
#     pop_back     队尾弹出
#
# 如果只使用 push_back + pop_front，
# 它就像普通队列。
#
# 如果只使用 push_back + pop_back，
# 它就像栈。
#
# 所以“双端队列”是一种抽象数据结构，
# 它只规定要支持哪些操作，并不规定底层必须怎么实现。
#
# 双端队列的常见底层实现方式有：
#
#     1. 循环数组
#        用一个数组和 head/tail 两个指针维护两端。
#
#     2. 双向链表
#        每个节点保存前驱 pre 和后继 nxt。
#
#     3. 分块数组
#        C++ STL deque 通常接近这种思路，
#        由多个小数组块组成，兼顾两端操作和随机访问。
#
# 也就是说，双端队列不一定非要用链表。
#
# 但本题要维护很多个双端队列，
# 队列编号 a 最大到 10^6，
# 操作次数 q 也最大到 10^6。
#
# 如果给每个队列都单独开数组或 deque 对象，
# 空队列也会产生额外内存开销，容易 MLE。
#
# 因此本题更适合使用：
#
#     全局节点池 + 每个队列记录 head/tail
#
# 也就是“数组模拟双向链表”的方式。
# 哪个队列真的插入元素，才创建节点；
# 没有插入元素的队列，只在 head/tail/size 中保持 0。
#
#
# 这题要维护很多个双端队列。
# 如果直接给每个编号都开一个 deque，最多可能有 10^6 个队列，
# 空 deque 对象也会占内存，极限数据容易 MLE。
#
# 所以这里不用 collections.deque，
# 而是用“数组模拟双向链表”来手写所有双端队列的底层。
#
#
# 一、整体结构
#
# 每次 push 一个元素，就新建一个节点。
# 所有节点统一存到三组数组里：
#
#     self.val[idx]   第 idx 个节点保存的值
#     self.pre[idx]   第 idx 个节点的前一个节点编号
#     self.nxt[idx]   第 idx 个节点的后一个节点编号
#
# 例如某个队列中有三个节点：
#
#     1 <-> 2 <-> 3
#
# 那么：
#
#     nxt[1] = 2
#     pre[2] = 1
#     nxt[2] = 3
#     pre[3] = 2
#
# 编号 0 被当作“空指针”，表示没有节点。
# 所以一开始数组里都先放一个 0，
# 让真实节点编号从 1 开始。
#
#
# 二、每个队列保存什么
#
# 第 a 个双端队列只需要保存三个信息：
#
#     self.head[a]   第 a 个队列的队首节点编号
#     self.tail[a]   第 a 个队列的队尾节点编号
#     self.size[a]   第 a 个队列的元素个数
#
# 如果第 a 个队列为空：
#
#     head[a] = 0
#     tail[a] = 0
#     size[a] = 0
#
# 因为题目保证 1 <= a <= 10^6，
# 所以 head、tail、size 都开到 MAX_A + 1。
# 下标 0 不使用，这样可以直接用编号 a 当数组下标。
#
#
# 三、为什么使用 array
#
# 普通 Python list 里存的是对象引用，内存开销比较大。
# 这题 q 和 a 都可能到 10^6，
# 如果大量使用 list 或很多 deque 对象，容易 MLE。
#
# array 是紧凑的整数数组：
#
#     array('i')   存 32 位整数，适合存节点编号、大小
#     array('q')   存 64 位整数，适合存元素值 x
#
# 这里：
#
#     head / tail / size / pre / nxt 用 array('i')
#     val 用 array('q')
#
#
# 四、new_node(x)
#
# 新建一个节点：
#
#     idx = len(self.val)
#
# 因为 val[0] 是占位用的 0，
# 所以第一次新建节点时 idx = 1。
#
# 然后把 x 加到 val 里，
# 并给 pre 和 nxt 也补一个位置：
#
#     val.append(x)
#     pre.append(0)
#     nxt.append(0)
#
# 最后返回这个新节点编号 idx。
#
#
# 五、push_back(a, x)
#
# 在第 a 个队列的尾部插入 x。
#
# 先创建新节点 idx，并记录原来的队尾：
#
#     idx = new_node(x)
#     old_tail = tail[a]
#
# 新节点放在原队尾后面，所以：
#
#     pre[idx] = old_tail
#
# 如果原队列不空，old_tail 存在：
#
#     nxt[old_tail] = idx
#
# 表示原来的队尾后面接上新节点。
#
# 如果原队列为空，说明这个新节点同时也是队首：
#
#     head[a] = idx
#
# 最后更新队尾和大小：
#
#     tail[a] = idx
#     size[a] += 1
#
#
# 六、push_front(a, x)
#
# 在第 a 个队列的头部插入 x。
#
# 先创建新节点 idx，并记录原来的队首：
#
#     idx = new_node(x)
#     old_head = head[a]
#
# 新节点放在原队首前面，所以：
#
#     nxt[idx] = old_head
#
# 如果原队列不空，old_head 存在：
#
#     pre[old_head] = idx
#
# 表示原来的队首前面接上新节点。
#
# 如果原队列为空，说明这个新节点同时也是队尾：
#
#     tail[a] = idx
#
# 最后更新队首和大小：
#
#     head[a] = idx
#     size[a] += 1
#
#
# 七、pop_back(a)
#
# 弹出第 a 个队列的队尾。
#
# 先看有没有队尾：
#
#     old_tail = tail[a]
#
# 如果 old_tail 是 0，说明队列为空，直接 return。
#
# 否则新的队尾应该是旧队尾的前一个节点：
#
#     new_tail = pre[old_tail]
#     tail[a] = new_tail
#
# 如果 new_tail 存在，说明弹完后队列还不空：
#
#     nxt[new_tail] = 0
#
# 表示新的队尾后面没有节点了。
#
# 如果 new_tail 不存在，说明原来只有一个元素，
# 弹完后队列为空：
#
#     head[a] = 0
#
# 最后：
#
#     size[a] -= 1
#
#
# 八、pop_front(a)
#
# 弹出第 a 个队列的队首。
#
# 先看有没有队首：
#
#     old_head = head[a]
#
# 如果 old_head 是 0，说明队列为空，直接 return。
#
# 否则新的队首应该是旧队首的后一个节点：
#
#     new_head = nxt[old_head]
#     head[a] = new_head
#
# 如果 new_head 存在，说明弹完后队列还不空：
#
#     pre[new_head] = 0
#
# 表示新的队首前面没有节点了。
#
# 如果 new_head 不存在，说明原来只有一个元素，
# 弹完后队列为空：
#
#     tail[a] = 0
#
# 最后：
#
#     size[a] -= 1
#
#
# 九、查询操作
#
# 查询大小：
#
#     size[a]
#
# 查询队首：
#
#     h = head[a]
#     如果 h != 0，答案是 val[h]
#
# 查询队尾：
#
#     t = tail[a]
#     如果 t != 0，答案是 val[t]
#
# 题目要求 front/back 为空时跳过，不输出。
# 所以 front() 和 back() 在空队列时返回 None，
# 主函数里判断：
#
#     if value is not None:
#         out.append(str(value))
#
#
# 十、复杂度
#
# 每个操作只改常数个数组位置，
# 所以时间复杂度是 O(q)。
#
# 每次 push 新建一个节点，最多 q 个节点，
# head/tail/size 各开 MAX_A + 1，
# 所以空间复杂度是 O(q + MAX_A)。
