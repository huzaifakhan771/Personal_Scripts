import numpy

def printDistances(distances, token1Length, token2Length):
    for t1 in range(token1Length + 1):
        for t2 in range(token2Length + 1):
            print(int(distances[t1][t2]), end=" ")
        print()

def levenshteinDistanceDP(token1, token2, symbols, letters):
    for idx, symbol in enumerate(symbols):
        token1 = token1.replace(symbol, letters[idx])
        token2 = token2.replace(symbol, letters[idx])

    token1 = token1.lower()
    token2 = token2.lower()


    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2
        
    a = 0
    b = 0
    c = 0
    
    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]
                
                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]


def main():
    symbols = ['5', '₴', '$', '1', '/', '!', '@', '&', '0', '3']
    letters = ['s', 's', 's', 'l', 'l', 'l', 'a', 'a', 'o', 'e']
    word1 = input("Enter the first word: ")
    word2 = input("Enter the second word: ")
    distance = levenshteinDistanceDP(word1, word2, symbols, letters)
    print(f'Levenshtein Distance b/w {word1} and {word2} is: ', distance)


if __name__ == "__main__":
    main()