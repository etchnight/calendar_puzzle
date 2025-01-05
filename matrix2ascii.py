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
# 1 适合在md浏览器中查看
# 2 显示数字，用于测试
def matrix2ascii(matrix, asciiType=0):
    ascii = ""
    for i in range(matrix.__len__() + 1):
        ascii += "\n"
        for j in range(matrix[0].__len__() + 1):
            ascii = ascii + getNodes(matrix, i, j, asciiType)
    if asciiType == 1:
        ascii = "\n```\n" + ascii + "\n```\n\n"
    return ascii


if __name__ == "__main__":
    # 测试
    matrix = [
        [4, 3, 3, 9, 9, 0, 0],
        [4, 3, 3, 2, 9, 9, 0],
        [4, 3, 0, 2, 2, 2, 2],
        [1, 6, 6, 6, 7, 5, 5],
        [1, 1, 1, 6, 7, 0, 5],
        [0, 0, 0, 0, 7, 5, 5],
    ]
    ascii = matrix2ascii(matrix, 2)
    print(ascii)
    with open("temp.md", "w+", encoding="utf-8") as f:
        f.write(ascii)
