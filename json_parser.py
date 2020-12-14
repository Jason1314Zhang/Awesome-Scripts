# Author: SuperJason
# Date: 2020.12.10
# usage: change root_dir in __main__
# description: parser API sequences behavior from cuckoo analyzer folder
import json
import sys
import pandas as pd
import os

#将json文件decode为python dict
def json_parser(json_file):
	#print(json_file)
	with open(json_file,"rb") as f:
		json_data=json.load(f)
	return json_data

#输入json dict，返回样本名称、样本sha1、API调用序列、每种API的调用次数（dict）
def get_behavior(json_data):
	sample_name=json_data["target"]["file"]["name"]
	sample_sha1=json_data["target"]["file"]["sha1"]
	#print(sample_name)
	for process in json_data["behavior"]["processes"]:
		if sample_name==process["process_name"]:
			sample_pid=process["pid"]
			API_calls=process["calls"]
	#get API sequences
	API_sequences=''
	for call in API_calls:
		API_sequences+=call["api"]+' '
	API_sequences.strip(' ')
	#get API counts dict
	for pid in json_data["behavior"]["apistats"]:
		if str(sample_pid)==pid:
			API_counts_dict=json_data["behavior"]["apistats"][pid]		
	#修改此处的值可以得到需要的list数据
	return sample_name,sample_sha1,API_sequences

#传入一个report.json文件
#获得样本名、API序列、API counts
def report_parser(root_dir):
	#获得子目录、文件个数
	result_list=[]
	dir_num=len(os.listdir(root_dir))		
	for index in range(1,dir_num):
		#print(index)
		filepath=root_dir+"/"+str(index)+"/reports/report.json"
		#single_list=[sample_name,sample_sha1,API_sequences,API_counts_dict]
		#single_list类型分别为str、str、list、dict
		single_list=list(get_behavior(json_parser(filepath)))
		result_list.append(single_list)
	name=['name','sha1','sequences']
	matrix=pd.DataFrame(columns=name,data=result_list)
	print(matrix)
	#保存API_sequences.csv文件到当前工作目录
	matrix.to_csv(os.path.join(os.getcwd(),"API_sequences.csv"),encoding="utf-8")

if __name__ == "__main__":
	#指定analyzer目录
	root_dir="C:/Users/SuperJason/Desktop/analyzer" #change folder
	report_parser(root_dir)