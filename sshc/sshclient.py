import os
import paramiko
import sys
sys.path.append("../")
from paramiko.client import AutoAddPolicy
from paramiko.client import SSHClient
from .otherTools import OtherTools
from adptransf.logger import logger


class MySSHClient:
    def __init__(self):
        self.ssh_client = SSHClient()

    # 连接登录
    def connect(self, hostname, port, username, password):
        try:
            logger.info('正在远程连接主机：%s' % hostname)
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
            return [True, '']
        except Exception as e:
            logger.error('连接出错了%s' % e)
            return [False, '%s' % e]

    # 列出目录文件 ls
    def listdir(self, path):
        # sftp = paramiko.SFTPClient.from_transport(self.ssh_client)
        try:
            sftp_client = self.ssh_client.open_sftp()
            # print('正在下载远程文件：%s 到本地：%s' % (remotepath, localpath))
            # sftp_client.get(remotepath, localpath)
            listdir = sftp_client.listdir(path)
            return listdir
        except Exception as e:
            raise e
        finally:
            sftp_client.close()

    # 远程执行命令
    def exec_command(self, command):
        try:
            logger.info('正在执行命令：'+ command)
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            logger.info('命令输出：')
            logger.info(stdout.read()) # 读取命令输出
            return [True, tuple]
        except Exception as e:
            logger.error('执行命令: %s出错' % command)
            return [False,'%s' % e]

    # 下载文件(非目录文件)
    def download_file(self, remotepath, localpath):
        try:
            localpath = os.path.abspath(localpath)
            localpath = localpath.replace('\t', '/t').replace('\n', '/n').replace('\r', '/r').replace('\b', '/b') # 转换特殊字符
            localpath = localpath.replace('\f', '/f')
            logger.info('转换后的本地目标路径为：%s' % localpath)
            head, tail = os.path.split(localpath)
            if not tail:
                logger.warning('下载文件：%s 到本地：%s失败，本地文件名不能为空' % (remotepath, localpath))
                return [False, '下载文件：%s 到本地：%s失败，本地文件名不能为空' % (remotepath, localpath)]
            if not os.path.exists(head):
                logger.info('本地路径：%s不存在，正在创建目录' % head)
                OtherTools().mkdirs_once_many(head)

            sftp_client = self.ssh_client.open_sftp()
            logger.info('正在下载远程文件：%s 到本地：%s' % (remotepath, localpath))
            sftp_client.get(remotepath, localpath)
            sftp_client.close()
            return [True, '']
        except Exception as e:
            logger.error('下载文件：%s 到本地：%s 出错:%s' % (remotepath, localpath, e))
            return [False, '下载文件：%s 到本地：%s 出错:%s' % (remotepath, localpath, e)]

    # 下载文件(非目录文件)
    def remove_file(self, remotepath):
        try:
            sftp_client = self.ssh_client.open_sftp()
            sftp_client.remove(remotepath)
            logger.info('删除文件：%s 成功:%s' % (remotepath))
        except Exception as e:
            logger.error('删除文件：%s 出错:%s' % (remotepath, e))
            return [False, '删除文件：%s 出错:%s' % (remotepath, e)]


    # 上传文件(非目录文件）
    def upload_file(self, localpath, remotepath):
        try:
            localpath = localpath.rstrip('\\').rstrip('/')
            localpath = localpath.replace('\t', '/t').replace('\n', '/n').replace('\r', '/r').replace('\b', '/b') # 转换特殊字符
            localpath = localpath.replace('\f', '/f')
            localpath = os.path.abspath(localpath)
            logger.info('转换后的本地文件路径为：%s' % localpath)

            remotepath = remotepath.rstrip('\\').rstrip('/')
            head, tail = os.path.split(localpath)
            if not tail:
                logger.error('上传文件：%s 到远程：%s失败，本地文件名不能为空' % (localpath, remotepath))
                return [False, '上传文件：%s 到远程：%s失败，本地文件名不能为空' % (localpath, remotepath)]
            if not os.path.exists(head):
                logger.error( '上传文件：%s 到远程：%s失败，父路径不存在' % (localpath, remotepath, head))
                return [False, '上传文件：%s 到远程：%s失败，父路径不存在' % (localpath, remotepath, head)]

            if not (remotepath.startswith('/') or remotepath.startswith('.')):
                logger.error('上传文件：%s 到远程：%s失败，远程路径填写不规范%s' % (localpath, remotepath,remotepath))
                return [False, '上传文件：%s 到远程：%s失败，远程路径填写不规范%s' % (localpath, remotepath,remotepath)]
            sftp_client = self.ssh_client.open_sftp()
            head, tail = os.path.split(remotepath)

            head = sftp_client.normalize(head) # 规范化路径
            remotepath = head + '/' + tail
            logger.info('规范化后的远程目标路径：', remotepath)

            logger.info('正在上传文件：%s 到远程：%s' % (localpath, remotepath))
            sftp_client.put(localpath, remotepath)
            sftp_client.close()
            return [True, '']
        except Exception as e:
            logger.error('上传文件：%s 到远程：%s 出错:%s' % (localpath, remotepath, e))
            return [False, '上传文件：%s 到远程：%s 出错:%s' % (localpath, remotepath, e)]

    def close(self):
        self.ssh_client.close()