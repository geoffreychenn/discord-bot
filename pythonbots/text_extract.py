import re

file = open("../questions.txt")
questions = file.read().splitlines()
file.close()


for q in questions:
    print(q)
    s1 = q.split('?')[0] + '?'
    with open("../questions1.txt", "a") as the_file:
        the_file.write(s1+"\n")

print(s1)
