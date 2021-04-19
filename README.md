2021/04/19: 更新了一下羽毛球预约的东西。需要使用的话欢迎查看源码或直接找我。

2021/03/10: 更新了一点点新问题。问题表现：返回错误信息为“位置信息为空”。

# AutoAction
每天自动提交平安复日。 代码主体参考 [k652](https://github.com/k652)



## 📃免责声明

本项目仅作技术交流，请根据自身实际情况进行打卡。对一切非法使用所产生的后果，本项目概不负责。



## 📑程序说明

在每天北京时间8:05（实际是8:49）自动提交平安复旦，其中地理位置延续上次提交的位置。提交结果以邮件形式返回到个人邮箱中。

自动预约羽毛球场地，默认周一周三16:00-17:00



## 📗使用方法 



### 快速使用

fork完之后在自己repo中setting的secrets添加如下字段：

- `USERNAME`:  学号

- `PASSWORD`: 密码

- `EMAIL`: 用于接收通知的邮箱

  不打算使用自动预约羽毛球的话可以去./.github/workflows把Badminton.yml删了

### 进阶使用

自动提交时间可以在./.github/workflows/report.yml中修改。

（.yml文件使用方法详见[官方文档](https://docs.github.com/en/free-pro-team@latest/actions/creating-actions/about-actions#versioning-your-action)

由于时差因素，不建议将时间改为北京时间8点以前。

