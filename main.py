import os


def search_file(file_name):
    """
    在当前目录及其子目录中搜索指定的文件名，并返回文件的完整路径列表。

    参数：
    file_name：要搜索的文件名。

    返回值：
    如果找到指定的文件，则返回包含文件的完整路径的列表；
    如果未找到指定的文件，则返回空列表。
    """
    file_paths = []  # 用于存储找到的文件路径
    if len(file_name) == 0:
        return file_paths
    # 遍历当前目录及其子目录
    for root, dirs, files in os.walk('.'):
        # 遍历目录中的文件
        for file in files:
            # 如果文件名与指定的文件名相同
            if file_name in file:
                # 将文件的完整路径添加到列表中
                file_paths.append(os.path.join(root, file))
    return file_paths


while True:
    # 获取用户输入的文件名
    file_name = input("文件名称: ")
    # 调用search_file函数获取文件路径列表
    result = search_file(file_name)
    # 如果结果为空列表，输出文件未找到提示
    if len(result) == 0:
        print("文件不存在!")
    else:
        # 输出文件路径列表
        for path in result:
            print(path)
    result = []
    print("")
