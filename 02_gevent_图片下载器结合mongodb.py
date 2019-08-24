# 这个文件需要切换到python3，不用E盘的虚拟环境

from pymongo import MongoClient
import pandas as pd
import requests
import gevent
import re


# from gevent import monkey
# monkey.patch_all()  # 这里由于没有用到time.sleep()等时间延迟，所以可以不要
# 下载数据，有时可以延迟一下，如果网站有反爬机制，可以在第47行代码前面设置time.sleep()

def get_books_info():
    """从mongodb数据库中提取图书的名称和图片的信息"""
    client = MongoClient()
    collection = client['bookschina_books']['books']  # 爬虫数据存储在mongo中
    data = collection.find()  # 获取全部数据信息

    pd.set_option('display.max_columns',None)  # 控制台输出全部的行信息，不输出省略号
    df = pd.DataFrame(data)
    # print(df.info())
    # print(df.head(1))

    # 提取数据，先将数据提取到一个字典当中
    books_info = list()
    # 去除可能存在的空值
    df = df[pd.notnull(df['img'])]
    # 提取数据，并拼接成一个列表
    img_urls = df['img'].str.split(',').tolist()
    bnames = df['bname'].str.split(',').tolist()

    for i in range(len(img_urls)):
        books_item = dict()
        # TODO：需要对书名进行处理，带有[\ / : * ? < > " |]的要去掉（文件命名不能有冒号） 【已处理，见正则表达式】
        # 唐诗三百首:插图.赏析.注释.译意( 最新版)(附光盘)
        # books_item['book_name'] = bnames[i][0]
        books_item['book_name'] = re.sub(r'[/\\:<>"*|]*', '', bnames[i][0])
        books_item['img_url'] = img_urls[i][0]
        books_info.append(books_item)

    print(books_info)
    return books_info

def imgs_download(file_name, img_url):
    """图片下载"""
    img_data = requests.get(img_url)  # 获取图片数据

    # 保存图片到books_imgs文件夹中
    with open(file_name, 'wb') as f:
        f.write(img_data.content)

def main():

    # 获取数据
    books_info = get_books_info()
    # 创建协程多任务 【任务的创建可以参考26.gevent图片下载器】
    # 这里是构建一个gevent.spawn的任务队列的列表，参数是 imgs_download     file_name       img_url
    task_list = [(gevent.spawn(imgs_download, './books_imgs/' + i['book_name'] + '.jpg', i['img_url'])) for i in books_info]
    print('-----任务开始-----')

    gevent.joinall(task_list)
    print('----图片下载完成----')


if __name__ == '__main__':
    main()
    # get_books_info()


# books_info:(这里只截取一部分内容)
# [{'book_name': '(单张)宣纸手工雕版印刷--飞天', 'img_url': 'http://image31.bookschina.com/images/feng200.jpg'},
# {'book_name': '曾 几何时', 'img_url': 'http://image12.bookschina.com/2015/20150201/s6647778.jpg'},
# {'book_name': '茧-张悦然作品集', 'img_url': 'http://image31.bookschina.com/2016/zuo/s7253626.jpg'},
# {'book_name': '话本小说史-孤本秘籍拾遗沥金', 'img_url': 'http://image31.bookschina.com/2018/zuo/12/s1826163.jpg'},
# {'book_name': '现身说法', 'img_url': 'http://image31.bookschina.com/2018/zuo/11/s6706148.jpg'},
# {'book_name': '慈悲', 'img_url': 'http://image12.bookschina.com/2015/20150726/s7088034.jpg'},
# {'book_name': '张爱玲全集03－ 怨女(2012版)', 'img_url': 'http://image12.bookschina.com/2012/20120713/s5564109.jpg'},
# {'book_name': '一句顶一万句', 'img_url': 'http://image12.bookschina.com/2016/20160821/s7261592.jpg'},
# {'book_name': '酒国-莫言文集-中国首位诺贝尔文学奖得主莫言代表作', 'img_url': 'http://image12.bookschina.com/2013/20130313/s5699677.jpg'},
# {'book_name': '三言两拍精编(全四册)', 'img_url': 'http://image31.bookschina.com/images/feng200.jpg'},
# {'book_name': '西游记-(图文速读本)', 'img_url': 'http://image31.bookschina.com/2010/20100829/s3214882.jpg'},
# {'book_name': '黄金时代', 'img_url': 'http://image12.bookschina.com/2018/20180406/s7388001.jpg'},
# {'book_name': '八仙传说', 'img_url': 'http://image31.bookschina.com/2006/061118/s1737573.jpg'},
# {'book_name': '唐诗三百首插图.赏析.注释.译意(最新版)(附光盘)', 'img_url': 'http://image12.bookschina.com/2013/20131007/s1930201.jpg'},
# {'book_name': '西厢记', 'img_url': 'http://image30.bookschina.com/1/1.10/s1152996.jpg'},
# {'book_name': '蒙古苍狼世人最崇敬的蒙古之王.成吉思汗', 'img_url': 'http://image31.bookschina.com/small/36/23/1874236.jpg'},]
