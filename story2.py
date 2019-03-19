import urllib
from bs4 import BeautifulSoup
import random
import requests
import json

"""
	V2.0
	此版本直接使用ajax返回的json数据进行分析
"""



"""
	此方法用于返回该字开头的第index页的数据
"""
def getJson(x,index):
	
	url = "https://hanyu.baidu.com/hanyu/ajax/search_list";
	data={
		'wd': x+"字开头的诗句",
		'from':'poem',
		'pn':index,
	}

	response = requests.get(url,params=data)

	# 获取r的文本 就是一个json字符串
	json_response = response.content.decode()
	# 将json字符串转换成dic字典对象
	return json.loads(json_response)

	
"""
	此方法解析数据
"""
def getStory(string):
	
	# diff用于每次都有不一样的诗句
	diff = 1
	# count用于计数，和diff相等时即为需要的诗句
	count = 0
	# 判断是否找到已经需要的数据
	onOff = True;
	# indexNumber是当前页数
	indexNumber = 1;
	
	totalNumber = 1
	# 用于异常的判断
	finallyText = "";
	
	# 取出字符串中的每一个字
	for x in string:
	
		# 每换一个字，初始化相关数据
		
		
		# 每次换一个字，就从第一页开始重新获取
		indexNumber = 1
		dictJson = getJson(x,indexNumber);
		if "extra" in dictJson.keys():
			diff = random.randint(1, 20)
			totalNumber = random.randint(1,  int(dictJson["extra"]["total-page"]))
		indexNumber = totalNumber
		

		dictJson = getJson(x,indexNumber);
		"""
		if diff > 200:
			diff = random.randint(1,200)
		"""
		# 每次换一个字，就从第一页开始重新获取	
		count = 0
		# 每次换一个字，就从第一页开始重新获取
		onOff = True
		row = ""
		finallyText = "";
		
		while(onOff):
			
		
			a={}
			if "ret_array" in dictJson.keys():
				a = dictJson["ret_array"]
			else:
				if finallyText == "":
					print(x + "字太难了，我想不出来")
				else:
					print(finallyText)
				break

			for text in a:
				row = text["display_name"][0]

				if row[0] == x and len(row) == 7:
					
					
					finallyText = row;
					if count == diff:
						#print("111111111111111111111111111\n")
						print(row)
						onOff = False
						break
					
					else:
						#print("忽略掉的诗句：   "+row)
						count += 1
						
			# 如果本页没有找到，就去下一页找
			
			indexNumber += 1
			dictJson = getJson(x,indexNumber)

	print("*************************")
	print("\n")
def main():
	string = input("请输入要生成的句子，输入exit退出\n")
	#string = "郭靖"
	while string != "exit":
		print("正在思考中，请稍后...\n");
		#print("\n")
		getStory(string);
		string = input("请输入要生成的句子，输入exit退出\n")

	print("成功退出，谢谢使用~");

if __name__ == "__main__":
	main();
