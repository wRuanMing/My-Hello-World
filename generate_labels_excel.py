# -*- coding: utf-8 -*-
'''
根据子文件夹的名称给子文件夹下的所有文件生成对应标签的csv
'''
import os
import pandas as pd
import collections
#GUI module
import tkinter
from tkinter.filedialog import askdirectory


FOLDER_PATH_STR = ''
def main_function():
    ##################输入输出参数start##################

    #用于生成的总文件夹路径
    print(FOLDER_PATH_STR)
    try:
        FOLDER_PATH = FOLDER_PATH_STR
    except:
        return -1
    #生成的csv文件目录
    GEN_CSV_PATH = os.path.join(os.getcwd(),'label.csv')
    GEN_EXCEL_PATH = os.path.join(os.getcwd(),'label.xlsx')
    #生成的csv类型:
    '''
    CSV_VERSION = 'NAME_LABEL':保存每个文件及其上一级目录的名称作为单一label
    CSV_VERSION = 'LABEL_FILES'保存每个文件夹名称的label和该label的所有文件
    '''
    CSV_VERSION = 'LABEL_FILES'
    ##################输入输出参数end####################

    ###################主要函数start#####################

    def trans_to_file_label_list_version1(prior_format_list):
        '''
        只取上一级的文件夹名称作为label
        '''
        label_prior = prior_format_list[0]
        files_list = prior_format_list[1]
        if label_prior == '.':
            label = None
        else:
            label = os.path.split(label_prior)[-1]
        return [[ii,label] for ii in files_list]
    ###################主要函数end#####################



    ##################主要流程start##################

    #当前目录切换到用于生成的总文件夹下
    print(FOLDER_PATH)
    os.chdir(FOLDER_PATH)
    #获取总文件夹下所有的文件及对应的文件夹名称version1：只匹配上一级的文件夹
    folder_name_and_file_name_list = [[dp,df] for dp,dn,df in os.walk('.')]
    if CSV_VERSION == 'NAME_LABEL':
        file_label_info_list = []
        for i in folder_name_and_file_name_list:
            if i[1] == []:
                continue
            file_label_info_list.extend(trans_to_file_label_list_version1(prior_format_list = i))
        df = pd.DataFrame(file_label_info_list,columns=['name','label'])
    if CSV_VERSION == 'LABEL_FILES':
        label_files_dict = collections.OrderedDict()
        for i in folder_name_and_file_name_list:
            label_prior = i[0]
            if label_prior == '.':
                label = 'UNKNOWN_LABEL'
            else:
                label = os.path.split(label_prior)[-1]
            files = pd.Series(i[1])
            label_files_dict.update({label:files})
        df = pd.DataFrame(label_files_dict)



    #保存成csv
    df.to_csv(GEN_CSV_PATH, index=False)
    df.to_excel(GEN_EXCEL_PATH, index=False)
    return 0
    ##################主要流程end####################


##############GUI######################
def Gui_Select_Path():
    Selected_Path = askdirectory()
    GUI_FOLDER_PATH.set(Selected_Path)
    global FOLDER_PATH_STR
    FOLDER_PATH_STR = Selected_Path
tk_root = tkinter.Tk()
FOLDER_PATH_STR = 0
GUI_FOLDER_PATH = tkinter.StringVar()

label1 = tkinter.Label(tk_root, text = "待解析目录:")
entry1 = tkinter.Entry(tk_root, textvariable = GUI_FOLDER_PATH)
button1 = tkinter.Button(tk_root, text = "路径选择:", command = Gui_Select_Path)
print(FOLDER_PATH_STR)
button2 = tkinter.Button(tk_root, text = "开始解析", command = main_function)
label1.pack()
entry1.pack()
button1.pack()
button2.pack()
tk_root.mainloop()