# AC自动机(简单版)
import sys
from collections import deque

class AhoCorasick:

    def __init__(self):
        # children[node]：
        # 当前节点通过某个字符可以到达的子节点
        self.children = [{}]
        # fail[node]：失配指针
        self.fail = [0]
        # count[node]：
        # 在当前节点结束的模式串数量
        self.count = [0]

    def insert(self,s):
        node = 0

        for ch in s:
            next_node = self.children[node].get(ch)
            if next_node is None:
                next_node = len(self.children)
                self.children[node][ch] = next_node
                self.children.append({})
                self.fail.append(0)
                self.count.append(0)

            node = next_node

        self.count[node] += 1

    def build_fail(self):
        queue = deque()

        # 根节点的所有儿子入队
        for child in self.children[0].values():
            queue.append(child)

        while queue:
            node = queue.popleft()

            for ch,child in self.children[node].items():
                fail_node = self.fail[node]

                while(fail_node != 0 and ch not in self.children[fail_node]):
                    fail_node = self.fail[fail_node]

                self.fail[child] = self.children[fail_node].get(ch,0)

                queue.append(child)


    def query(self,text):
        node = 0
        ans = 0

        for ch in text:
            # 当前节点无法匹配 ch，就沿 fail 指针跳转
            while(node !=0 and ch not in self.children[node]):
                node = self.fail[node]

            node = self.children[node].get(ch,0)

            check = node

            while check != 0:
                if self.count[check] != 0:
                    ans += self.count[check]
                    # 标记该节点已经统计过，
                    # 避免同一个模式串重复计数
                    self.count[check] = 0

                check = self.fail[check]

        return ans

def main():
    input = sys.stdin.readline
    n = int(input())

    ac = AhoCorasick()

    for _ in range(n):
        pattern = input().strip()
        ac.insert(pattern)

    text = input().strip()

    ac.build_fail()

    sys.stdout.write(str(ac.query(text)))

if __name__ == '__main__':
    main()


# ==================== 算法理论、思路与细节 ====================
#
# 一、题目要求
#
# 给出 n 个模式串和一个文本串，
# 求有多少个不同编号的模式串至少在文本中出现过一次。
#
# 注意：
#
#     不是统计模式串出现的总次数，
#     而是统计出现过的模式串编号数量。
#
# 例如模式串为：
#
#     a
#     aa
#     aa
#
# 文本串为：
#
#     aaa
#
# 答案是 3。
#
# 因为第 2 个和第 3 个模式串虽然内容相同，
# 但编号不同，需要分别计数。
#
#
# 二、为什么使用 AC 自动机
#
# 如果只有一个模式串，可以使用 KMP。
#
# 如果有很多模式串，逐个使用 KMP，
# 就需要反复扫描文本，效率较低。
#
# AC 自动机可以看成：
#
#     Trie + 失配指针 fail
#
# 其中：
#
#     Trie：
#         同时保存所有模式串
#
#     fail：
#         当前匹配失败时，跳到仍然可能匹配的后缀
#
# 处理过程分为三步：
#
#     1. 把所有模式串插入 Trie
#     2. 使用 BFS 建立 fail 指针
#     3. 扫描文本串并统计匹配结果
#
#
# 三、Trie 中的节点含义
#
# children[node] 是一个字典，
# 表示当前节点通过哪些字符可以继续转移。
#
# 例如：
#
#     children[0]['a'] = 1
#
# 表示：
#
#     根节点经过字符 a，可以到达节点 1。
#
# 一个节点代表从根节点走到它经过的字符串。
#
# 例如：
#
#     根 -> a -> b
#
# 对应字符串：
#
#     ab
#
#
# 四、count[node] 的含义
#
# count[node] 表示：
#
#     有多少个模式串恰好在 node 对应的字符串结束。
#
# 插入模式串时：
#
#     self.count[node] += 1
#
# 如果模式串 aa 出现了两次，
# 它们会共用同一个 Trie 节点，
# 但 count[node] 会变成 2。
#
# 这正好符合题目中“编号不同就算不同模式串”的要求。
#
#
# 五、什么是 fail 指针
#
# fail[node] 表示：
#
#     当前节点对应字符串的最长真后缀，
#     且这个后缀也是 Trie 中存在的前缀。
#
# 例如有模式串：
#
#     a
#     ba
#
# 节点 ba 的后缀有：
#
#     a
#     空字符串
#
# 其中 a 也是 Trie 中的前缀，
# 所以：
#
#     fail[ba] = a
#
# 如果当前匹配到了 ba，
# 后面继续匹配失败，
# 就可以跳到 a 继续尝试，
# 而不必回到文本串的开头。
#
#
# 六、build_fail：建立失配指针
#
# 根节点的所有儿子的 fail 指针都是根节点，
# 因此先把它们加入 BFS 队列：
#
#     for child in self.children[0].values():
#         queue.append(child)
#
# 这些节点表示单个字符，
# 没有更短的非空后缀。
#
# 之后按照 BFS 顺序处理每个节点。
# 这样可以保证：
#
#     当前节点的 fail 指针已经建立完成，
#     才去计算它的儿子的 fail 指针。
#
# 对于当前节点 node 的一个儿子 child，
# 边上的字符为 ch。
#
#     node --ch--> child
#
# 先跳到父节点的 fail 位置：
#
#     fail_node = self.fail[node]
#
# 然后检查 fail_node 是否有字符 ch 的边。
#
# 如果没有：
#
#     while fail_node != 0 and \
#           ch not in self.children[fail_node]:
#         fail_node = self.fail[fail_node]
#
# 就继续沿 fail 指针向上跳。
#
# 找到可以接上 ch 的节点后：
#
#     self.fail[child] =
#         self.children[fail_node].get(ch, 0)
#
# 如果找到字符 ch，就把 child 的 fail 指向对应节点；
# 如果根节点也没有 ch，就指向 0，也就是根节点。
#
# 例如模式串：
#
#     ab
#     ba
#     bab
#
# 节点 bab 的父节点是 ba。
#
#     fail[ba] = a
#
# 节点 a 通过字符 b 可以到达 ab，
# 所以：
#
#     fail[bab] = ab
#
# 这表示 bab 匹配失败后，
# 仍然可以保留后缀 ab。
#
#
# 七、query：扫描文本串
#
# node 表示当前已经匹配到的 Trie 节点。
#
# 扫描文本的每个字符 ch 时，
# 如果当前节点没有 ch 这条边：
#
#     while node != 0 and \
#           ch not in self.children[node]:
#         node = self.fail[node]
#
# 就沿着 fail 指针向上跳，
# 尝试保留当前字符串的某个后缀。
#
# 找到可以继续匹配的位置后：
#
#     node = self.children[node].get(ch, 0)
#
# 如果能沿 ch 转移，就进入对应儿子；
# 如果根节点也没有 ch，就回到根节点 0。
#
# 这个过程不会回退文本指针，
# 只会改变 Trie 中的状态 node。
#
#
# 八、为什么要检查整个 fail 链
#
# 当前节点对应的字符串，
# 它的后缀也可能是模式串。
#
# 例如模式串：
#
#     a
#     aa
#     aaa
#
# 当当前状态是 aaa 时，
# 同时匹配了：
#
#     aaa
#     aa
#     a
#
# 因此代码从当前节点开始，
# 不断沿 fail 指针向上检查：
#
#     check = node
#
#     while check != 0:
#         ...
#         check = self.fail[check]
#
# 依次检查当前字符串及其所有可匹配后缀。
#
#
# 九、为什么找到模式串后要把 count 置零
#
# 题目只要求判断模式串是否出现过，
# 同一个模式串出现多次只能贡献一次。
#
# 例如：
#
#     模式串：a
#     文本串：aaa
#
# 答案应该是 1，而不是 3。
#
# 第一次找到节点 a 时：
#
#     ans += count[a]
#     count[a] = 0
#
# 后面再次找到 a 时，
# count[a] 已经是 0，
# 因此不会重复计数。
#
# 如果两个编号不同的模式串内容相同，
# 例如：
#
#     a
#     a
#
# 它们共用一个节点，但：
#
#     count[a] = 2
#
# 第一次匹配时会一次性增加 2。
#
#
# 十、算法正确性
#
# 1. Trie 保存了所有模式串的完整路径，
#    所以每个模式串的结尾都对应一个节点。
#
# 2. fail[node] 指向当前字符串的最长可匹配后缀，
#    所以匹配失败时不会漏掉仍然可能成功的模式串。
#
# 3. 扫描到某个状态时，
#    当前节点和 fail 链上的节点正好表示当前文本后缀中
#    所有可能出现的模式串。
#
# 4. count 只在第一次匹配时被计入答案，
#    因此每个模式串编号只贡献一次。
#
#
# 十一、复杂度
#
# 设所有模式串总长度为 L，
# 文本串长度为 T。
#
# 建立 Trie：
#
#     O(L)
#
# 建立 fail 指针：
#
#     BFS 遍历 Trie 节点和边。
#
# 查询文本：
#
#     沿 Trie 和 fail 指针进行匹配。
#
# 这份代码为了易读，
# 在 query 中会沿 fail 链检查模式串，
# 因此某些特殊数据下可能出现较多重复遍历，
# Python 版本可能 TLE。
#
# 空间复杂度：
#
#     O(L)
#
# 因为 Trie 节点数量最多是所有模式串长度之和加 1。
