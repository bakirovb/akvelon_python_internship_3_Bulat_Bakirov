def fibonacci(number: int) -> int:
    x = 1
    y = 0
    for i in range(0, number):
        x += y
        y = x - y
    return y


print(fibonacci(0))         # 0
print(fibonacci(7))         # 13
print(fibonacci(17))        # 1597
