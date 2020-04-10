### 0. 功能

* 统计某个关键词，如“支付宝”自2003-01-01至2020-01-01在百度检索系统返回的所有页面标题中含有该关键词的页面数量(以每个月份为计)。

* 检索方式为锁定半年时间一次（可修改）

### 1. Package

```bash
pip install selenium
```

### 2. 安装webdriver

具体步骤详见：https://fansblog.club/2019/12/17/cnki-spider/

### 3. 执行

```bash
python spider_baidu.py
```

### 4. 代码修改详见注释

### 5. 存储格式为xlsx 

* 爬取的数据以xlsx格式存储在该代码同级目录下，名称为test0.xlsx test1.xlsx以此类推
* 计算数量结果以xlsx格式存储在该代码同级目录下，名称为 count_keyword.xlsx以此类推

### 6. 样例文件

* test0.xlsx
* count_支付宝.xlsx

### 7.长期接单爬虫任务

* 请联系aestheticisma@outlook.com

