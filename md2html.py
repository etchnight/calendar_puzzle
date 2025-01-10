import os


def md2html(month, day, weekday, isweek):
    def num2str(num):
        if num < 10:
            return "0" + str(num)
        else:
            return str(num)

    dirname = "./已完成结果/2025"
    if isweek:
        mdname = "{}月{}日星期{}-完成".format(num2str(month), num2str(day), weekday)
    else:
        mdname = "{}月{}日-完成".format(num2str(month), num2str(day))
    outputName = "./html/2025/{}.html".format(mdname)
    os.path.isfile("./已完成结果/2025/01月01日星期3-完成.md")

    def getClass(char):
        charList = [
            # 左上右上左下右下 right left top bottom space
            {"char": "■╻■", "className": ["s", "s", "r", "l"]},
            {"char": "■┃■", "className": ["r", "l", "r", "l"]},
            {"char": "━┓■", "className": ["b", "s", "t r", "l"]},
            {"char": "■┏━", "className": ["s", "b", "r", "l t"]},
            {"char": "━┳━", "className": ["b", "b", "t r", "t l"]},
            {"char": "■┣━", "className": ["r", "l b", "r", "l t"]},
            {"char": "━┫■", "className": ["r b", "l", "r t", "l"]},
            {"char": "━╋━", "className": ["r b", "l b", "r t", "l t"]},
            {"char": "■╹■", "className": ["r", "l", "s", "s"]},
            {"char": "━╸■", "className": ["b", "s", "t", "s"]},
            {"char": "■╺━", "className": ["s", "b", "s", "t"]},
            {"char": "━┛■", "className": ["r b", "l", "t", "s"]},
            {"char": "■┗━", "className": ["r", "l b", "s", "t"]},
            {"char": "━┻━", "className": ["r b", "l b", "t", "t"]},
            {"char": "■■■", "className": ["s", "s", "s", "s"]},
            {"char": "━━━", "className": ["b", "b", "t", "t"]},
        ]
        for item in charList:
            if item["char"] == char:
                return item["className"]
        return False

    def getStyle(className):
        style = ""
        for c in className:
            if c == "r":
                style += "border-right: 1px solid black;"
            elif c == "l":
                style += "border-left: 1px solid black;"
            elif c == "t":
                style += "border-top: 1px solid black;"
            elif c == "b":
                style += "border-bottom: 1px solid black;"
            elif c == "s":
                style += "border: 1px solid black;"
        return style

    with open(dirname + "/" + mdname + ".md", "r", encoding="utf-8") as inputFile:
        with open((outputName), "w+", encoding="utf-8") as output:
            line = inputFile.readline()
            isTable = False
            while line:
                if line == "":
                    line = inputFile.readline()
                    continue
                if line.startswith("```"):
                    isTable = not isTable
                    if isTable:
                        output.write("<table>\n")
                        isLine = False
                    else:
                        output.write("</table>\n")
                    line = inputFile.readline()
                    continue
                if isTable:
                    if line == "\n":
                        line = inputFile.readline()
                        continue
                    # 隔一行写入一行
                    isLine = not isLine
                    if not isLine:
                        line = inputFile.readline()
                        continue
                    # line = line[1 : len(line) - 2]
                    htmlLine1 = []
                    htmlLine2 = []
                    groups = [line[i : i + 3] for i in range(0, len(line), 3)]
                    borders = [getClass(groups[i]) for i in range(len(groups))]
                    i = -1
                    for border in borders:
                        i += 1
                        if not border:
                            continue
                        print(groups[i], border)
                        htmlLine1.append('<td class="{}"></td>'.format(getStyle(border[0])))
                        htmlLine1.append('<td class="{}"></td>'.format(getStyle(border[1])))
                        htmlLine2.append('<td class="{}"></td>'.format(getStyle(border[2])))
                        htmlLine2.append('<td class="{}"></td>'.format(getStyle(border[3])))
                    output.write("<tr>\n")
                    output.write("".join(htmlLine1))
                    output.write("</tr>\n<tr>\n")
                    output.write("".join(htmlLine2))
                    output.write("</tr>\n")
                line = inputFile.readline()
            output.close()
        inputFile.close()


if __name__ == "__main__":
    md2html(1, 1, 3, True)
