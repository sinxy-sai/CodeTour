# 字典树Trie
import sys

class Trie:
    def __init__(self):
        self.children = [{}]
        self.count = [0]


    def insert(self,s):
        node = 0

        for ch in s:
            next_node = self.children[node].get(ch)
            if next_node is None:
                next_node = len(self.children)
                self.children[node][ch] = next_node
                self.children.append({})
                self.count.append(0)
            node = next_node
            self.count[node] += 1

    def query(self,s):
        node = 0

        for ch in s:
            next_node = self.children[node].get(ch)
            if next_node is None:
                return 0
            node = next_node
        return self.count[node]

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out = []

    for _ in range(T):
        n = int(next(it))
        q = int(next(it))

        trie = Trie()

        for _ in range(n):
            trie.insert(next(it))

        for _ in range(q):
            out.append(str(trie.query(next(it))))

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、字典树是什么
#
# 字典树也叫 Trie。
# 它是一种专门处理字符串前缀的数据结构。
#
# Trie 的核心特点是：
#
#     每条边表示一个字符
#     从根节点走到某个节点，路径上的字符拼起来就是一个前缀
#
# 例如插入：
#
#     fusu
#     abcde
#     fusufusu
#
# 字典树大概是：
#
#     root
#     ├── f
#     │   └── u
#     │       └── s
#     │           └── u
#     │               └── f
#     │                   └── u
#     │                       └── s
#     │                           └── u
#     └── a
#         └── b
#             └── c
#                 └── d
#                     └── e
#
# 其中：
#
#     root -> f -> u -> s -> u
#
# 代表前缀：
#
#     fusu
#
#
# 二、本题要解决什么
#
# 本题给定 n 个模式串 s_1, s_2, ..., s_n。
# 每次询问给一个字符串 t，
# 要回答有多少个模式串 s_j 满足：
#
#     t 是 s_j 的前缀
#
# 也就是：
#
#     有多少个模式串以 t 开头
#
# 例如模式串有：
#
#     fusu
#     fusufusu
#     anguei
#
# 查询：
#
#     fusu
#
# 答案是 2，
# 因为 fusu 和 fusufusu 都以 fusu 开头。
#
#
# 三、节点怎么存
#
# 本程序使用两个数组来存 Trie：
#
#     self.children = [{}]
#     self.count = [0]
#
# self.children 是“节点数组”。
# 每个 self.children[node] 是一个字典，
# 表示 node 这个节点有哪些出边。
#
# 例如：
#
#     self.children[0] = {
#         b'f': 1,
#         b'a': 5
#     }
#
# 表示：
#
#     从 0 号节点走字符 f，到 1 号节点
#     从 0 号节点走字符 a，到 5 号节点
#
# 可以把它画成：
#
#     0 --f--> 1
#     0 --a--> 5
#
# 根节点编号是 0。
#
#
# 四、为什么新节点编号是 len(self.children)
#
# self.children 是节点数组。
# 如果当前有 5 个节点，
# 那么已有节点编号是：
#
#     0, 1, 2, 3, 4
#
# 下一个新节点 append 到数组末尾后，
# 它的编号就是：
#
#     5
#
# 也就是当前的：
#
#     len(self.children)
#
# 所以当前代码先写：
#
#     next_node = len(self.children)
#     self.children[node][ch] = next_node
#
# 表示：
#
#     从当前 node 节点走字符 ch，
#     会到达编号为 next_node 的新节点。
#
# 随后：
#
#     self.children.append({})
#     self.count.append(0)
#
# 才是真的把这个新节点加入节点数组。
#
# 注意不是 len(self.children) + 1。
# 因为 Python 下标从 0 开始，
# 长度为 5 的数组，下一个下标正好是 5。
#
#
# 五、count[node] 怎么理解
#
# self.count[node] 表示：
#
#     有多少个模式串经过了 node 这个节点
#
# 而每个节点代表一个前缀，
# 所以也可以理解成：
#
#     有多少个模式串拥有这个前缀
#
# 插入 fusu 时，会经过这些前缀节点：
#
#     f
#     fu
#     fus
#     fusu
#
# 所以这些节点的 count 都会加 1。
#
# 如果再插入 fusufusu，
# 它也会经过前缀 fusu，
# 所以 fusu 对应节点的 count 会变成 2。
#
# 查询 fusu 时，
# 走到 fusu 对应节点后返回 count[node]，
# 就能得到有多少个模式串以 fusu 为前缀。
#
# count[node] 不是表示这个字符串完整出现了几次，
# 而是表示：
#
#     有多少个模式串经过当前前缀节点
#
#
# 六、insert(s)：插入模式串
#
# 代码：
#
#     def insert(self, s):
#         node = 0
#
#         for ch in s:
#             next_node = self.children[node].get(ch)
#             if next_node is None:
#                 next_node = len(self.children)
#                 self.children[node][ch] = next_node
#                 self.children.append({})
#                 self.count.append(0)
#             node = next_node
#             self.count[node] += 1
#
# 插入过程：
#
#     1. 从根节点 0 开始
#     2. 依次读取字符串里的每个字符 ch
#     3. 用 get(ch) 查当前节点有没有 ch 这条边
#     4. 如果没有，就创建新节点，并把 ch 指向这个新节点
#     5. 沿着 ch 这条边走到下一个节点
#     6. 当前节点代表的前缀被一个模式串经过，所以 count[node] += 1
#
# 为什么这里使用 get(ch)：
#
# 原始写法可能是：
#
#     if ch not in self.children[node]:
#         ...
#     node = self.children[node][ch]
#
# 这会先做一次 in 查询，
# 后面又做一次 [] 查询，
# 等于可能查了两次字典。
#
# 当前写法：
#
#     next_node = self.children[node].get(ch)
#
# 只查一次。
# 如果查不到，返回 None；
# 如果查得到，直接返回下一个节点编号。
#
# 这能减少哈希表查询次数，是本程序能 AC 的关键优化之一。
#
# 注意：
# 节点编号从 0 开始，
# 新节点编号使用 len(self.children)，
# 所以合法节点编号永远不会是 None。
# 因此可以安全地用 None 表示“这条边不存在”。
#
# 因为本程序用 sys.stdin.buffer.read().split() 一次性读入，
# 所以字符串是 bytes 类型。
# 遍历 bytes 时，ch 是字符对应的整数编码。
# 例如 b'fusu' 中的 ch 依次是：
#
#     102, 117, 115, 117
#
# 这不影响 Trie 的逻辑，
# 因为字典的 key 可以是整数。
# 也就是说：
#
#     self.children[node][102] = next_node
#
# 可以理解成：
#
#     从当前节点走字符 f 到 next_node
#
#
# 七、query(s)：查询前缀数量
#
# 代码：
#
#     def query(self, s):
#         node = 0
#
#         for ch in s:
#             next_node = self.children[node].get(ch)
#             if next_node is None:
#                 return 0
#             node = next_node
#         return self.count[node]
#
# 查询过程：
#
#     1. 从根节点 0 开始
#     2. 按照查询串 s 的字符一路往下走
#     3. 每一步都用 get(ch) 查当前节点的 ch 边
#     4. 如果某一步没有对应字符边，说明没有模式串拥有这个前缀，返回 0
#     5. 如果能顺利走完整个 s，当前节点就是 s 这个前缀对应的节点
#     6. 返回 count[node]
#
# 为什么返回 count[node] 就是答案？
#
# 因为 count[node] 记录的是：
#
#     有多少个模式串经过当前前缀节点
#
# 能经过这个节点，
# 就说明这个模式串以查询串 s 为前缀。
#
#
# 八、多组数据
#
# 题目有 T 组测试数据。
# 每组数据都要重新建立一棵 Trie：
#
#     trie = Trie()
#
# 不能把上一组数据的 Trie 留到下一组，
# 否则不同测试组之间会互相影响。
#
# 本程序输入使用：
#
#     data = sys.stdin.buffer.read().split()
#     it = iter(data)
#
# 这样会一次性读入全部输入，
# 后面通过：
#
#     next(it)
#
# 依次取出 T、n、q、模式串和询问串。
#
# 这比反复调用 readline() 更快。
# 本题字符串总长度很大，
# 操作次数也很多，
# 减少 IO 调用次数对 Python 很重要。
#
# 所有答案统一放到 out 中，
# 最后一次性输出：
#
#     sys.stdout.write('\n'.join(out))
#
# 这样可以减少频繁 print 带来的 IO 开销。
#
#
# 九、复杂度分析
#
# 插入一个字符串 s：
#
#     O(len(s))
#
# 查询一个字符串 t：
#
#     O(len(t))
#
# 因为每个字符只走一步 Trie 边。
#
# 题目保证输入字符串总长度不超过 3 * 10^6，
# 所以总时间复杂度是：
#
#     O(所有字符串总长度)
#
# 空间复杂度：
#
# Trie 中最多为每个模式串字符创建一个节点，
# 所以节点数最多是所有模式串长度之和。
#
# 因此空间复杂度是：
#
#     O(所有模式串总长度)
#
#
# 十、为什么这个 Python 版本能 AC
#
# 本程序使用 dict 存每个节点的出边，
# 写法直观，适合理解 Trie。
#
# 这个版本能 AC，主要靠几个 Python 层面的常数优化：
#
# 1. 一次性读入
#
#     data = sys.stdin.buffer.read().split()
#
# 避免大量 readline() 调用。
# 对本题这种输入规模很大的题，IO 优化很关键。
#
# 2. 不 decode 字符串
#
# 程序直接处理 bytes。
# 遍历 bytes 时，ch 是整数编码，
# 可以直接作为字典 key。
#
# 这样避免了把 bytes 转成 str 的额外开销。
#
# 3. 用 dict.get(ch) 查边
#
# 原写法：
#
#     if ch not in self.children[node]:
#         ...
#     node = self.children[node][ch]
#
# 可能进行了两次字典查询。
#
# 当前写法：
#
#     next_node = self.children[node].get(ch)
#
# 只查一次，
# 查询不到就返回 None。
#
# 这比 not in + [] 更省常数。
#
# 4. 保留类，但核心数据结构仍然简单
#
# Trie 类让代码可读性比较好。
# 虽然类方法和 self.children 会有一点点额外开销，
# 但本程序已经通过 IO 和 get 优化抵消了主要瓶颈。
#
# 和完全局部变量版本相比，
# 这个版本可能略慢一点，
# 但可读性更好，并且已经可以通过本题。
#
# 5. 为什么不一定要用数组模拟
#
# 在 Python 中，数组模拟 Trie 不一定更快。
# 如果用链式数组存边，
# 查询一条边时往往要在 Python 层 while 扫描。
#
# 而 dict.get 的哈希查找底层主要由 C 实现，
# 实际常数可能更低。
#
# 所以对这题来说，
# “dict Trie + 快速 IO + get 查询”反而是更适合 Python 的写法。
#
# 复杂度没有变：
#
#     时间复杂度仍是 O(所有字符串总长度)
#     空间复杂度仍是 O(所有模式串总长度)
#
# 变化的是实现常数。
