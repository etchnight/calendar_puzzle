# 获取矩阵的某个元素
def getCell(matrix, i, j):
    if i >= matrix.__len__() or i < 0:
        return 0
    if j >= matrix[i].__len__() or j < 0:
        return 0
    return matrix[i][j]


# 初始化ascii制表符号矩阵
def initAscii():
    text = [
        [
            [[[], []], [[], []]],
            [[[], []], [[], []]],
        ],
        [
            [[[], []], [[], []]],
            [[[], []], [[], []]],
        ],
    ]
    text[0][0][0][0] = "   "

    text[1][0][0][0] = " ╹ "
    text[0][1][0][0] = "━╸ "
    text[0][0][1][0] = " ╻ "
    text[0][0][0][1] = " ╺━"

    text[1][1][0][0] = "━┛ "
    text[1][0][1][0] = " ┃ "
    text[1][0][0][1] = " ┗━"
    text[0][1][1][0] = "━┓ "
    text[0][1][0][1] = "━━━"
    text[0][0][1][1] = " ┏━"

    text[0][1][1][1] = "━┳━"
    text[1][0][1][1] = " ┣━"
    text[1][1][0][1] = "━┻━"
    text[1][1][1][0] = "━┫ "

    text[1][1][1][1] = "━╋━"
    return text


# 左上为节点编号
def getNodes(matrix, i, j, asciiType=0):
    # 上左下右
    list = []

    def push(r, c, m, n):
        if getCell(matrix, r, c) - getCell(matrix, m, n) != 0:
            list.append(1)
        else:
            list.append(0)

    push(i - 1, j - 1, i - 1, j)  # 上
    push(i - 1, j - 1, i, j - 1)  # 左
    push(i, j - 1, i, j)  # 下
    push(i - 1, j, i, j)  # 右
    asciiMatrix = initAscii()
    text = asciiMatrix[list[0]][list[1]][list[2]][list[3]]
    if asciiType == 0:
        return text
    elif asciiType == 1:
        return text.replace(" ", "■")
    elif asciiType == 2:
        num = getCell(matrix, i, j)
        outNum = str(num) if num >= 10 else "0" + str(num)
        return text + outNum


# asciiType
# 0 适合在IDE中查看
# 1 适合在md浏览器中查看(gitee)
# 2 显示数字，用于测试
def matrix2ascii(matrix, asciiType=0):
    ascii = ""
    for i in range(matrix.__len__() + 1):
        ascii += "\n"
        for j in range(matrix[0].__len__() + 1):
            ascii = ascii + getNodes(matrix, i, j, asciiType)
    if asciiType == 1:
        ascii = "\n```\n" + ascii + "\n```\n\n"
    result=''
    for line in ascii.splitlines():
            line = line + "\n"+asciiNextLine(line)
            result = result + line
    return result


# 优化gitee显示，补丁方案
def asciiNextLine(line):
    result = ""
    for char in line:
        if char in ["╻", "┃", "┓", "┏", "┳", "┣", "┫", "╋"]:
            result = result + "┃"
        elif char in ["╹", "╸","╺", "┛", "┗", "┻", "■","━"]:
            result = result + "■"
    return result + "\n"

def test(filePath):
    # 测试
    matrix = [
        [4, 3, 3, 9, 9, 0, 0],
        [4, 3, 3, 2, 9, 9, 0],
        [4, 3, 0, 2, 2, 2, 2],
        [1, 6, 6, 6, 7, 5, 5],
        [1, 1, 1, 6, 7, 0, 5],
        [0, 0, 0, 0, 7, 5, 5],
    ]
    ascii = matrix2ascii(matrix, 1)
    print(ascii)
    with open(filePath, "w+", encoding="utf-8") as f:
        f.write(ascii)


def tempPatch(filePath):
    with open(filePath, "r", encoding="utf-8") as f:
        content = f.read().splitlines()
    with open(filePath, "w+", encoding="utf-8") as f:
        result=''
        for line in content:
            line = line + "\n"+asciiNextLine(line)
            result = result + line
        f.write(result)

def tempPatchs():
    import os
    # 指定文件夹路径
    folder_path = '已完成结果/2025'

    # 获取文件夹下的所有文件和文件夹名称
    entries = os.listdir(folder_path)

    # 遍历并打印文件夹下的所有文件
    for entry in entries:
        # 获取完整的文件路径
        full_path = os.path.join(folder_path, entry)
        # 检查是否为文件
        if os.path.isfile(full_path):
            tempPatch(full_path)
            print(full_path)



if __name__ == "__main__":
    #tempPatchs()
    filePath = "temp.md"
    test(filePath)
    #tempPatch("temp.md")



