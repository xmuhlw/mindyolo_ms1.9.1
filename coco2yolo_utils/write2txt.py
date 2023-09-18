
# 将images路径写到txt文本中，用于yolo格式

import os
import os.path

if __name__ == "__main__":
    # pic_path = 'data/custom/images/train/'   # 要遍历的图片文件夹路径
    # save_txtfile = open('data/custom/train.txt','w') # 保存路径的记事本文件
    pic_path = '/home/ma-user/work/data/images/val2017'   # 要遍历的图片文件夹路径
    save_txtfile = open('/home/ma-user/work/data/val2017.txt','w') # 保存路径的记事本文件
    # i = 0
    for root, dirs, files in os.walk(pic_path): 
# root 所指的是当前正在遍历的这个文件夹的本身的地址
# dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
# files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
        for file in files:
            print(os.path.join(root,file))
            # save_txtfile.write(os.path.join(root,file) + ' ' + str(i) +'\n')
            save_txtfile.write(os.path.join(root,file) +'\n')
    print('The files path of ' + str(pic_path) + 'has already written to' + str(save_txtfile) )
    save_txtfile.close();

