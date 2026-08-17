# 手写哈希表模板 拉链法
import sys

class ChainHashMap:
    def __init__(self,size):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash(self,key):
        return key % self.size

    def set(self,key,value):
        pos = self.hash(key)
        for i,(k,v) in enumerate(self.buckets[pos]):
            if k == key:
                self.buckets[pos][i] = (key,value)
                return
        self.buckets[pos].append((key,value))

    def get(self,key):
        pos = self.hash(key)
        for k,v in self.buckets[pos]:
            if  k == key:
                return v
        return 0

def main():
    n = int(sys.stdin.readline())

    mp = ChainHashMap(n * 2)
    ans = 0
    mod = 1 << 64 # 等价于 2^64

    for i in range(1,n+1):
        x,y = map(int,sys.stdin.readline().split())
        old = mp.get(x)
        ans = (ans + i * old) % mod
        mp.set(x,y)

    sys.stdout.write(str(ans))

if __name__ == '__main__':
    main()


# 思路说明：拉链法哈希表
#
# 题目要维护一个映射 f(x)。
# 每次操作给出 x 和 y，需要先得到旧的 f(x)，再把 f(x) 改成 y。
# 所以主流程是：
#
#     old = mp.get(x)
#     ans += i * old
#     mp.set(x, y)
#
# 这里没有直接用 Python 内置 dict，而是自己实现哈希表。
#
# 拉链法的核心：
#
#     pos = hash(key)
#
# 先通过哈希函数把 key 映射到一个桶的位置。
# 但是不同 key 可能得到同一个 pos，这叫哈希冲突。
# 拉链法的处理方式是：每个桶里放一个列表，冲突的元素都放进同一个桶里。
#
# 在本程序中：
#
#     self.buckets = [[] for _ in range(size)]
#
# 表示有 size 个桶，每个桶都是一个列表。
# 桶里的元素是二元组：
#
#     (key, value)
#
# 查询 get(key)：
#
# 1. 先计算 pos = key % size。
# 2. 只在 buckets[pos] 这个桶里查找。
# 3. 如果找到 key，返回对应 value。
# 4. 如果没找到，说明 f(key) 还是初始值 0。
#
# 修改 set(key, value)：
#
# 1. 先计算 pos = key % size。
# 2. 在 buckets[pos] 里找 key。
# 3. 如果 key 已经存在，就更新它的 value。
# 4. 如果 key 不存在，就把 (key, value) 加入这个桶。
#
# 拉链法的优点：
# 逻辑直观，冲突处理容易理解。
#
# 拉链法的缺点：
# 如果很多 key 被分到同一个桶，这个桶会变长，查询和修改就会变慢。
#
# 平均复杂度：
# 哈希分布比较均匀时，get 和 set 平均是 O(1)。
