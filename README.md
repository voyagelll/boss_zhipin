
# boss_zhipin职位爬取和分析
项目主要是爬取boss直聘并分析职位数据。

## 爬取(职位自行改，城市需要拿到正确的城市代码。（城市代码url：https://www.zhipin.com/common/data/city.json ）
* 爬取职位：爬虫，数据分析，数据挖掘。

* 爬取城市：北京，上海，广州，深圳，杭州，苏州，武汉，成都，厦门，西安。

* 字段：{"_id" ,"job", "salary" ,"location" ,"experience","degree" ,"bonus","job_desc","requirements" ,"company" ,"staff_num" ,"release_time"}

## 职位分析
#### 一、数据详情
* 共有3350条职位数据关于（爬虫，数据分析，数据挖掘）
* 包含的字段：福利，公司名，学历要求，工作经验，职位名称，职位描述，地点，发布时间，能力要求，薪水，员工人数，职位简称
#### 二、问题
* 1.三种职位占比
* 2.职位地区分布
* 3.职位要求（学历，工作经验）
* 4.薪水的地区分布及区间分布
* 5.职位数与发布时间的关系
* 6.工作内容
* 7.能力要求

#### 主要文件
* boss_zhipin_spider: 职位爬取
* jobs.ipynb: 职位数据分析
* stopwords.txt: 分隔词 

#### 需要安装的包：
* requests
* pymongo
* pyecharts
* numpy
* pandas
* jieba
* fake_useragent 
* redis
