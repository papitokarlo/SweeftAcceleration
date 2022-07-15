""" 
    Lexicographical order is often known as alphabetical order when dealing with strings. 
    A string is greater than another string
    if it comes later in a lexicographically sorted list.
"""

ran = int(input("enter number of words :"))
for _ in range(ran):
    s = input()
    s = list(s[::-1])
    done = 0
    for i in range(1,len(s)):
        if s[i-1] > s[i]:
            for j in range(i):
                if s[j] > s[i]:
                    s[j],s[i] = s[i],s[j]
                    s = sorted(s[:i])[::-1] + s[i:]
                    print("".join(s[::-1]))
                    break
            break
    else:
            print("no answer")
