import os
def csv2md(month,day,weekday,isweek):
    dirname="result"
    if isweek:
        csvname = "{}_{}_{}_result".format(month,day,weekday)
    else:
        csvname = "{}_{}_result".format(month,day)
    count = 0
    scheme = ''
    #isweek = True
    color = [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272',
        '#fc8452', '#9a60b4', '#ea7ccc', "#A9A9A9", "#FFFFFF"
    ]
    count = 1
    #outputName='{}/{}/{}_{}-{}.md'.format(dirname,csvname, csvname,str(count), str(count + 100))
    outputName='已完成结果/{}.md'.format(csvname)

    '''
    path='{}/{}'.format(dirname,csvname)
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  '''
    with open(dirname+"/"+csvname + '.csv', 'r',encoding="utf-8") as inputFile:
        output = open((outputName), 'w+',encoding='utf-8')
        output.write('<style>td{width: 20px;height: 20px;}</style>')
        line = inputFile.readline()
        while line:
            cellList = line.split(',')
            #print(line)
            if len(cellList) - 1 <= 0:
                line = inputFile.readline()
                continue
            if cellList[len(cellList) - 1] != scheme:
                count += 1
                '''
                if count%100==0:
                    output.close()
                    outputName='{}/{}/{}_{}-{}.md'.format(dirname,csvname, csvname,str(count), str(count + 100))
                    output = open((outputName), 'w+')
                    output.write('<style>td{width: 20px;height: 20px;}</style>')'''
                scheme = cellList[len(cellList) - 1]
                output.write('</table>\n<h3>{}</h3>\n<table>'.format(scheme))
            output.write('<tr>')
            for i in range(len(cellList) - 1):
                if (i > 1 and not (isweek) and i < 9) or (i > 2 and isweek
                                                        and i < 10):
                    if cellList[i] == '':
                        num = 10
                    else:
                        num = int(cellList[i])
                    output.write('<td style="background:{};">{}</td>'.format(
                        color[num], num))
            output.write('</tr>')
            line = inputFile.readline()
        output.close()
        inputFile.close()

csv2md(9,1,5,True)
