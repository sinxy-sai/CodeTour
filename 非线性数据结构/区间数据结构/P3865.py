# ST表 RMQ（Range Minimum/Maximum Query, 区间最值查询）问题
import sys

class SparseTable:
    def __init__(self,values):
        self.n = len(values)-1
        self.log = [0]*(self.n+1)

        # 等价于预计算floor(log_2(i)) 不超过 i 的最大 2 的幂的指数     
        for i in range(2,self.n+1):
            self.log[i] = self.log[i//2]+1

        # table[k][i] 表示从i开始,长度为2^k的区间的最大值 [i,i+2^k-1]
        # table[0][i] 表示长度为1的区间
        self.table = [values] 

        k = 1

        while (1 << k) <= self.n:
            previous = self.table[-1] # 上一层的结果，区间长度为2^(k-1)
            length = 1 << k
            half = 1 << (k-1)

            current = [0]*(self.n+1)

            for i in range(1,self.n - length + 2):

                current[i] = max(previous[i],previous[i+half])

            self.table.append(current)
            k += 1

    def query_max(self,left,right):
        length = right - left +1
        k = self.log[length]
        block_length = 1 << k
        return max(self.table[k][left],self.table[k][right-block_length+1])


def main():
    input = sys.stdin.buffer.readline
    n,m = map(int,input().split())
    data = [0]+list(map(int,input().split()))

    st = SparseTable(data) 
    out = []
    for _ in range(m):
        left,right = map(int,input().split())
        out.append(st.query_max(left,right))

    sys.stdout.buffer.write('\n'.join(map(str,out)).encode())


if __name__ == '__main__':
    main()


# 思路说明：
#
# 一、ST 表是什么
#
# ST 表的全称是 Sparse Table，
# 适合解决静态区间查询问题。
#
# “静态”表示：
#
#     数列建立之后不会再修改
#
# 本题需要进行很多次：
#
#     查询区间 [left, right] 的最大值
#
# 由于没有修改操作，
# 可以先花时间预处理，
# 换取每次查询 O(1) 的速度。
#
# 这正是 ST 表的适用场景。
#
#
# 二、为什么不用线段树或普通遍历
#
# 如果每次查询都遍历 [left, right]，
# 单次查询最坏是 O(n)。
#
# M 最大为 2 * 10^6，
# 这样会非常慢。
#
# 线段树可以做到单次 O(log n)，
# 但题目要求最大数据时查询 O(1)，
# 所以使用 ST 表。
#
#
# 三、table[k][i] 表示什么
#
# 本程序定义：
#
#     table[k][i]
#
# 表示：
#
#     从 i 开始，长度为 2^k 的区间最大值
#
# 也就是区间：
#
#     [i, i + 2^k - 1]
#
# 例如：
#
#     table[0][i]
#     表示长度为 1 的区间 [i, i]
#
#     table[1][i]
#     表示长度为 2 的区间 [i, i + 1]
#
#     table[2][i]
#     表示长度为 4 的区间 [i, i + 3]
#
#     table[3][i]
#     表示长度为 8 的区间 [i, i + 7]
#
# 初始的：
#
#     self.table = [values]
#
# 就是先保存 k = 0 的结果。
#
#
# 四、ST 表如何转移
#
# 长度为 2^k 的区间，
# 可以拆成两个长度为 2^(k-1) 的区间：
#
#     左半部分：
#     [i, i + 2^(k-1) - 1]
#
#     右半部分：
#     [i + 2^(k-1), i + 2^k - 1]
#
# 所以：
#
#     table[k][i] =
#         max(
#             table[k-1][i],
#             table[k-1][i + 2^(k-1)]
#         )
#
# 对应代码：
#
#     previous = self.table[-1]
#     length = 1 << k
#     half = 1 << (k - 1)
#
#     current[i] = max(
#         previous[i],
#         previous[i + half]
#     )
#
# 其中：
#
#     previous[i]
#     是左半段最大值
#
#     previous[i + half]
#     是右半段最大值
#
#
# 五、1 << k 是什么
#
#     1 << k
#
# 表示把二进制的 1 左移 k 位，
# 等价于：
#
#     2^k
#
# 例如：
#
#     1 << 0 = 1
#     1 << 1 = 2
#     1 << 2 = 4
#     1 << 3 = 8
#
# 所以：
#
#     length = 1 << k
#
# 表示当前区间长度是 2^k。
#
#
# 六、log 数组的作用
#
# 代码：
#
#     self.log = [0] * (self.n + 1)
#
#     for i in range(2, self.n + 1):
#         self.log[i] = self.log[i // 2] + 1
#
# self.log[i] 表示：
#
#     floor(log2(i))
#
# 也就是不超过 i 的最大 2 的幂的指数。
#
# 例如：
#
#     log[1] = 0
#     log[2] = 1
#     log[3] = 1
#     log[4] = 2
#     log[5] = 2
#     log[6] = 2
#     log[7] = 2
#     log[8] = 3
#
# 注意 range(2, n + 1) 从 2 开始，
# 所以 log[1] 保持初始化值 0。
#
# 查询长度为 length 的区间时，
# 用：
#
#     k = self.log[length]
#
# 就能 O(1) 得到最大的 k，
# 使得 2^k <= length。
#
#
# 七、如何做到 O(1) 查询
#
# 查询区间 [left, right] 时：
#
#     length = right - left + 1
#     k = self.log[length]
#     block_length = 1 << k
#
# 取两个长度为 2^k 的区间：
#
#     第一个：
#     [left, left + 2^k - 1]
#
#     第二个：
#     [right - 2^k + 1, right]
#
# 代码：
#
#     max(
#         self.table[k][left],
#         self.table[k][right - block_length + 1]
#     )
#
# 为什么这两个区间能覆盖 [left, right]？
#
# 因为：
#
#     2^k <= length
#
# 第一个区间从左端开始，
# 第二个区间从右端结束。
#
# 当 length 不是 2 的幂时，
# 两个区间可能重叠。
#
# 例如查询 [2,7]，长度是 6：
#
#     k = floor(log2(6)) = 2
#     2^k = 4
#
# 两个区间是：
#
#     [2,5]
#     [4,7]
#
# 它们覆盖了完整的 [2,7]，
# 中间 [4,5] 重叠。
#
# 对最大值来说，区间重叠没有问题：
#
#     max(max([2,5]), max([4,7]))
#
# 仍然等于 max([2,7])。
#
# 这也是 ST 表可以做到 O(1) 查询的关键。
#
#
# 八、为什么 ST 表只能直接处理静态数据
#
# ST 表预处理了大量固定区间的答案。
#
# 如果修改某个 a[x]，
# 所有包含 x 的预处理区间都可能失效，
# 需要重新计算大量 table。
#
# 所以 ST 表适合：
#
#     预处理一次
#     查询很多次
#     中间不修改数据
#
# 如果有修改操作，
# 应考虑树状数组或线段树。
#
#
# 九、复杂度分析
#
# log 数组预处理：
#
#     O(n)
#
# ST 表建表：
#
#     O(n log n)
#
# 因为共有 O(log n) 层，
# 每层最多计算 O(n) 个区间块。
#
# 单次区间最大值查询：
#
#     O(1)
#
# 总查询复杂度：
#
#     O(m)
#
# 总时间复杂度：
#
#     O(n log n + m)
#
# 空间复杂度：
#
#     table 有 O(log n) 层，
#     每层最多 O(n) 个元素
#
# 所以空间复杂度是：
#
#     O(n log n)
#
#
# 十、为什么本题强调查询 O(1)
#
# 本题 M 最大为 2 * 10^6。
#
# 如果每次查询 O(log n)，
# 总复杂度会达到：
#
#     O(m log n)
#
# 如果每次查询 O(n)，
# 更无法通过。
#
# ST 表把查询阶段压缩成只读取两个预处理值，
# 所以单次查询是 O(1)，
# 适合本题大量静态区间最大值查询。
