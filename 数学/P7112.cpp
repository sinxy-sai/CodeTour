#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

int64 determinant(vector<vector<int64>> &matrix, int n, int64 mod)
{
    int64 sign = 1;

    for (int col = 0; col < n; ++col)
    {
        for (int row = col + 1; row < n; ++row)
        {
            // 使用类似辗转相除法的方式消元
            while (matrix[col][col] != 0)
            {
                int64 pivot = matrix[col][col];
                int64 value = matrix[row][col];

                // 带余除法中的商
                int64 quotient = value / pivot;

                for (int k = col; k < n; ++k)
                {
                    matrix[row][k] =
                        (matrix[row][k] - quotient * matrix[col][k]) % mod;

                    // C++ 中负数取模结果可能为负数
                    if (matrix[row][k] < 0)
                    {
                        matrix[row][k] += mod;
                    }
                }

                // 交换两行
                swap(matrix[col], matrix[row]);

                // 交换两行，行列式变号
                sign = -sign;
            }

            // 主元变成 0 后，再交换回来
            swap(matrix[col], matrix[row]);
            sign = -sign;
        }
    }

    // 计算 sign 对 mod 的结果
    int64 answer = sign % mod;

    if (answer < 0)
    {
        answer += mod;
    }

    // 上三角矩阵的行列式等于主对角线乘积
    for (int i = 0; i < n; ++i)
    {
        answer = answer * matrix[i][i] % mod;
    }

    return answer;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    int64 p;

    cin >> n >> p;

    vector<vector<int64>> matrix(
        n,
        vector<int64>(n));

    for (int i = 0; i < n; ++i)
    {
        for (int j = 0; j < n; ++j)
        {
            cin >> matrix[i][j];
            matrix[i][j] %= p;
        }
    }

    cout << determinant(matrix, n, p) << '\n';

    return 0;
}