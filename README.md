# mysite

#Django的官方举例
https://docs.djangoproject.com/zh-hans/2.0/

1. URL请求过来
2. 到项目下的urls.py，根据urlpatterns过滤到对应的app，维护的是请求与app.urls的关系
3. 转到app内的urls.py，根据urlpatterns过滤到对应请求的views页面，维护的是app内的url与views的关系

	
改变模型需要这三步：
	1. 编辑 models.py 文件，改变模型。
	2. 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
	3. 运行 python manage.py migrate 来应用数据库迁移。
数据库迁移被分解成生成和应用两个命令是为了让你能够在代码控制系统上提交迁移数据并使其能在多个应用里使用；这不仅仅会让开发更加简单，也给别的开发者和生产环境中的使用带来方便。
