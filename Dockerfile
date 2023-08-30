FROM bids/freesurfer:v6.0.1-6.1
MAINTAINER Chenfei <chenfei.ye@foxmail.com>

# install pybids
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ pybids	

COPY ./ /
RUN chmod 777 /run_fs_batch.py /hcpmmp_conv.py /run.py
CMD ["python", "/run.py"]
