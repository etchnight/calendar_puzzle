# 日历拼图

日历拼图的线性规划解法，使用google的[ortools工具箱](https://developers.google.cn/optimization/cp/cp_solver?hl=zh-cn)进行求解。

## 使用说明

修改参数，直接运行即可，会在终端输出结果，目前设置的是寻找全部可行解，目前没有做界面或输入。

需要修改的参数如下：
- day = 24  #日，均从1开始
- month = 8  #月
- weekday = 4  #星期,0表示星期天
- isWeek = True  #是否带星期

或者在已完成结果内有部分已经算好的结果，可直接查看。

## 算法