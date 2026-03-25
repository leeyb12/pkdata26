class Arrays:
    def __new__(cls):
        print("new 연산자") 
        return super().__new__(cls)
    
    def __init__(self):
        print("초기화됨")
a = Arrays()
print(a)