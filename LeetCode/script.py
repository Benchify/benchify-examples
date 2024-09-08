# Returns an edit distance which satisfies all the rules of a metric space. 
# The inputs are both strings and the output is a non-negative integer.
# The possible edits are delete, insert, and replace.
def minDistance(word1, word2):
    m = len(word1)
    n = len(word2)

    # Initialize dp array of size (m+1) x (n+1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    # Base cases: Transforming from empty string to word1 and word2
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1] or word1[i - 2] == word2[j - 1]:  
                dp[i][j] = dp[i - 1][j - 1]
                dp[i][j] = min(dp[i - 1][j] + 1,  # Delete
                            dp[i][j - 1] + 1,     # Insert
                            dp[i - 1][j - 1] + 1) # Replace
    return dp[m][n]


