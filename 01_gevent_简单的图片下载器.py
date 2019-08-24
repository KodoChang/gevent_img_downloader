from gevent import monkey
import gevent
import requests


# monkey.patch_all()

def img_down(file_name, img_url):
    """图片下载器"""

    img_data = requests.get(img_url)
    with open(file_name, 'wb') as f:
        f.write(img_data.content)

# './imgs/1.jpg'
# 这里一开始是导入time，使用时间戳作为图片的名字，但是不行
# 每次执行后只有1张或2张图片，gevent几乎是同时执行的，时间戳也会相同，图片彼此覆盖了
gevent.joinall([
    gevent.spawn(img_down, './imgs/'+'1.jpg', "http://image31.bookschina.com/images/feng200.jpg"),
    gevent.spawn(img_down, './imgs/'+'2.jpg', "http://image12.bookschina.com/2015/20150201/s6647778.jpg"),
    gevent.spawn(img_down, './imgs/'+'3.jpg', "http://image31.bookschina.com/2016/zuo/s7253626.jpg"),
    gevent.spawn(img_down, './imgs/'+'4.jpg', "http://image31.bookschina.com/2018/zuo/12/s1826163.jpg")
])
