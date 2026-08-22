# 哈夫曼编码树
# 最小堆 DFS 二叉树
import sys
import heapq

class HuffmanTree:
    def __init__(self,words,weights):
        self.words = words
        self.n = len(words)
        self.weights = weights[:]
        self.left = [-1] * self.n
        self.right = [-1] * self.n
        self.symbol = list(range(self.n))
        self.heap = [(weight,index) for index,weight in enumerate(self.weights)]  # index是第二个关键字，解决权重相同时的比较问题
        heapq.heapify(self.heap)     # 建立最小堆


    def build(self):
        if self.n == 1:
            return 0

        while len(self.heap) > 1:
            weight1,node1 = heapq.heappop(self.heap)
            weight2,node2 = heapq.heappop(self.heap)

            parent = len(self.weights)

            new_weight = weight1 + weight2

            self.weights.append(new_weight)
            self.left.append(node1)
            self.right.append(node2)
            self.symbol.append(-1)

            heapq.heappush(self.heap,(new_weight,parent))

        # 哈夫曼树构造完成后，堆中只剩一个根节点
        # self.heap[0][0]是堆顶根节点的权重，self.heap[0][1]是堆顶根节点的索引
        return self.heap[0][1]

    def getcodes(self,root):
        codes = ['']*self.n
        path = []

        def dfs(node):
            # 终止条件
            if self.symbol[node] != -1: 
                index = self.symbol[node]
                if self.n == 1:
                    codes[index] = '0'
                else:
                    codes[index] = ''.join(path) or '0'
                return

            # 左边为0，右边为1
            path.append('0')
            dfs(self.left[node])
            path.pop()

            path.append('1')
            dfs(self.right[node])
            path.pop()


        dfs(root)
        return codes
    

def main():
    input = sys.stdin.buffer.readline
    n = int(input())

    words = []
    weights = []
    for _ in range(n):
        word,weight = input().split()
        words.append(word.decode())
        weights.append(int(weight))

    tree = HuffmanTree(words,weights)
    root = tree.build()
    codes = tree.getcodes(root)

    out = []
    for word,code in zip(words,codes):
        out.append(f'{word} {code}')

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    main()

# ============================================================
# B2168 哈夫曼编码：理论、算法思路与细节
# ============================================================
#
# 一、哈夫曼编码是什么
#
# 哈夫曼编码是一种变长编码。
#
# 出现频率较高的单词使用较短的编码；
# 出现频率较低的单词使用较长的编码。
#
# 例如：
#
#     高频单词 -> 0
#     低频单词 -> 1101
#
# 这样可以让所有单词的总编码长度尽可能小。
#
#
# 二、前缀编码
#
# 哈夫曼编码要求满足前缀性质：
#
#     任意一个单词的编码，都不能是另一个单词编码的前缀。
#
# 例如：
#
#     0
#     10
#     11
#
# 是合法的前缀编码。
#
# 但是：
#
#     0
#     01
#
# 不合法，因为 0 是 01 的前缀。
#
# 哈夫曼树中所有单词都位于叶子节点，
# 因此一个叶子节点不可能是另一个叶子节点的祖先，
# 自然满足前缀性质。
#
#
# 三、哈夫曼树
#
# 每个单词最初对应一个叶子节点。
#
#     节点权值 = 单词出现频率
#
# 从根节点到叶子节点的路径就是该单词的编码：
#
#     向左走：编码 0
#     向右走：编码 1
#
# 如果某个单词从根节点经过：
#
#     左 -> 右 -> 左
#
# 那么它的编码就是：
#
#     010
#
#
# 四、带权路径长度 WPL
#
# 如果第 i 个单词的频率为 wi，
# 它的编码长度为 li，
# 那么总带权路径长度为：
#
#     WPL = w1 * l1 + w2 * l2 + ... + wn * ln
#
# 哈夫曼算法的目标就是让 WPL 最小。
#
# 频率越高的单词应该尽量靠近根节点，
# 这样编码长度更短，对 WPL 的贡献更小。
#
#
# 五、贪心策略
#
# 哈夫曼算法每次执行：
#
#     取出权值最小的两个节点；
#     合并成一个新节点；
#     新节点权值等于两个节点权值之和；
#     把新节点重新放回集合。
#
# 例如权值为：
#
#     1, 2, 3, 4
#
# 第一步：
#
#     1 + 2 = 3
#
# 剩余：
#
#     3, 3, 4
#
# 第二步：
#
#     3 + 3 = 6
#
# 剩余：
#
#     4, 6
#
# 第三步：
#
#     4 + 6 = 10
#
# 最后得到根节点。
#
# 这种“每次选择当前最小的两个”的方法叫贪心算法。
#
#
# 六、为什么使用最小堆
#
# 每一步都需要快速找到权值最小的两个节点。
#
# Python 的 heapq 默认是小根堆：
#
#     heapq.heappop(heap)
#
# 可以取出当前权值最小的节点。
#
# 堆中的元素通常写成：
#
#     (weight, node_id)
#
# Python 会先比较 weight；
# 如果权值相同，再比较 node_id。
#
# 因此 node_id 可以作为第二关键字，
# 避免节点权值相同时无法比较节点对象。
#
#
# 七、节点数组的含义
#
#     weight[node]
#
# 表示节点的权值。
#
#     left[node]
#
# 表示节点的左孩子编号。
#
#     right[node]
#
# 表示节点的右孩子编号。
#
#     symbol[node]
#
# 表示叶子节点对应的单词下标。
#
# 如果：
#
#     symbol[node] != -1
#
# 说明该节点是叶子节点，对应一个单词。
#
# 如果：
#
#     symbol[node] == -1
#
# 说明该节点是内部节点。
#
#
# 八、叶子节点与内部节点
#
# 初始的 n 个节点都是叶子节点：
#
#     symbol[node] = 单词下标
#     left[node] = -1
#     right[node] = -1
#
# 每次合并两个节点时，新建一个内部节点：
#
#     left[parent] = node1
#     right[parent] = node2
#     symbol[parent] = -1
#
# 新节点的权值为：
#
#     weight[parent] = weight[node1] + weight[node2]
#
#
# 九、DFS 生成编码
#
# 哈夫曼树建好后，从根节点开始 DFS。
#
# 进入左子树时：
#
#     path.append('0')
#
# 进入右子树时：
#
#     path.append('1')
#
# 到达叶子节点时，当前 path 就是该单词的编码。
#
# 搜索完左子树后必须撤销：
#
#     path.pop()
#
# 然后才能正确搜索右子树。
#
# 基本结构：
#
#     path.append('0')
#     dfs(left[node])
#     path.pop()
#
#     path.append('1')
#     dfs(right[node])
#     path.pop()
#
#
# 十、为什么需要回溯
#
# 假设当前路径为：
#
#     path = ['0', '1']
#
# 搜索左子树时追加：
#
#     path.append('0')
#
# 得到：
#
#     010
#
# 搜索结束后必须执行：
#
#     path.pop()
#
# 恢复为：
#
#     01
#
# 然后再追加右分支：
#
#     011
#
# 如果不撤销，路径会混入之前分支的编码。
#
#
# 十一、为什么输出顺序仍然是输入顺序
#
# 哈夫曼树的 DFS 顺序不一定和输入顺序一致。
#
# 因此不能直接按照 DFS 遍历顺序输出单词。
#
# 插入叶子节点时，保存它对应的输入下标：
#
#     symbol[node] = index
#
# 生成编码时：
#
#     codes[index] = 当前路径
#
# 最后按照：
#
#     codes[0], codes[1], ..., codes[n - 1]
#
# 输出，就能恢复输入顺序。
#
#
# 十二、只有一个单词的特殊情况
#
# 如果 n == 1，哈夫曼树只有一个根节点，
# 根节点没有边，正常情况下路径为空。
#
# 但题目需要输出一个 01 字符串，
# 所以通常规定它的编码为：
#
#     0
#
# 这就是单独处理 n == 1 的原因。
#
#
# 十三、算法流程
#
# 1. 为每个单词建立一个叶子节点；
#
# 2. 把所有叶子节点放入最小堆；
#
# 3. 重复取出权值最小的两个节点；
#
# 4. 合并成新节点并放回最小堆；
#
# 5. 堆中只剩一个节点时，它就是根节点；
#
# 6. 从根节点 DFS；
#
# 7. 左边追加 0，右边追加 1；
#
# 8. 到达叶子节点时保存编码；
#
# 9. 按输入顺序输出所有单词和编码。
#
#
# 十四、复杂度
#
# 初始有 n 个节点。
# 每次合并两个节点，并新建一个节点，
# 一共需要合并 n - 1 次。
#
# 每次从最小堆中取出或加入节点的复杂度为：
#
#     O(log n)
#
# 所以建树的时间复杂度为：
#
#     O(n log n)
#
# DFS 遍历哈夫曼树需要访问所有节点，
# 复杂度为：
#
#     O(n)
#
# 如果把编码字符串的总长度也计算进去，
# 总时间复杂度可以写成：
#
#     O(n log n + 编码总长度)
#
# 哈夫曼树最多有 2n - 1 个节点，
# 因此空间复杂度为：
#
#     O(n)
#
#
# 十五、这道题考查的知识点
#
#     1. 贪心算法；
#     2. 优先队列；
#     3. 最小堆；
#     4. 二叉树；
#     5. DFS；
#     6. 路径回溯；
#     7. 前缀编码；
#     8. 带权路径长度 WPL。
