# boss_zhipin职位爬取和分析 

#### 爬取的信息(职位自行改，城市需要拿到正确的城市代码（url：https://www.zhipin.com/common/data/city.json）)：

* 职位：爬虫，数据分析，数据挖掘。

* 城市：北京，上海，广州，深圳，杭州，苏州，武汉，成都，厦门，西安。

* 字段：{"_id" ,"job", "salary" ,"location" ,"experience","degree" ,"bonus","job_desc","requirements" ,"company" ,"staff_num" ,"release_time"}

#### 爬虫是两个进程实现的简单的分布式（还不完善），一个爬取职位url，另一个解析职位url并存储到mongodb。

#### 爬虫实现需要进程池

## 项目结构
