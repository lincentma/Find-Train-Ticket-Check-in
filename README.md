## Find-Train-Ticket-Check-in

来自于[ecmadao](https://github.com/ecmadao)的小项目(https://github.com/ecmadao/Train-12306)的启发
原由：近日多地大雨导致铁路多趟列车停运，自己关注成都铁路12306微信公众号，发现一个新的侯乘信息查询功能。
该功能提供了动车和高铁的列车检票口的信息，正好圆了自己的之前挖的坑建的这个仓库。
微信公众号地址：http://kf.cd-rail.com/CTKF/CTZX/view/mainFrame/wx_hcxx.html

### 开发环境

腾讯云服务器  python 2.7.6

### 第三方依赖

[prettytable](https://pypi.python.org/pypi/PrettyTable/0.7.2)
[click](https://pypi.python.org/pypi/click/6.7)


### 做出来的效果

```bash
ubuntu@VM-68-117-ubuntu:~/maling/workspace/FindTrainTicketCheck-in$ python run.py 
查询车站 [成都东站]: 成都东站
查询车次 []: D368
查询日期 [20170704]: 20170704
+------+--------+------+-------+--------+-----------+----------+
| 车次 |  始发  | 终到 |  发时 | 检票口 |   候车区  | 检票状态 |
+------+--------+------+-------+--------+-----------+----------+
| D368 | 成都东 | 武汉 | 10:55 | B8、B9 | 2层候车区 | 停止检票 |
+------+--------+------+-------+--------+-----------+----------+
ubuntu@VM-68-117-ubuntu:~/maling/workspace/FindTrainTicketCheck-in$ 

```
