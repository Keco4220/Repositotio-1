def primo(N):
    divisores = True
    for i in range(2, N):
        if N%i == 0:
            divisores = False
            break
        return divisores 
    print(primo(10000000000000000000000000000000000000000000000000000000000000000000000000000000000))

