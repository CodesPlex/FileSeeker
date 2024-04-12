import os
import concurrent.futures


def search_file_in_dir(root, file_name):
    """
    在指定目录中搜索指定的文件名，并返回文件的完整路径列表。

    参数：
    root：要搜索的目录路径。
    file_name：要搜索的文件名。

    返回值：
    包含找到的文件的完整路径的列表。
    """
    file_paths = []
    # 遍历目录中的文件
    for file in os.listdir(root):
        # 如果文件名与指定的文件名相同或包含指定文件名
        if file_name.lower() in file.lower():
            # 将文件的完整路径添加到列表中
            file_paths.append(os.path.join(root, file))
    return file_paths


def search_file(file_name):
    """
    在当前目录及其子目录中并发搜索指定的文件名，并返回文件的完整路径列表。

    参数：
    file_name：要搜索的文件名。

    返回值：
    包含找到的文件的完整路径的列表。
    """
    file_paths = []
    if not file_name:
        return file_paths

        # 获取当前目录的所有子目录
    dirs = next(os.walk('.'))[1]

    # 使用线程池并发搜索文件
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(dirs)) as executor:
        futures = {executor.submit(search_file_in_dir, os.path.join('.', dir_name), file_name): dir_name
                   for dir_name in dirs}

        # 遍历所有子目录的搜索结果
        for future in concurrent.futures.as_completed(futures):
            dir_name = futures[future]
            try:
                # 获取搜索结果并添加到总列表
                file_paths.extend(future.result())
            except Exception as exc:
                print(f'在目录 {dir_name} 中搜索时发生错误: {exc}')

    return file_paths


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