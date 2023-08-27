csvname = "已完成结果/8_27_3_result"
count = 0
scheme=''
isweek=True
color=['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc',"#A9A9A9","#FFFFFF"]
with open(csvname + '.csv', 'r') as inputFile:
    with open(csvname + '.html', 'w+') as output:
        output.write('<style>td{width: 20px;height: 20px;}</style>')
        line = inputFile.readline()
        while line:
            cellList = line.split(',')
            count += 1
            #print(line)
            if len(cellList)-1<=0:
                line = inputFile.readline()
                continue
            if cellList[len(cellList)-1]!=scheme:
                scheme=cellList[len(cellList)-1]
                output.write('</table>\n<h3>{}</h3>\n<table>'.format(scheme))
            output.write('<tr>')
            for i in range(len(cellList)-1):
                if (i>1 and not (isweek) and i<9)or(i>2 and isweek and i<10):
                    if cellList[i]=='':
                        num=10
                    else:
                        num=int(cellList[i])
                    output.write('<td style="background:{};">{}</td>'.format(color[num],num))     
            output.write('</tr>')
            line = inputFile.readline()
        output.close()
    inputFile.close()
