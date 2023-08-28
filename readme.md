# 日历拼图

日历拼图的线性规划解法，使用google的[ortools工具箱](https://developers.google.cn/optimization/cp/cp_solver?hl=zh-cn)进行求解。

## 使用说明

1. 安装ortools
```
python -m pip install --upgrade --user ortools
```
 
2. 修改`main.py`中函数参数，直接运行即可，会在终端输出结果并生成csv和html表格(md文件)两种结果，会从开始的日期一直算到年底，目前没有做界面或输入。

需要修改的参数如下：
- isLeapYear = 0 #是否闰年
- isWeek = True  #是否带星期
- startMonth = 9  #第一天是几月
- startDay = 10  #第一天是几号
- startWeekday = 0  #第一天是星期几
- maxSolNum = 50  #最大解数量(每天)

> 或者在`已完成结果`文件夹内有部分已经算好的结果，可直接查看，由于每天的解法众多（不带星期版有100+解法，带星期版有1000+解法甚至2000+解法，每天只算50种）。


## 日历拼图的线性规划算法

以带星期的拼图为例，一个符合条件的解应该是如下样子：

<table><tr><td style="background:#ea7ccc;">8</td><td style="background:#ea7ccc;">8</td><td style="background:#ea7ccc;">8</td><td style="background:#ee6666;">3</td><td style="background:#ee6666;">3</td><td style="background:#ee6666;">3</td><td style="background:#FFFFFF;"></td></tr><tr><td style="background:#ea7ccc;">8</td><td style="background:#FFFFFF;"></td><td style="background:#ee6666;">3</td><td style="background:#ee6666;">3</td><td style="background:#A9A9A9;">9</td><td style="background:#A9A9A9;">9</td><td style="background:#FFFFFF;"></td></tr><tr><td style="background:#FFFFFF;"></td><td style="background:#73c0de;">4</td><td style="background:#73c0de;">4</td><td style="background:#5470c6;">0</td><td style="background:#5470c6;">0</td><td style="background:#A9A9A9;">9</td><td style="background:#A9A9A9;">9</td></tr><tr><td style="background:#9a60b4;">7</td><td style="background:#73c0de;">4</td><td style="background:#5470c6;">0</td><td style="background:#5470c6;">0</td><td style="background:#5470c6;">0</td><td style="background:#fac858;">2</td><td style="background:#91cc75;">1</td></tr><tr><td style="background:#9a60b4;">7</td><td style="background:#73c0de;">4</td><td style="background:#fc8452;">6</td><td style="background:#fac858;">2</td><td style="background:#fac858;">2</td><td style="background:#fac858;">2</td><td style="background:#91cc75;">1</td></tr><tr><td style="background:#9a60b4;">7</td><td style="background:#73c0de;">4</td><td style="background:#fc8452;">6</td><td style="background:#fac858;">2</td><td style="background:#91cc75;">1</td><td style="background:#91cc75;">1</td><td style="background:#91cc75;">1</td></tr><tr><td style="background:#9a60b4;">7</td><td style="background:#fc8452;">6</td><td style="background:#fc8452;">6</td><td style="background:#fc8452;">6</td><td style="background:#3ba272;">5</td><td style="background:#FFFFFF;"></td><td style="background:#3ba272;">5</td></tr><tr><td style="background:#FFFFFF;"></td><td style="background:#FFFFFF;"></td><td style="background:#FFFFFF;"></td><td style="background:#FFFFFF;"></td><td style="background:#3ba272;">5</td><td style="background:#3ba272;">5</td><td style="background:#3ba272;">5</td></tr></table>

#### 1. 构建0-1矩阵

首先，将问题进行分解，其有10块拼图，每块拼图由最多5个方块组成，每块拼图又有最多8种形态（或状态），分别为：原始、逆时针旋转90°后左右翻转（左下右上45°翻转）、左右翻转、逆时针旋转90°、上下翻转、顺时针旋转90°、旋转180、顺时针旋转90后左右翻转（左上右下45°翻转）。在拼好的状态下，每块拼图的每个方块都有唯一的位置，即行索引和列索引。

由此，我们可以构建一个5维矩阵，其中的每个元素用`work[p, n, s, r, c] `表示，即p拼图的第n个方块在第s种形态下是否在第r行第c列，这是一个0-1矩阵，每个元素只有两种取值，即真或假（0或1）。

请注意上面所用的字母，下文中将经常提到，即:
- p:拼图块
- n:拼图块的第n个方块
- s:拼图块所处的形态
- r:行号
- c:列号

> 当然，可能的优化方法是将块拼图的所有47个方块统一编号为0-46,这样就是一个4维矩阵，但是在下步的设置条件环节将更为复杂，我们在此不做讨论。

#### 2. 约束条件设置

1. 首先，要将拼图块放在底板上，每个位置只能有1个方块(个别位置没有)，且这个拼图块（方块）只能处于1种形态。即：在位置`[r,c]`上所有`[p,n,s]`位置元素取值的和小于等于1（无法保证等于1，因为指定的日期，即底板内空白的位置是不确定的），当然，因为底板形状不是长方形，在某些位置其应该等于0。

> 在该条件下，可能有的拼图块取到很多次（有多个位置），有的却并没有被使用。

2. 其次，需要再添加一个条件，每种拼图块的每个方块号只有1个行号、列号、形态（由于拼图块所含方块数不同，部分拼图块不可选择某些方块号）。即：在`[p,n]`上所有`[r,c,s]`位置元素的取值的和等于1，当然，实际不存在的方块号其和为0。

> 在该条件下，不同的方块可以选择同一个位置。

3. 另外一个显而易见的条件是，每种拼图块的所有方块均应属于一种形态，毕竟不能把拼图块真的切成方块。即：对每种拼图块的每种形态(`[p,s]`)，所有位置上的方块数总和（`[n,r,c]`）要么等于0（未使用该形态），要么等于拼图块的方块数。

4. 在这一步，要把每种拼图块的方块"拼"成其本身的形状。首先确定每种拼图块的一种形态，将其方块进行编号（如0-5），确定0号方块的位置，即可确定其他方块的位置（在0号方块偏移i行j列的位置）。即在某位置，某拼图块的某形态下（`[r,c,p,s]`），0号方块与第n号方块所在元素的和不等于1(为0时，拼图块不在该位置；为2时，拼图块在该位置)。

若假设的形态下0号方块位于`(r,c)`，其他某方块位置为`(r+i,c+j)`,则其他形态下分别为`(r+i,c+j)(r+j,c+i)(r+i,c-j)(r+j,c-i)(r-i,c+j)(r-j,c+i)(r-i,c-j)(r-j,c-i)`。

需要注意的是，如果计算出任一方块的位置索引超出底板范围，则说明该拼图块的0号方块在该形态下不能出现在该位置。

5. 到此，已经可以与实际一致了，即可以把所有拼图块放入底板了。如果不指定日期，再限制所有表示月份的位置，其所有拼图块的所有方块的形态和为11；所有表示星期的位置，和为6即可。要指定日期，则为指定行号、列号下，其余参数取所有值的元素和为0。

6. 上面的约束已可以计算出所有结果，但是有冗余，因为某些拼图块“变换形态”后，新形态与原形态是一致的，为消除冗余，可以禁用某些形态，即设置该拼图块的某些形态下，所有方块在所有位置下`[n,r,c]`元素和为0。

要注意辨别哪些形态是重复的，不同的拼图块重复形态并不一致。

#### 3.求解

该问题属于限制条件优化问题，可以使用google的[ortools工具箱](https://developers.google.cn/optimization/cp/cp_solver?hl=zh-cn)中CP-SAT 求解器进行求解。

## 后记

经测试，计算出1种方案的时间在10-20秒之间（带星期），若取为20秒，也就是说，如果每天只计算1种方案，2小时可算完某1年的所有答案，14小时可算完所有答案。

经测试，每天的解法众多：不带星期版每天有100+解法，取为150种，1年365天大概有5.5万个解；带星期版每天有1000+解法甚至2000+解法，取为2000种，每年大概有73万个解，算上星期的不同有511万个解。上述解，是从`2^7^7^8^6^8`或`2^8^7^10^5^8`种可能中找到的。总之，请最好不要尝试计算出所有解。

最后，该算法能够保证计算出的解均符合要求，但是难以保证没有冗余，如果应增加其他限制条件，请告诉我，不胜感激！