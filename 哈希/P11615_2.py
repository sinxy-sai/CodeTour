# 手写哈希表模板 开放寻址法
import sys

class OpenAddressHashMap:
    def __init__(self,size):
        self.size = size
        self.keys = [0] * size
        self.values = [0] * size
        self.used = [False] * size

    def hash(self,key):
        return key % self.size

    def find_slot(self,key):
        pos = self.hash(key)
        while self.used[pos]:
            if self.keys[pos] == key:
                return pos
            pos = (pos + 1) % self.size

        return pos


    def set(self,key,value):
        pos = self.find_slot(key)
        if not self.used[pos]:
            self.keys[pos] = key
            self.used[pos] = True

        self.values[pos] = value

    def get(self,key):
        pos = self.find_slot(key)
        if self.used[pos]:
            return self.values[pos]
        return 0

def main():
    n = int(sys.stdin.readline())

    mp = OpenAddressHashMap(n * 4)
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


# 思路说明：开放寻址法哈希表
#
# 题目要维护一个映射 f(x)。
# 每次操作给出 x 和 y，需要先查询旧值，再更新新值：
#
#     old = mp.get(x)
#     ans += i * old
#     mp.set(x, y)
#
# 这里没有直接用 Python 内置 dict，而是自己实现哈希表。
#
# 开放寻址法的核心：
#
#     pos = hash(key)
#
# 先通过哈希函数把 key 映射到数组中的一个位置。
# 如果这个位置已经被占用，而且存的不是当前 key，就继续往后找：
#
#     pos = (pos + 1) % size
#
# 直到找到这个 key，或者找到一个空位置。
#
# 在本程序中：
#
#     keys[pos]    记录这个位置存的 key
#     values[pos]  记录这个 key 对应的 value
#     used[pos]    记录这个位置是否已经被使用
#
# 为什么需要 used：
# 题目允许 x = 0，而 keys 数组初始值也是 0。
# 所以不能用 keys[pos] == 0 判断这个位置是否为空。
# 必须单独用 used[pos] 记录当前位置有没有被占用。
#
# find_slot(key) 的作用：
#
# 1. 从 hash(key) 得到的初始位置开始找。
# 2. 如果当前位置已经被使用，并且 key 相同，就返回这个位置。
# 3. 如果当前位置已经被使用，但 key 不同，就继续向后找。
# 4. 如果遇到空位置，也返回这个位置。
#
# 查询 get(key)：
#
# 1. 用 find_slot(key) 找到 key 应该在的位置。
# 2. 如果这个位置已经使用，说明 key 存在，返回 values[pos]。
# 3. 如果这个位置没使用，说明 key 不存在，返回初始值 0。
#
# 修改 set(key, value)：
#
# 1. 用 find_slot(key) 找到 key 应该在的位置。
# 2. 如果是新位置，先标记 used[pos] = True，并记录 keys[pos] = key。
# 3. 再把 values[pos] 更新为 value。
#
# 开放寻址法的优点：
# 数据都存在连续数组里，常数小，C++ 中通常很快。
#
# 开放寻址法的缺点：
# 表不能太满；如果冲突很多，连续探测会变长，性能会下降。
# 所以一般会开比数据量更大的数组，例如本程序中使用 n * 4。
#
# 平均复杂度：
# 哈希分布比较均匀、表比较空时，get 和 set 平均是 O(1)。
