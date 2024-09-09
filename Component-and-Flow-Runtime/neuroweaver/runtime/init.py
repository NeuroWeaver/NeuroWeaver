import pickle


param = [1., 5.] # initial value for parameter
Flag = False
X = []
Y = []


with open('param', 'wb') as f:
    pickle.dump(param, f)

with open('Flag', 'wb') as f:
    pickle.dump(Flag, f)

with open('X', 'wb') as f:
    pickle.dump(X, f)

with open('Y', 'wb') as f:
    pickle.dump(Y, f)


with open('param', 'rb') as f:
    p = pickle.load(f)
    print(p)

with open('Flag', 'rb') as f:
    flag = pickle.load(f)
    print(flag)

with open('X', 'rb') as f:
    x = pickle.load(f)
    print(x)

with open('Y', 'rb') as f:
    y = pickle.load(f)
    print(y)
