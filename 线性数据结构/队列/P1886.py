# 单调队列/滑动窗口
import sys
from collections import deque

def main():
    n,k = map(int,sys.stdin.buffer.readline().split())
    data = list(map(int,sys.stdin.buffer.readline().split()))

    min_q = deque()
    max_q = deque()

    min_ans = []
    max_ans = []

    for i,x in enumerate(data):

        # 维护最小值队列，队头最小，单调递增队列
        while min_q and data[min_q[-1]] >= x:
            min_q.pop()
        min_q.append(i)

        # 维护最大值队列，队头最大，单调递减队列
        while max_q and data[max_q[-1]] <= x:
            max_q.pop()
        max_q.append(i)

        # 删掉已经滑出窗口的下标
        left = i - k + 1
        if min_q[0] < left:
            min_q.popleft()
        if max_q[0] < left:
            max_q.popleft()

         # 当窗口长度达到 k 时，记录答案
        if i >= k-1:
            min_ans.append(str(data[min_q[0]]))
            max_ans.append(str(data[max_q[0]]))

    sys.stdout.write(' '.join(min_ans) + '\n' + ' '.join(max_ans))

if __name__ == '__main__':
    main()