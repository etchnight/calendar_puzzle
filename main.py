from ortools.sat.python import cp_model

day=23
month=8
def solve():
    model = cp_model.CpModel()
    num_pieces = 8
    num_row = 7
    num_col = 7
    num_piece = 6

    work = {}
    # 创建【碎片型号，碎片号，碎片排布形态，行号，列号】的五维0-1数组
    for p in range(num_pieces):
        for n in range(num_piece):
            for s in range(8):
                for r in range(num_row):
                    for c in range(num_col):
                        work[p, n, s, r, c] = model.NewBoolVar(
                            'work_%i_%i_%i_%i_%i' % (p, n, s, r, c))
    #输入条件
    if day and month:
        rowDay=int((day-1)/7)+2
        colDay=(day-1) % 7 
        rowMonth=int((month-1)/6)
        colMonth=(month-1) % 6
        #print(rowDay,colDay,rowMonth,colMonth)
        model.Add(sum(work[p, n, s, rowDay, colDay] for p in range(num_pieces)
            for n in range(num_piece) for s in range(8)) == 0)
        model.Add(sum(work[p, n, s, rowMonth, colMonth] for p in range(num_pieces)
            for n in range(num_piece) for s in range(8)) == 0)

    #每个行号、列号只有一种碎片的一种形态的一个号(个别位置没有)
    for r in range(num_row):
        for c in range(num_col):
            if (r == 0 and c == 6) or (r == 1 and c == 6) or (r == 6
                                                              and c > 2):
                """不可选择的位置"""
                model.Add(
                    sum(work[p, n, s, r, c] for p in range(num_pieces)
                        for n in range(num_piece) for s in range(8)) == 0)
            else:
                model.Add(
                    sum(work[p, n, s, r, c] for p in range(num_pieces)
                        for n in range(num_piece) for s in range(8)) <= 1)

    #每种型号的每个碎片号只有1个行号、列号、形态
    for p in range(num_pieces):
        for n in range(num_piece):
            if (p > 0 and n == 5):
                "不可选择的碎片号"
                model.Add(
                    sum(work[p, n, s, r, c] for r in range(num_row)
                        for c in range(num_col) for s in range(8)) == 0)
            else:
                model.Add(
                    sum(work[p, n, s, r, c] for r in range(num_row)
                        for c in range(num_col) for s in range(8)) == 1)

    #每种型号的所有碎片的形态号统一
    for p in range(num_pieces):
        for s in range(8):
            if p == 0:
                model.Add(
                    sum(work[p, n, s, r, c] for r in range(num_row)
                        for c in range(num_col)
                        for n in range(num_piece)) <= 6)
                model.Add(
                    sum(work[p, n, s, r, c] for r in range(num_row)
                        for c in range(num_col)
                        for n in range(num_piece)) != 5)
            else:
                model.Add(
                    sum(work[p, n, s, r, c] for r in range(num_row)
                        for c in range(num_col)
                        for n in range(num_piece)) <= 5)
            model.Add(
                sum(work[p, n, s, r, c] for r in range(num_row)
                    for c in range(num_col) for n in range(num_piece)) != 4)
            model.Add(
                sum(work[p, n, s, r, c] for r in range(num_row)
                    for c in range(num_col) for n in range(num_piece)) != 3)
            model.Add(
                sum(work[p, n, s, r, c] for r in range(num_row)
                    for c in range(num_col) for n in range(num_piece)) != 2)
            model.Add(
                sum(work[p, n, s, r, c] for r in range(num_row)
                    for c in range(num_col) for n in range(num_piece)) != 1)

    # 前两行空的必须为1
    model.Add(
        sum(work[p, n, s, r, c] for p in range(num_pieces)
            for n in range(num_piece) for s in range(8) for r in range(2)
            for c in range(num_col)) == 11)

    # 拼图块内距离约束
    def addDistance(di, dj, pnum, nnum, nnum2):
        """
        nnum：源碎片序号
        nnum2：目标碎片序号
        """
        d = [di, dj]
        for r in range(num_row):
            for c in range(num_col):
                '''for p in range(num_pieces):
                    for n in range(num_piece):
                        if pnum != p or n != nnum2:'''
                s = 0
                for i in [1, -1]:
                    for j in [1, -1]:
                        for k in [0, 1]:
                            row = r + i * d[k]
                            col = c + j * d[1 - k]
                            #print(i,j,k)
                            if row < num_row and col < num_col and row >= 0 and col >= 0:
                                #print([pnum, nnum, s, r, c])
                                #print([pnum, nnum2, s, row, col])
                                model.Add(
                                    (work[pnum, nnum, s, r, c] +
                                     work[pnum, nnum2, s, row, col] != 1))
                            else:
                                #该形态不能出现在该位置
                                model.Add(work[pnum, nnum, s, r, c] == 0)
                            s = s + 1

    #禁用形态
    '''
    0:原始
    1:逆时针旋转90后左右翻转（左下右上45°翻转）
    2:左右翻转-
    3:逆时针旋转90
    4:上下翻转
    5:顺时针旋转90-
    6:旋转180-
    7:顺时针旋转90后左右翻转（左上右下45°翻转）-
    '''
    #0号
    for s in range(2,8):
         model.Add(sum(work[0, n, s, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    #2号
    model.Add(sum(work[2, n, 1, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[2, n, 3, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[2, n, 5, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[2, n, 7, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    #3号
    model.Add(sum(work[3, n, 4, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[3, n, 5, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[3, n, 6, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[3, n, 7, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    #7号
    model.Add(sum(work[7, n, 2, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[7, n, 5, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[7, n, 6, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    model.Add(sum(work[7, n, 7, r, c] for r in range(num_row)
                                for c in range(num_col)  for n in range(num_piece) ) == 0)
    #0号拼图
    """012  
       345"""
    addDistance(1, 2, 0, 0, 5)
    addDistance(1, 1, 0, 0, 4)
    addDistance(1, 0, 0, 0, 3)
    addDistance(0, 2, 0, 0, 2)
    addDistance(0, 1, 0, 0, 1)
    #1号拼图
    """
       012
       34
    """
    addDistance(1, 1, 1, 0, 4)
    addDistance(1, 0, 1, 0, 3)
    addDistance(0, 2, 1, 0, 2)
    addDistance(0, 1, 1, 0, 1)
    #2号拼图
    """
        0
        1
        234
    """
    addDistance(2, 2, 2, 0, 4)
    addDistance(2, 1, 2, 0, 3)
    addDistance(2, 0, 2, 0, 2)
    addDistance(1, 0, 2, 0, 1)
    #3号拼图
    """
       01
        2
        34
    """
    addDistance(2, 2, 3, 0, 4)
    addDistance(2, 1, 3, 0, 3)
    addDistance(1, 1, 3, 0, 2)
    addDistance(0, 1, 3, 0, 1)
    #4号拼图
    """
       0
       1
       23
        4
    """
    addDistance(3, 1, 4, 0, 4)
    addDistance(2, 1, 4, 0, 3)
    addDistance(2, 0, 4, 0, 2)
    addDistance(1, 0, 4, 0, 1)
    #5号拼图
    """
       0
       1
       23
       4
    """
    addDistance(3, 0, 5, 0, 4)
    addDistance(2, 1, 5, 0, 3)
    addDistance(2, 0, 5, 0, 2)
    addDistance(1, 0, 5, 0, 1)
    #6号拼图
    """
       0
       1
       2
       34
    """
    addDistance(3, 1, 6, 0, 4)
    addDistance(3, 0, 6, 0, 3)
    addDistance(2, 0, 6, 0, 2)
    addDistance(1, 0, 6, 0, 1)
    #7号拼图
    """
       0 1
       234
    """
    addDistance(1, 2, 7, 0, 4)
    addDistance(1, 1, 7, 0, 3)
    addDistance(1, 0, 7, 0, 2)
    addDistance(0, 2, 7, 0, 1)

    #求解
    print("开始计算")
    solver = cp_model.CpSolver()
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    solution_printer = VarArraySolutionPrinter(work)
    status = solver.Solve(model, solution_printer)
    # 统计结果
    print('统计数据')
    print('  - 状态       : %s' % solver.StatusName(status))
    print("  -     OPTIMAL 代表最优解")
    print('  -     INFEASIBLE 代表无解')
    print('  -     FEASIBLE 代表可行解')
    print('  - 冲突       : %i' % solver.NumConflicts())
    print('  - 分支       : %i' % solver.NumBranches())
    print('  - 运行时长   : %f s' % solver.WallTime())
    '''if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("结果预览")
        #print("     0   1   2   3   4   5   6")
        for r in range(num_row):
            #schedule = str(r) + ' : '
            schedule = ''
            for c in range(num_col):
                isprint = False
                for p in range(num_pieces):
                    for s in range(8):
                        for n in range(num_piece):
                            if solver.BooleanValue(work[p, n, s, r, c]):
                                #schedule += str(p) + '.' + str(n) + '.'+ str(s) +' | '
                                #schedule += str(p) + '.' + str(n) +' | '
                                schedule += str(p)  +' | '
                                #schedule += str(p) + '.' + str(s) +' | '
                                isprint = True
                if not isprint:
                    #schedule += '      | '
                    #schedule += '    | '
                    schedule += '  | '
                    #schedule += '    | '
            print(schedule)'''


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        fileName=str(month)+'_'+str(day)+'_'+'result.csv'
        with open(fileName,'a+') as f:
            csv_result=[]
            dayText=''
            monthText=''
            for r in range(7):
                #schedule = str(r) + ' : '
                schedule = ''
                csv_line=''
                for c in range(7):
                    isprint = False
                    for p in range(8):
                        for s in range(8):
                            for n in range(6):
                                if self.BooleanValue(self.__variables[p, n, s, r,
                                                                    c]):
                                    #schedule += str(p) + '.' + str(n) + '.'+ str(s) +' | '
                                    #schedule += str(p) + '.' + str(n) +' | '
                                    csv_line+= str(p) +','
                                    schedule += str(p) +' | '
                                    #schedule += str(p) + '.' + str(s) +' | '
                                    isprint = True
                    if not isprint:
                        #schedule += '      | '
                        #schedule += '    | '
                        schedule += '  | '
                        csv_line+= ','
                        if (r == 0 and c == 6) or (r == 1 and c == 6) or (r == 6
                                                              and c > 2):
                           ''''''
                        elif r>1:
                            dayText=str((r-2)*7+c+1)+','
                        else:
                            monthText=str((r)*6+c+1)+','
                        #schedule += '    | '
                print(schedule)
                csv_line+=str(r)+'行,方案'+str(self.__solution_count)+'\n'
                csv_result.append(csv_line)
            for line in csv_result:
                f.write(monthText)
                f.write(dayText)
                f.write(line)
            print()
            f.close()

    def solution_count(self):
        return self.__solution_count


solve()