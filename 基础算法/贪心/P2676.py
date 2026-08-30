import sys

def main():
    input = sys.stdin.buffer.readline
    N,B = map(int, input().split())
    heights = []
    for _ in range(N):
        heights.append(int(input()))

    # 贪心策略：先用最高的牛
    heights.sort(reverse=True)

    total = 0
    for i in range(N):
        total += heights[i]
        if total >=B:
            sys.stdout.buffer.write(str(i+1).encode())
            break

if __name__ == '__main__':
    main()