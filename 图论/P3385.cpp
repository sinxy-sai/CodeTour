#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Edge {
    int to;
    int weight;
};


bool hasNegativeCycle(
    int n,
    const vector<vector<Edge>>& graph
) {
    const int64 INF = 4e18;

    // dist[i]：从顶点 1 到 i 的当前最短距离
    vector<int64> dist(n + 1, INF);

    // depth[i]：当前路径经过的边数
    vector<int> depth(n + 1, 0);

    // inQueue[i]：顶点 i 是否已经在队列中
    vector<bool> inQueue(n + 1, false);

    queue<int> que;

    dist[1] = 0;
    que.push(1);
    inQueue[1] = true;

    while (!que.empty()) {
        int u = que.front();
        que.pop();

        inQueue[u] = false;

        for (const Edge& edge : graph[u]) {
            int v = edge.to;
            int64 weight = edge.weight;

            if (dist[v] <= dist[u] + weight) {
                continue;
            }

            // 松弛
            dist[v] = dist[u] + weight;
            depth[v] = depth[u] + 1;

            // n 个点的路径经过 n 条边，
            // 必然重复经过某个点
            if (depth[v] >= n) {
                return true;
            }

            if (!inQueue[v]) {
                que.push(v);
                inQueue[v] = true;
            }
        }
    }

    return false;
}


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, m;
        cin >> n >> m;

        vector<vector<Edge>> graph(n + 1);

        for (int i = 0; i < m; ++i) {
            int u, v, w;
            cin >> u >> v >> w;

            // 添加 u -> v
            graph[u].push_back({v, w});

            // 非负边权还要添加 v -> u
            if (w >= 0) {
                graph[v].push_back({u, w});
            }
        }

        if (hasNegativeCycle(n, graph)) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}