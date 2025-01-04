import os
from ortools.sat.python import cp_model
import datetime
from matrix2ascii import matrix2ascii

# 以下参数会算至年底
isLeapYear = 0  # 是否闰年
isWeek = True  # 是否带星期

year = 2025  # 仅作为输出使用
startMonth = 1  # 第一天是几月
startDay = 1  # 第一天是几号
startWeekday = 3  # 第一天是星期几

maxSolNum = 10  # 最大解数量

startTime = datetime.datetime.now()


def solve(day, month, weekday, isWeek, maxSolNum, outfileName):
    # 参数
    num_col = 7  # 列数
    if isWeek:
        num_row = 8  # 行数
        num_pieces = 47  # 总方块数
        num_group = [5, 5, 5, 5, 5, 5, 5, 4, 4, 4]  # 拼图块含有的方块数集合
        # num_piece = 5  # 每片拼图包含的方块数（最大值）
    else:
        num_row = 7
        num_pieces = 41  # 5+5+5+5+6+5+5+5
        num_group = [5, 5, 5, 5, 5, 5, 4, 6]  # 拼图块含有的方块数集合
        # num_piece = 6

    model = cp_model.CpModel()
    work = {}
    # 创建【总方块数，拼图块排布形态，行号，列号】的四维0-1数组
    for p in range(num_pieces):
        for s in range(8):
            for r in range(num_row):
                for c in range(num_col):
                    work[p, s, r, c] = model.NewBoolVar(
                        "work_%i_%i_%i_%i" % (p, s, r, c)
                    )

    # 每个行号、列号只有一个方块(个别位置没有)
    def addRowColConstraint(r, c):
        model.Add(
            sum(work[p, s, r, c] for p in range(num_pieces) for s in range(8)) == 0
        )

    def addRowColConstraints():
        rowDay = int((day - 1) / 7) + 2
        colDay = (day - 1) % 7
        rowMonth = int((month - 1) / 6)
        colMonth = (month - 1) % 6
        rowWeek = int(weekday / 4) + 6
        colWeek = weekday % 4 + 3 + rowWeek - 6
        # print(rowWeek, colWeek)
        for r in range(num_row):
            for c in range(num_col):
                if (
                    (r == 0 and c == 6)
                    or (r == 1 and c == 6)
                    or (r == 6 and c > 2 and (not isWeek))
                    or (r == 7 and c < 4 and isWeek)
                ):
                    """不可选择的位置"""
                    addRowColConstraint(r, c)
                # 输入条件
                elif r == rowDay and c == colDay:
                    addRowColConstraint(r, c)
                elif r == rowMonth and c == colMonth:
                    addRowColConstraint(r, c)
                elif r == rowWeek and c == colWeek:
                    addRowColConstraint(r, c)
                else:
                    model.Add(
                        sum(
                            work[p, s, r, c]
                            for p in range(num_pieces)
                            for s in range(8)
                        )
                        == 1
                    )

    addRowColConstraints()
    # 每个方块只有1个行号、列号、形态（含不可选择的方块号）
    for p in range(num_pieces):
        model.Add(
            sum(
                work[p, s, r, c]
                for r in range(num_row)
                for c in range(num_col)
                for s in range(8)
            )
            == 1
        )

    # 每种型号的所有方块的形态号统一
    # 即第i到j个方块的形态号相同，对每种形态s,其所有位置上的方块数总和，满足以下条件
    # 要么等于0（未使用该形态），要么等于拼图块的方块数。
    def addSLimit():
        startP = 0
        for num in num_group:
            for s in range(8):
                model.Add(
                    sum(
                        work[p, s, r, c]
                        for p in range(startP, startP + num)
                        for r in range(num_row)
                        for c in range(num_col)
                    )
                    <= num
                )
                for i in range(1, num):
                    model.Add(
                        sum(
                            work[p, s, r, c]
                            for p in range(startP, startP + num)
                            for r in range(num_row)
                            for c in range(num_col)
                        )
                        != i
                    )
            startP += num

    addSLimit()

    """不要求日期时使用  TODO"""

    # 拼图块内距离约束
    def addDistance(di, dj, pnum, pnum2):
        """
        nnum：源方块序号
        nnum2：目标方块序号
        """
        d = [di, dj]
        for r in range(num_row):
            for c in range(num_col):
                s = 0
                for i in [1, -1]:
                    for j in [1, -1]:
                        for k in [0, 1]:
                            row = r + i * d[k]
                            col = c + j * d[1 - k]
                            if (
                                row < num_row
                                and col < num_col
                                and row >= 0
                                and col >= 0
                            ):
                                model.Add(
                                    (
                                        work[pnum, s, r, c] + work[pnum2, s, row, col]
                                        != 1
                                    )
                                )
                            else:
                                # 该形态不能出现在该位置
                                model.Add(work[pnum, s, r, c] == 0)
                            s = s + 1

    def addDistances():
        # 禁用形态
        """
        0:原始
        1:逆时针旋转90后左右翻转（左下右上45°翻转）
        2:左右翻转-
        3:逆时针旋转90
        4:上下翻转
        5:顺时针旋转90-
        6:旋转180-
        7:顺时针旋转90后左右翻转（左上右下45°翻转）-
        """

        # 0号拼图(两种都有)
        """
        0 1 2
        3 4
        """
        addDistance(1, 1, 0, 4)
        addDistance(1, 0, 0, 3)
        addDistance(0, 2, 0, 2)
        addDistance(0, 1, 0, 1)
        # 1号拼图（两种都有）
        """
        5
        6
        7 8 9
        """
        addDistance(2, 2, 5, 9)
        addDistance(2, 1, 5, 8)
        addDistance(2, 0, 5, 7)
        addDistance(1, 0, 5, 6)
        for p in range(5, 10):
            model.Add(
                sum(work[p, 1, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 3, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 5, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 7, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
        # 2号拼图（两种都有）
        """
        10 11
        12
        13 14
        """
        addDistance(2, 2, 10, 14)
        addDistance(2, 1, 10, 13)
        addDistance(1, 1, 10, 12)
        addDistance(0, 1, 10, 11)
        for p in range(10, 15):
            model.Add(
                sum(work[p, 4, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 5, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 6, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 7, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
        # 3号拼图（两种都有）
        """
        15
        16
        17 18
        19
        """
        addDistance(3, 1, 15, 19)
        addDistance(2, 1, 15, 18)
        addDistance(2, 0, 15, 17)
        addDistance(1, 0, 15, 16)

        # 4号拼图（两种都有）
        """
        20
        21
        22
        23 24
        """
        addDistance(3, 1, 20, 24)
        addDistance(3, 0, 20, 23)
        addDistance(2, 0, 20, 22)
        addDistance(1, 0, 20, 21)
        # 5号拼图（两种都有）
        """
        25    26
        27 28 29
        """
        addDistance(1, 2, 25, 29)
        addDistance(1, 1, 25, 28)
        addDistance(1, 0, 25, 27)
        addDistance(0, 2, 25, 26)
        for p in range(25, 30):
            model.Add(
                sum(work[p, 2, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 5, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 6, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
            model.Add(
                sum(work[p, 7, r, c] for r in range(num_row) for c in range(num_col))
                == 0
            )
        if not isWeek:
            # 6号拼图
            """
            30
            31
            32 33
            34
            """
            addDistance(3, 0, 30, 34)
            addDistance(2, 1, 30, 33)
            addDistance(2, 0, 30, 32)
            addDistance(1, 0, 30, 31)
            # 7号拼图
            """
            35 36 37  
            38 39 40 
            """
            addDistance(1, 1, 35, 40)
            addDistance(1, 0, 35, 39)
            addDistance(0, 2, 35, 38)
            addDistance(0, 1, 35, 37)
            addDistance(1, 2, 35, 35)
            for p in range(35, 41):
                for s in range(2, 8):
                    model.Add(
                        sum(
                            work[p, s, r, c]
                            for r in range(num_row)
                            for c in range(num_col)
                        )
                        == 0
                    )
        else:
            # 6号拼图
            """
            30
            31 32 33
            34
            """
            addDistance(1, 2, 30, 34)
            addDistance(1, 1, 30, 33)
            addDistance(1, 0, 30, 32)
            addDistance(2, 0, 30, 31)
            for p in range(30, 35):
                model.Add(
                    sum(
                        work[p, 3, r, c] for r in range(num_row) for c in range(num_col)
                    )
                    == 0
                )
                model.Add(
                    sum(
                        work[p, 4, r, c] for r in range(num_row) for c in range(num_col)
                    )
                    == 0
                )
                model.Add(
                    sum(
                        work[p, 6, r, c] for r in range(num_row) for c in range(num_col)
                    )
                    == 0
                )
                model.Add(
                    sum(
                        work[p, 7, r, c] for r in range(num_row) for c in range(num_col)
                    )
                    == 0
                )

            # 7号拼图
            """
            35
            36
            37
            38
            """
            addDistance(3, 0, 35, 38)
            addDistance(2, 0, 35, 37)
            addDistance(1, 0, 35, 36)
            for p in range(35, 39):
                for s in range(2, 8):
                    model.Add(
                        sum(
                            work[p, s, r, c]
                            for r in range(num_row)
                            for c in range(num_col)
                        )
                        == 0
                    )

            # 8号拼图
            """
            39
            40
            41 42
            """
            addDistance(2, 1, 39, 42)
            addDistance(2, 0, 39, 41)
            addDistance(1, 0, 39, 40)

            # 9号拼图
            """
            43 44
            -- 45 46
            """
            addDistance(1, 2, 43, 46)
            addDistance(1, 1, 43, 45)
            addDistance(0, 1, 43, 44)
            for p in range(43, 47):
                for s in range(4, 8):
                    model.Add(
                        sum(
                            work[p, s, r, c]
                            for r in range(num_row)
                            for c in range(num_col)
                        )
                        == 0
                    )

    addDistances()
    # 求解
    solver = cp_model.CpSolver()
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True

    # solver.parameters.num_search_workers = 4
    # solver.parameters.interleave_search = False
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        """Print intermediate solutions."""

        def __init__(self, variables, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0
            self.__solution_limit = limit

        def on_solution_callback(self):
            self.__solution_count += 1
            print方案 = "第%i种方案：\n" % self.__solution_count
            print(print方案)
            endTime = datetime.datetime.now()
            # 输出结果到文件
            matrix = []
            for r in range(num_row):
                matrix.append([])
                for c in range(num_col):
                    matrix[r].append([])
                    isprint = False
                    p = -1
                    for index in range(num_group.__len__()):
                        num = num_group[index]
                        for i in range(num):
                            p += 1
                            # 计算所在方块
                            for s in range(8):
                                if self.BooleanValue(self.__variables[p, s, r, c]):
                                    isprint = True
                                    matrix[r][c] = index + 1
                                    # print(p, end=" ")调试用
                    if not isprint:
                        matrix[r][c] = 0

            ascii = matrix2ascii(matrix, 1)
            ascii2 = matrix2ascii(matrix, 2)
            print(ascii2)
            with open(outfileName, "a+", encoding="utf-8") as f:
                f.write(print方案)
                f.write(ascii)
                f.close()
            print(endTime - startTime)
            print()
            with open("print.log", "a+", encoding="utf-8") as f2:
                timeSingle = endTime - startTime
                seconds = timeSingle.total_seconds()
                if isWeek:
                    f2.write(
                        "{}|月|{}|日|星期|{}|方案|{}|程序已运行|{}|{}|秒\n".format(
                            month,
                            day,
                            weekday,
                            self.__solution_count,
                            endTime - startTime,
                            seconds,
                        )
                    )
                else:
                    f2.write(
                        "{}|月|{}|日|    |  |方案|{}|程序已运行|{}|{}|秒\n".format(
                            month,
                            day,
                            self.__solution_count,
                            endTime - startTime,
                            seconds,
                        )
                    )
                f2.close()
            if self.__solution_count >= self.__solution_limit:
                self.StopSearch()

        def solution_count(self):
            return self.__solution_count

    solution_printer = VarArraySolutionPrinter(work, maxSolNum)  # 修改以改变解数量
    status = solver.Solve(model, solution_printer)
    assert solution_printer.solution_count() == maxSolNum  # 修改以改变解数量
    # 统计结果
    print("统计数据")
    # print('  - 状态       : %s' % solver.StatusName(status))
    print("  - 状态       : ", end="")
    if solver.StatusName(status) == "OPTIMAL":
        print("最优解")
    elif solver.StatusName(status) == "FEASIBLE":
        print("可行解")
    elif solver.StatusName(status) == "INFEASIBLE":
        print("无解")
    else:
        print(solver.StatusName(status))
    print("  - 冲突       : %i" % solver.NumConflicts())
    print("  - 分支       : %i" % solver.NumBranches())
    print("  - 运行时长   : %f s" % solver.WallTime())
    with open("print2.log", "a+", encoding="utf-8") as f3:
        f3.write(
            "月|{}|日|{}|星期|{}|状态|{}|冲突|{}|分支|{}|运行时长|{}|方案数|{}\n".format(
                month,
                day,
                weekday,
                solver.StatusName(status),
                solver.NumConflicts(),
                solver.NumBranches(),
                solver.WallTime(),
                maxSolNum,
            )
        )


# from csv2html import csv2md
def makeOutFile(year, month, day, weekday, isWeek):
    if isWeek:
        outfileName = "./已完成结果/{}/{}月{}日星期{}.md".format(
            year, month, day, weekday
        )
    else:
        outfileName = "./已完成结果/{}/{}月{}日无星期.md".format(year, month, day)
    if not os.path.exists("./已完成结果/{}".format(year)):
        os.makedirs("./已完成结果/{}".format(year))
    with open(outfileName, "w+", encoding="utf-8") as f:
        if isWeek:
            f.write("{}年{}月{}日星期{}\n".format(year, month, day, weekday))
        else:
            f.write("{}年{}月{}日\n".format(year, month, day))
        f.close()
    return outfileName


def main(isLeapYear, isWeek, startMonth, startDay, startWeekday, maxSolNum):
    # day = 29  #日，均从1开始
    # month = 8  #月
    # weekday = 2  #星期,0表示星期天
    """isLeapYear = 0 #是否闰年
    isWeek = True  #是否带星期
    startMonth = 9  #第一天是几月
    startDay = 10  #第一天是几号
    startWeekday = 0  #第一天是星期几
    maxSolNum = 50  #最大解数量"""

    # for month in range(8, 13):#月范围
    for month in range(startMonth, 13):  # 月范围
        list31 = [1, 3, 5, 7, 8, 10, 12]
        if month in list31:
            maxDay = 31
        else:
            maxDay = 30
        for day in range(1, maxDay + 1):
            if day < startDay and month == startMonth:
                continue
            if month == 2 and day >= 29 + isLeapYear:
                continue
            weekday = startWeekday % 7
            startWeekday += 1
            print("{}月{}日星期{}".format(month, day, weekday))
            print("开始计算")
            outfileName = makeOutFile(year, month, day, weekday, isWeek)
            newfileName = outfileName.replace(".md", "-完成.md")
            if os.path.isfile(newfileName):
                print("已计算过")
                os.remove(outfileName)
                continue
            solve(day, month, weekday, isWeek, maxSolNum, outfileName)
            os.rename(outfileName, newfileName)


main(isLeapYear, isWeek, startMonth, startDay, startWeekday, maxSolNum)
