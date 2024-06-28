# ipython
基于百度、高德、腾讯地图api获取指定地区设施 

 #### python环境配置：

    1）python3.12.4 # https://www.python.org/downloads/
    2）pip # python -m ensurepip --upgrade
    3）pip install requests pandas 


 #### 文件定义:

    1）csv -> 存放处理前和处理后的csv文件
        1、processed -> 已处理csv文件
        2、untreated -> 未处理csv文件
    2）exl_file -> 处理后excel


 #### git: 
    # https://docs.github.com/zh
    1）git clone https://github.com/c-emo/ipython.git
    2）cd ipython
    3）git add .
    4）git commit -m "提交信息"
    5）git push -u origin mian

    # 从主分支上创建新分支
      1.git checkout main # 切到主分支
      2.git pull # 拉取最新代码
      3.git checkout -b 分支名 # 创建新分支
      4.git push -u origin 分支名 # 推送新分支到远程仓库
      5.git branch # 查看当前分支
      
    # 提交代码
      1.git pull  # 拉取最新代码
      2.git add . # 添加所有文件
      3.git commit -m "提交信息" # 提交代码
      4.git push origin 分支名 # 推送到远程仓库
