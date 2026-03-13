import sys
args = sys.argv
name = args[1]
age = args[2]
with open('./test_note.txt', 'a') as f:
    f.write(name + " " + age + "\n")
print("입력되었습니다.")