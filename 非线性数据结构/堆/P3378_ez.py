# 堆 / 优先队列
import sys
import heapq

def main():
    n = int(sys.stdin.buffer.readline())

    heap = []
    out = []    
    
    for _ in range(n):
        op = sys.stdin.buffer.readline().split()

        if op[0] == b'1':
            x = int(op[1])
            heapq.heappush(heap,x)

        elif op[0] == b'2':
            out.append(str(heap[0]))

        elif op[0] == b'3':
            heapq.heappop(heap)

    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()