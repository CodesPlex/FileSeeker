import os
import concurrent.futures


def search_file_recursive(root, file_name):
    """
    递归地在指定目录及其子目录中搜索指定的文件名，并返回文件的完整路径列表。

    参数：
    root：要搜索的目录路径。
    file_name：要搜索的文件名（不区分大小写）。

    返回值：
    包含找到的文件的完整路径的列表。
    """
    file_paths = []
    # 遍历目录中的文件和子目录
    for item in os.listdir(root):
        item_path = os.path.join(root, item)
        # 如果是文件，则检查是否匹配
        if os.path.isfile(item_path) and file_name.lower() in item.lower():
            file_paths.append(item_path)
            # 如果是目录，则递归搜索
        elif os.path.isdir(item_path):
            file_paths.extend(search_file_recursive(item_path, file_name))
    return file_paths


def search_file(file_name):
    """
    在当前目录及其子目录中并发搜索指定的文件名，并返回文件的完整路径列表（无重复项）。

    参数：
    file_name：要搜索的文件名。

    返回值：
    包含找到的文件的完整路径的列表（无重复项）。
    """
    if not file_name:
        return []

        # 获取当前目录的所有子目录
    dirs = next(os.walk('.'))[1]

    # 使用线程池并发搜索文件
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(dirs)) as executor:
        futures = [executor.submit(search_file_recursive, os.path.join('.', dir_name), file_name)
                   for dir_name in dirs]

        # 使用集合存储唯一的文件路径
        unique_file_paths = set()

        # 遍历所有子目录的搜索结果
        for future in concurrent.futures.as_completed(futures):
            try:
                # 获取搜索结果并添加到集合中，自动去重
                unique_file_paths.update(future.result())
            except Exception as exc:
                print(f'在搜索时发生错误: {exc}')

                # 搜索当前目录（不包括子目录），并添加到集合中
    unique_file_paths.update(search_file_recursive('.', file_name))

    # 将集合转换为列表并返回
    return list(unique_file_paths)


while True:
    # 获取用户输入的文件名
    file_name = input("文件名称: ")
    # 调用search_file函数获取文件路径列表
    result = search_file(file_name)
    # 如果结果为空列表，输出文件未找到提示
    if not result:
        print("文件不存在!")
    else:
        # 输出文件路径列表
        for path in result:
            print(path)
    print("")
