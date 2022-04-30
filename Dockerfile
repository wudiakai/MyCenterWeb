# 设置基础镜像
FROM python:3.10
# 设置代码文件夹工作目录 /app
WORKDIR /app
# 复制当前代码文件到容器中 /app
ADD . /app
# 设置时间
# RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# 安装所需的包，这里的requirements文件名需和项目生成的一致
RUN pip3 install -r requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
# 执行入口文件
CMD ["python", "main.py"]

# docker build --network=host -t centerserver:v1 .