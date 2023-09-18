# MindYOLO_ms1.9.1

## 采用mindspore 1.9.1的镜像；
首先创建好8卡的资源后通过notebook连接服务器；
### 1. git载入对应的MindSpore的版本的模型，放在根目录；
```
git clone https://github.com/xmuhlw/mindyolo_ms1.9.1.git -b r0.1 

#MindSpore2.1之前不支持在910B上运行，另外910B的支持在逐步添加中,因此用r0.1的分支对应1.9.1的版本；
```
### 2. 通过modelarts的obs工具上传我们的数据，并且通过python来解压，因为自带的unzip指令无法解压超过5G的数据，并且数据与coco2017格式对应；
```
import moxing as mox
mox.file.copy('obs://fiveclasses-yoloformat/fiveclasses-yoloformat.zip')
```
```
import zipfile
f = zipfile.ZipFile("/home/ma-user/work/fiveclasses-yoloformat.zip")# 压缩文件位置
for file in f.namelist():
    f.extract(file,"/home/ma-user/work/data/")#解压位置
f.close()
```
### 3. 数据格式转换工具：*coco2yolo_utils*，因为自身数据集是COCO格式，而Mindyolo数据格式为yolo格式；
- coco2yolo.py: 
```
python ./coco2yolo_utils/coco2yolo.py --json_path ./XXX/XXX.json --save_path ./labels
```
将coco格式的json文件转成txt形式并存储在./lables文件下
- json_rename.py 
```
python ./coco2yolo_utils/json_rename.py 
```
若图片命名或者json文件中id,file_name等带有字符串需要重命名，json_rename.py可以实现图片跟json一一对应并且一键改名；
- write2txt.py 将图片绝对路径写入txt文件，以便于读图片；

### 4. 配置自己的yaml文件，配置文件主要包含数据集、数据增强、loss、optimizer、模型结构涉及的相应参数，由于MindYOLO提供yaml文件继承机制，可只将需要调整的参数编写为our_model.yaml，并继承MindYOLO提供的原生yaml文件即可，其内容如下：
```
__BASE__: [
  './configs/yolov8/yolov8m.yaml',
]

per_batch_size: 16 # 16 * 8 = 128
img_size: 640 # image sizes
weight: ./yolov8-m_500e_mAP505-8ff7a728.ckpt
strict_load: False

data:
  dataset_name: shwd
  train_set: /home/ma-user/work/data/train2017.txt
  val_set: /home/ma-user/work/data/val2017.txt
  test_set: /home/ma-user/work/data/val2017.txt
  nc: 5
  # class names
  names: [ 'crack', 'crul', 'dent', 'material' , 'nick']

optimizer:
  lr_init: 0.001  # initial learning rate
```
- __BASE__为一个列表，表示继承的yaml文件所在路径，可以继承多个yaml文件
per_batch_size和img_size分别表示单卡上的batch_size和数据处理图片采用的图片尺寸
- weight为上述提到的预训练模型的文件路径，strict_load表示丢弃shape不一致的参数
- log_interval表示日志打印间隔
- data字段下全部为数据集相关参数，其中dataset_name为自定义数据集名称，train_set、val_set、test_set分别为保存训练集、验证集、测试集图片路径的txt文件路径，nc为类别数量，names为类别名称
- optimizer字段下的lr_init为经过warm_up之后的初始化学习率，此处相比默认参数缩小了10倍
参数继承关系和参数说明可参考[configuration_CN.md](../../tutorials/configuration_CN.md)。

### 5. 模型代码调整，因为modelarts的显卡为Ascend 910B对MindSpore的动静统一的支持有限，因此采用r0.1分支对应的MindSpore 1.9.1版本，这边参考[#181 File Changes](https://github.com/mindspore-lab/mindyolo/pull/181/files)进行调整,支持pretrain模型的严格加载 *--strict_load = Trues*;
### 6. 下载[MODEL_ZOO](https://github.com/mindspore-lab/mindyolo/blob/master/MODEL_ZOO.md)对应yolo版本的pretrain模型，
### 7.安装依赖
- mindspore >= 1.8.1
- numpy >= 1.17.0
- pyyaml >= 5.3
- openmpi 4.0.3 (for distributed mode)
安装这些依赖，请执行以下命令
```shell
pip install -r requirements.txt
```
### 8.执行多卡训练
```
mpirun --allow-run-as-root -n 8 python train.py --config ./our_model.yaml --is_parallel True
```