# coding=utf-8

# from gevent import monkey
# monkey.patch_all()
# import multiprocessing

debug = True
# 修改代码时自动重启
reload = True
#
reload_engine = 'inotify'
# //绑定与Nginx通信的端口
bind = '127.0.0.1:3002'
#bind = 'unix:/data/wwwroot/luejiao.com/tmp/gunicorn.sock'
pidfile = 'log/gunicorn.pid'

workers = 4  # 进程数
# workers = multiprocessing.cpu_count() * 2 + 1 #进程数

#worker_class = 'uvicorn.workers.UvicornWorker'  # 默认为阻塞模式，最好选择gevent模式,默认的是sync模式
# 日志级别
# debug:调试级别，记录的信息最多；
# info:普通级别；
# warning:警告消息；
# error:错误消息；
# critical:严重错误消息；
loglevel = 'debug'
# 访问日志路径
accesslog = './log/gunicorn_access.log'
# 错误日志路径
errorlog = './log/gunicorn_error.log'
# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
