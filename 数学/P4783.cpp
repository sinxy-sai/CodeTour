#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

const int64 MOD = 1000000007LL;

// 快速幂：计算 a^b mod MOD
int64 mod_pow(int64 a, int64 b)
{
    int64 result = 1;

    while (b > 0)
    {
        if (b & 1)
        {
            result = result * a % MOD;
        }

        a = a * a % MOD;
        b >>= 1;
    }

    return result;
}

// 求矩阵的逆矩阵
bool matrix_inverse(
    vector<vector<int64>> &matrix,
    int n)
{
    // 构造增广矩阵 [A | I]
    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            matrix[i].push_back(i == j ? 1 : 0);
        }
    }

    for (int col = 0; col < n; ++col)
    {
        // 寻找非零主元
        int pivot_row = -1;

        for (int row = col; row < n; ++row)
        {
            if (matrix[row][col] != 0)
            {
                pivot_row = row;
                break;
            }
        }

        // 找不到主元，矩阵不可逆
        if (pivot_row == -1)
        {
            return false;
        }

        // 交换主元行
        swap(matrix[col], matrix[pivot_row]);

        // 求主元的模逆元
        int64 pivot = matrix[col][col];
        int64 inverse_pivot = mod_pow(pivot, MOD - 2);

        // 将主元化为 1
        for (int j = col; j < 2 * n; ++j)
        {
            matrix[col][j] =
                matrix[col][j] * inverse_pivot % MOD;
        }

        // 消去其他行当前列的元素
        for (int row = 0; row < n; ++row)
        {
            if (row == col)
            {
                continue;
            }

            int64 factor = matrix[row][col];

            if (factor == 0)
            {
                continue;
            }

            for (int j = col; j < 2 * n; ++j)
            {
                int64 subtract =
                    factor * matrix[col][j] % MOD;

                matrix[row][j] -= subtract;

                if (matrix[row][j] < 0)
                {
                    matrix[row][j] += MOD;
                }
            }
        }
    }

    return true;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<vector<int64>> matrix(n);

    for (int i = 0; i < n; ++i)
    {
        matrix[i].resize(n);

        for (int j = 0; j < n; ++j)
        {
            cin >> matrix[i][j];
            matrix[i][j] %= MOD;
        }
    }

    if (!matrix_inverse(matrix, n))
    {
        cout << "No Solution\n";
        return 0;
    }

    // 输出增广矩阵右半部分
    for (int i = 0; i < n; ++i)
    {
        for (int j = n; j < 2 * n; ++j)
        {
            if (j > n)
            {
                cout << ' ';
            }

            cout << matrix[i][j];
        }

        cout << '\n';
    }

    return 0;
}