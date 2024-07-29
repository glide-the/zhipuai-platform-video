#### 开放平台视频生成批量操作

#### 1. 项目简介
本项目是基于开放平台的视频生成批量操作，主要包括视频生成功能，提交包含input_text,image_path字段的的level_contexts.xlsx文件

input_text：文本内容
image_path: 图片绝对路径

输出结果为视频任务id


#### 使用

- 安装依赖
```shell
pip install zhipuai-platform-video -U

```


- 设置环境变量
```shell
export ZHIPUAI_API_KEY="开放平台key" 
```

- 运行

> 启动目录为项目根目录

```shell
python -m zhipuai_platform_video.start --input_excel C:\\Users\\renrui\\Desktop\\data\\level_contexts.xlsx --output_path C:\\Users\\renrui\\Desktop\\data\\
```

> 参数说明
> 
> input_excel：为包含input_text,image_path字段的的level_contexts.xlsx文件
> 
> output_path：为输出文件路径，生成 video_report.csv文件
> 
> 可以断点续传，会自动跳过已经生成的任务, 
> 
> 根据需要配置线程
> 
> prompt_num_threads: 提示词线程数,默认2
> 
> video_num_threads: 视频生成线程数,默认1
> 

- 获取任务结果 

> 启动目录为项目根目录
```shell
python -m zhipuai_platform_video.video_pull --task_video_csv C:\\Users\\renrui\\Desktop\\data\\video_report.csv --output_path C:\\Users\\renrui\\Desktop\\data\\
```
> 参数说明
> 
> input_excel： video_report.csv文件
> 
> output_path：为输出文件路径 生成video_pull_report.csv文件
> 
> 会自动跳过已经获取的任务, 删除根目录cache_data/VideoPullGenerator的文件可以重新获取
> 
> 根据需要配置线程
> 
> num_threads: 线程数,默认2
> 


- 下载视频 

> 启动目录为项目根目录
```shell
python -m zhipuai_platform_video.download_video  --csv_file_path  C:\\Users\\renrui\\Desktop\\data\\video_pull_report.csv --output_path C:\\Users\\renrui\\Desktop\\data\\

```
> 参数说明
> 
> csv_file_path： video_pull_report.csv文件
> 
> output_path：为输出文件路径 视频下载目录
>   
> 