'''
author: 流岚
date: 2020-4-10 20:45
version: 2.0

README:
1. 修改 keyword_list: 为一个列表，添加你要爬取的”关键词“
2. 爬取的数据以xlsx格式存储在该代码同级目录下 名称为test0.xlsx test1.xlsx以此类推
3. xlsx文件内容共有两列：'title', 'date' 其中'date'的格式为 例：2020-04-08
4. 页面时间显示“多少分钟前、或者多少小时前、或者一天内”均看作当日时间，其余时间为原本日期
5. 百度检索出的页面划分为了三种：a.无图片 b.有图片 c.回答类 or 发表的文档
'''
from selenium import webdriver
import time
import datetime
import re
import pandas as pd
import re
from count import count_data


keyword_list = ['支付宝', '淘宝']
url = 'https://www.baidu.com'
start_times = []
end_times = []
# 数据统计至 2020.01.01
year_list = [str(i)+'-' for i in range(2003,2020)]
for year in year_list:
	start_times.append(year+'01-'+'01')
	start_times.append(year+'07-'+'01')
end_times = start_times[1:]+['2020-01-01']

class baidu_news(object):
	# 初始化：打开百度，输入关键词进行检索等
	def __init__(self, browser, keyword, start_time, end_time):
		self.title_list = []
		self.date_list = []
		# url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=' + keyword+ '&medium=0'
		# url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=' + keyword + '&oq=%25E6%2594%25AF%25E4%25BB%2598%25E5%25AE%259D&rsv_pq=bb36772a0003cda3&rsv_t=9cc2QrYR2355o1iOwwsZgkWsfwZSZtW41ZfRE6KJd2OLxeik3UJiD5E6O%2Bo&rqlang=cn&rsv_enter=0&rsv_dl=tb&gpc=stf%3D0%2C1586448000%7Cstftype%3D2&tfflag=1'
		self.browser = browser
		#获取网址
		self.browser.get(url)
		search_input = self.browser.find_element_by_xpath('//*[@class="s_ipt"]')
		search_input.clear()
		search_input.send_keys(keyword)
		search_input.submit()
		self.current_url = self.browser.current_url
		self.start_time = start_time
		self.end_time = end_time
		self.keyword = keyword
	# 选择时间年份
	def choice_time(self):
		self.browser.get(self.current_url)
		# print(len(self.browser.find_elements_by_xpath('//*[@class="t"]')))
		self.browser.find_element_by_xpath('//*[@class="search_tool"]').click()
		time.sleep(1)
		self.browser.find_element_by_xpath('//*[@class="search_tool_tf "]').click()
		time.sleep(1)
		start = self.browser.find_element_by_xpath('//input[@name="st"]')
		start.clear()
		start.send_keys(start_time)
		end = self.browser.find_element_by_xpath('//input[@name="et"]')
		end.clear()
		end.send_keys(end_time)
		time.sleep(1)
		self.browser.find_element_by_xpath('//*[@class="c-tip-custom-submit"]').click()
		self.current_url = self.browser.current_url
		self.browser.get(self.current_url)
	# 无图类型
	def get_date_1(self):
		# time.sleep(1)
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		# yesterday = (datetime.datetime.now()-datetime.timedelta(hours=24)).strftime('%Y-%m-%d')
		dates = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/div[@class="c-abstract"]/span[@class=" newTimeFactor_before_abs m"]')
		titles = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/div[@class="c-abstract"]/span[@class=" newTimeFactor_before_abs m"]/../../h3/a')
		print('无图: %d, %d' % (len(dates), len(titles)), end = '\n')
		for date, title in zip(dates, titles):
			#test
			date_str = date.text
			if '前' in str(date_str):
				date_str = today
			else:
				date_str = ''.join(re.split(r'[-]', date_str))
				date_str = date_str.replace('年','-')
				date_str = date_str.replace('月','-')
				date_str = date_str.replace('日','')
				date_str = date_str.strip()
				if len(date_str) == 9:
					if date_str[6] == '-':
						date_str = date_str[:5]+'0'+date_str[5:]
					else:
						date_str = date_str[:8]+'0'+date_str[8:]
				elif len(date_str) == 8:
					date_str = date_str[:5]+'0'+date_str[5:]
					date_str = date_str[:8]+'0'+date_str[8:]
			print('过滤前：%s, %s' % (title.text, date_str))

			# 判断网页标题是否有该keyword 以及 是否为所选年份时间内
			if self.keyword in title.text and (self.start_time[:4] in date_str or self.end_time == date_str):
				self.date_list.append(date_str)
				self.title_list.append(title.text)
				print('过滤后：%s, %s' % (title.text, date_str))
	# 有图类型
	def get_date_2(self):
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		dates = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/div[@class="c-row c-gap-top-small"]/div[@class="c-span18 c-span-last"]/div[@class="c-abstract"]/span[@class=" newTimeFactor_before_abs m"]')
		titles = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/div[@class="c-row c-gap-top-small"]/div[@class="c-span18 c-span-last"]/div[@class="c-abstract"]/span[@class=" newTimeFactor_before_abs m"]/../../../../h3/a')
		# print(len(dates), len(titles))
		print('\n有图: %d, %d' % (len(dates), len(titles)), end = '\n')
		for date, title in zip(dates, titles):
			#test
			date_str = date.text
			if '前' in str(date_str) or '内' in str(date_str):
				date_str = today
			else:
				date_str = ''.join(re.split(r'[-]', date_str))
				date_str = date_str.replace('年','-')
				date_str = date_str.replace('月','-')
				date_str = date_str.replace('日','')
				date_str = date_str.strip()
				if len(date_str) == 9:
					if date_str[6] == '-':
						date_str = date_str[:5]+'0'+date_str[5:]
					else:
						date_str = date_str[:8]+'0'+date_str[8:]
				elif len(date_str) == 8:
					date_str = date_str[:5]+'0'+date_str[5:]
					date_str = date_str[:8]+'0'+date_str[8:]
			print('过滤前：%s, %s' % (title.text, date_str))
			# 判断网页标题是否有该keyword 以及 是否为所选年份时间内
			if self.keyword in title.text and (self.start_time[:4] in date_str or self.end_time == date_str):
				self.date_list.append(date_str)
				self.title_list.append(title.text)
				print('过滤后：%s, %s' % (title.text, date_str))
	#回答类 or 发表文章类
	def get_date_3(self):
		dates = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/p[@class="f13 m"]')
		titles = self.browser.find_elements_by_xpath('//div[@class="result c-container "]/p[@class="f13 m"]/../h3/a')
		
		print('\n发布或回答时间: %d, %d' % (len(dates), len(titles)), end = '\n')
		for date, title in zip(dates, titles):
			date_str = str(re.findall(r'[\d]{4}.[\d]{1,2}.[\d]{1,2}', date.text))[2:-2]
			date_str = date_str.replace('年','-')
			date_str = date_str.replace('月','-')
			if len(date_str) == 9:
				if date_str[6] == '-':
					date_str = date_str[:5]+'0'+date_str[5:]
				else:
					date_str = date_str[:8]+'0'+date_str[8:]
			elif len(date_str) == 8:
				date_str = date_str[:5]+'0'+date_str[5:]
				date_str = date_str[:8]+'0'+date_str[8:]
			print('过滤前：%s, %s' % (title.text, date_str))
			# 判断网页标题是否有该keyword 以及 是否为所选年份时间内
			if self.keyword in title.text and (self.start_time[:4] in date_str or self.end_time == date_str):
				self.date_list.append(date_str)
				self.title_list.append(title.text)
				print('过滤后：%s, %s' % (title.text, date_str))
	# 跳转至下一页
	def next_page(self):
		self.browser.find_elements_by_xpath("//a[@class='n']")[-1].click()
		time.sleep(3)
	# 判断是否为最后一页
	def get_pagenum(self):
		page = self.browser.find_element_by_xpath('//*[@id="page"]')
		nextpage = page.text.split('\n')[-1]
		if nextpage == '下一页>':
			return True
		else:
			return False
	# 关闭浏览器
	def close(self):
		self.browser.close()

if __name__ == '__main__':
	chrome_options= webdriver.ChromeOptions()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--headless')
	browser = webdriver.Chrome(chrome_options=chrome_options) #'D:\Google\chromedriver', chrome_options=chrome_options
	for num, keyword in enumerate(keyword_list):
		title_list = []
		date_list = []
		for start_time, end_time in zip(start_times, end_times):
			page = 0
			print('keyword:%s' % keyword)
			print('time: %s - %s' % (start_time, end_time))
			driver = baidu_news(browser, keyword, start_time, end_time)
			driver.choice_time()
			while True:
			# for i in range(10):
				# driver.get_title()
				print('\n************* 正在载入第%d页 **************' % (page+1))
			# for i in range(10):
				# driver.get_title()
				driver.get_date_1()
				driver.get_date_2()
				driver.get_date_3()
				if driver.get_pagenum():
					driver.next_page()
					page += 1
				else:
					break
				# driver.next_page()
			title_list += driver.title_list
			date_list += driver.date_list

		data_dict = {'title': title_list, 'date': date_list}
		data_df = pd.DataFrame(data_dict)
		print(data_df)
		filename = 'test'+str(num)+'.xlsx'
		data_df.to_excel(filename, index = None)
		#统计并保存统计结果
		count_data(filename, keyword)
	driver.close()








