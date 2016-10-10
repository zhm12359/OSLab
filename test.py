def numSquares(n):
    """
    :type n: int
    :rtype: int
    """
    ans = [x for x in range(0,n+1)]

    perfects = [ x*x for x in range(1, n/2+1) ]

    ans[0] =1
    ans[1] =1

    for i in range(2, n+1):
        #if ans[i] != i: continue
        m = 1
        while m*i*i <= n:
            ans[m*i*i] = min (ans[m*i*i],m)
            m += 1
        ans[i] = min(ans[i], ans[i-1] + 1)

        for a in range(0, int(i**0.5)):
            s = a*a
            difference = i - s
            if difference > 0:
                ans[i] = min(ans[i], ans[s] + ans[difference])

        #print("when i is", i, "modified ans into", ans)

    return ans[n]

print(numSquares(800))
