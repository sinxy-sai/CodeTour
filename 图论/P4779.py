# 单源最短路径(标准版)
import sys
import heapq

def main():
    input = sys.stdin.buffer.readline
    n,m,s = map(int,input().split())

    graph = [[] for _ in range(n+1)]
    
    for _ in range(m):
        u,v,w = map(int,input().split())
        graph[u].append((v,w))

    INF = 2**31-1   
    dist = [INF]*(n+1)
    dist[s] = 0

    heap = [(0,s)]
    while heap:
        current_dist,u = heapq.heappop(heap)

        if current_dist != dist[u]:
            continue

        for v,w in graph[u]:
            new_dist = current_dist + w

            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap,(new_dist,v))

    sys.stdout.write(' '.join(map(str,dist[1:])))

if __name__ == '__main__':
    main()