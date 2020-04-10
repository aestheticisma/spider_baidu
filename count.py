'''
author: 流岚
date: 2020-4-10 20:45
version 2.0

README:
1. 本文件由spider_baidu.py调用
2. 计算月份数量以xlsx格式存储在该代码同级目录下 名称为 count_keyword.xlsx以此类推
3. xlsx文件内容共有两列：'date', 'count' 其中'date'的格式为 例：2020-04- 'count'即为数量
'''
import pandas as pd

def count_data(filename, keyword):

# filenames = ['test0.xlsx']

	year_list = [str(i)+'-' for i in range(2003,2021)]
	month_list = [str(i)+'-' for i in range(1,13)]
	for i in range(0, 9):
		month_list[i] = '0'+month_list[i]
	year_month = {}


	# for filename in filenames:
	for year in year_list:
		for month in month_list:
			year_month[year+month] = 0
			
	test = pd.read_excel(filename)

	for i in test['date'].values:
		if i[:8] in year_month:
			year_month[i[:8]] += 1
	# print(year_month)
	date_list = []
	count_list = []
	for date, count in year_month.items():
		date_list.append(date)
		count_list.append(count)
	date_count = {'date': date_list, 'count': count_list}

	year_month_df = pd.DataFrame(date_count)
	print(year_month_df)
	year_month_df.to_excel('count_'+keyword+'.xlsx')
	print('keyword %s 统计完成.' % keyword)

if __name__ == '__main__':
	count_data('test0.xlsx', '支付宝')

