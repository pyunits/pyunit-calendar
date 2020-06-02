FROM python:3.8.3-alpine3.11
MAINTAINER Jytoui <jtyoui@qq.com>

EXPOSE 5000

# 加入pip源
ENV pypi https://pypi.douban.com/simple

# 安装flask插件
RUN pip install flask -i ${pypi}

# 工作目录
ENV DIR /mnt/pyunit-calendar
WORKDIR ${DIR}

COPY ./ ./

# 安装项目第三方库
RUN pip3 install whl/uWSGI-2.0.18-cp38-cp38-linux_x86_64.whl
RUN rm -rf whl/

CMD ["sh","app.sh"]