#### 开放平台视频生成批量操作

#### 1. 项目简介
本项目是基于开放平台的视频生成批量操作，主要包括视频生成功能，提交包含input_text,image_path字段的的level_contexts.xlsx文件

input_text：文本内容
image_path: 图片绝对路径

输出结果为视频任务id


#### 试用

- 安装依赖
```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

```


- 设置环境变量
```shell
export ZHIPUAI_API_KEY="开放平台key" 
···

- 运行

> 启动目录为项目根目录
```shell
python start.py --input_excel C:\\Users\\renrui\\Desktop\\data\\level_contexts.xlsx --output_path C:\\Users\\renrui\\Desktop\\data\\
```

> 参数说明
> input_excel：为包含input_text,image_path字段的的level_contexts.xlsx文件
> output_path：为输出文件路径
> 可以断点续传，会自动跳过已经生成的任务, 
> 根据需要配置线程
> prompt_num_threads: 提示词线程数,默认2
> video_num_threads: 视频生成线程数,默认1
> 

- 获取任务结果 

> 启动目录为项目根目录
```shell
python video_pull.py --task_video_csv C:\\Users\\renrui\\Desktop\\data\\video_report.csv --output_path C:\\Users\\renrui\\Desktop\\data\\
```
> 参数说明
> input_excel：为包含input_text,image_path字段的的level_contexts.xlsx文件
> output_path：为输出文件路径
> 会自动跳过已经获取的任务, 删除根目录cache_data/VideoPullGenerator的文件可以重新获取
> 根据需要配置线程
> num_threads: 线程数,默认2