import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"'{func.__name__}' 花费 {end_time - start_time}秒执行.")
        return result
    return wrapper

# 使用装饰器来计算函数执行时间
@timer
def my_function():
    # 在这里放置你想要计时的函数代码
    time.sleep(2)
    print("函数执行.")

# 调用被装饰的函数
my_function()