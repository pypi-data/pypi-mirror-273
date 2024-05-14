# %%
import json
import functools


class FunctionLogger:
    def __init__(self):
        self.indent_level = 0

    def log_function_call(self, func):
        def wrapper(*args, **kwargs):
            # 获取函数参数名称
            parameter_names = func.__code__.co_varnames

            # 构建参数字典，将参数名和对应值关联起来
            parameters = dict(zip(parameter_names, args))
            parameters.update(kwargs)

            # 打印函数名和输入参数，带有缩进
            print(
                f"""{'  ' * self.indent_level}调用函数 {func.__name__}，输入参数: {parameters}"""
            )

            # 增加缩进级别
            self.indent_level += 1

            # 调用原始函数并获取输出结果
            result = func(*args, **kwargs)

            # 减少缩进级别
            self.indent_level -= 1

            # 打印输出结果，带有缩进
            print(f"{'  ' * self.indent_level}函数 {func.__name__} 的输出结果: {result}")

            return result

        return wrapper


# 创建 FunctionLogger 实例


if __name__ == "__main__":
    funclogger = FunctionLogger()

    # 使用装饰器
    # @funclogger.log_function_call
    def add(a, b):
        return a + b

    @funclogger.log_function_call
    def multiply(x, y):
        return x * y

    @funclogger.log_function_call
    def square_and_add(x, y):
        squared_x = x**2
        return add(squared_x, y)

    # 测试
    result_square_and_add = square_and_add(2, 3)

# %%
