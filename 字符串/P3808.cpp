#include <bits/stdc++.h>
using namespace std;

class AhoCorasick {
private:
    struct Node {
        array<int, 26> next{};
        int fail = 0;
        int output = 0;
        int count = 0;
    };

    vector<Node> trie;

public:
    explicit AhoCorasick(int maxNodes) {
        trie.reserve(maxNodes);
        trie.emplace_back();
    }

    void insert(const string& s) {
        int node = 0;

        for (char ch : s) {
            int c = ch - 'a';

            if (trie[node].next[c] == 0) {
                trie[node].next[c] =
                    static_cast<int>(trie.size());

                trie.emplace_back();
            }

            node = trie[node].next[c];
        }

        // 相同字符串的不同编号需要分别统计
        trie[node].count++;
    }

    void buildFail() {
        vector<int> order;
        order.reserve(trie.size());

        // 根节点的儿子入队
        for (int c = 0; c < 26; c++) {
            int child = trie[0].next[c];

            if (child != 0) {
                order.push_back(child);
            }
        }

        for (size_t head = 0; head < order.size(); head++) {
            int node = order[head];
            int failNode = trie[node].fail;

            for (int c = 0; c < 26; c++) {
                int child = trie[node].next[c];

                if (child != 0) {
                    // 建立 child 的 fail 指针
                    trie[child].fail =
                        trie[failNode].next[c];

                    int target = trie[child].fail;

                    // output 指向 fail 链上最近的模式串节点
                    if (trie[target].count != 0) {
                        trie[child].output = target;
                    } else {
                        trie[child].output =
                            trie[target].output;
                    }

                    order.push_back(child);
                } else {
                    // 补全自动机转移
                    trie[node].next[c] =
                        trie[failNode].next[c];
                }
            }
        }
    }

    int query(const string& text) {
        int state = 0;
        int answer = 0;

        // seen[node] 表示该终止节点是否已经统计过
        vector<char> seen(trie.size(), false);

        for (char ch : text) {
            int c = ch - 'a';

            // 补全转移后，不需要 while 沿 fail 跳
            state = trie[state].next[c];

            int check;

            if (trie[state].count != 0) {
                check = state;
            } else {
                check = trie[state].output;
            }

            // 只检查当前节点和 output 链
            while (check != 0) {
                if (seen[check]) {
                    // 该节点第一次统计时，
                    // 它后面的 output 链也已经处理过
                    break;
                }

                answer += trie[check].count;
                seen[check] = true;

                check = trie[check].output;
            }
        }

        return answer;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<string> patterns(n);
    int totalLength = 0;

    for (string& pattern : patterns) {
        cin >> pattern;
        totalLength += static_cast<int>(pattern.size());
    }

    string text;
    cin >> text;

    AhoCorasick ac(totalLength + 1);

    for (const string& pattern : patterns) {
        ac.insert(pattern);
    }

    ac.buildFail();

    cout << ac.query(text) << '\n';

    return 0;
}