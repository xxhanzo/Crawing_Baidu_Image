# Crawing_Baidu_Image
优点：优化了selenium某块，即不需要浏览器及浏览器驱动即可爬取

# 1.安装必要的软件

> 确保系统已更新，且安装了python3和pip，如已安装请忽略此步骤。

```Python
sudo apt update
sudo apt upgrade
```

# 2.设置虚拟环境

```Python
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
```

# 3.安装Flask和依赖

```Python
pip install -r requirements.txt
```

# 4.运行

1. 激活虚拟环境（为自己创建的虚拟环境）

   1. ```Python
      source myenv/bin/activate
      ```

2. cd到``/root/MyPycharmProject`` 文件夹下，执行

   1. ```Python
      python Crawing_Images.py 
      ```

# 6.使用

运行成功后应该能看到以下信息：

![image](https://github.com/user-attachments/assets/b7fa4a01-b6f1-4bf2-bf2d-584cd2d7a27b)


1. 在本地执行命令：

```Python
curl -X POST http://127.0.0.1:8000/crawl_images -H "Content-Type: application/json" -d "{\"query\": \"溃坝\", \"num_images\":110}"
```

1. 其中：
   1. 端口号设置为：8000
   2. `` ``http://127.0.0.1:8000````改为本机地址
   3. ``"{\"query\": \"溃坝\", \"num_images\": 10}"``中的``query``为要搜索的内容，``10`` 为要搜索的数量。
2. 运行结果：

![fa6a8c29eeaba70420d11d1a1f8d7cf](https://github.com/user-attachments/assets/8ed758d6-afe4-4ae7-aa85-2953edc983b6)

