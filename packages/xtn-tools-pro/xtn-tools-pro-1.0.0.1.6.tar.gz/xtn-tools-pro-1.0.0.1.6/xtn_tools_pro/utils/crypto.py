#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 说明：
#    加解密、编解码
# History:
# Date          Author    Version       Modification
# --------------------------------------------------------------------------------------------------
# 2024/5/13    xiatn     V00.01.000    新建
# --------------------------------------------------------------------------------------------------
import base64
import hashlib


def get_md5_32(s: str, is_upper=False):
    """
        获取文本的md5值 32位
    :param s: 文本
    :param is_upper: 是否转大写 默认False
    :return:
    """
    # s.encode()#变成bytes类型才能加密
    m = hashlib.md5(s.encode())  # 长度是32
    if is_upper:
        return m.hexdigest().upper()
    return m.hexdigest()


def get_md5_16(s: str, is_upper=False):
    """
        获取文本的md5值 16位
    :param s: 文本
    :param is_upper: 是否转大写 默认False
    :return:
    """
    result = get_md5_32(s, is_upper)
    return result[8:24]


def get_binary_content_md5_32(content, is_upper=False):
    """
        二进制内容md5 例如图片
    :param content: 二进制内容
    :param is_upper: 是否转大写 默认False
    :return:
    """
    md5_hash = hashlib.md5(content)
    md5_hexdigest = md5_hash.hexdigest()
    if is_upper:
        return md5_hexdigest.upper()
    return md5_hexdigest


def get_binary_content_md5_16(content, is_upper=False):
    """
        二进制内容md5 例如图片
    :param content: 二进制内容
    :param is_upper: 是否转大写 默认False
    :return:
    """
    result = get_binary_content_md5_32(content, is_upper)
    return result[8:24]


def get_file_md5_32(file_path, is_upper=False):
    """
        获取文件md5值
    :param file_path: 文件路径
    :param is_upper: 是否转大写 默认False
    :return:
    """
    with open(file_path, 'rb') as file:
        data = file.read()
        md5_hash = hashlib.md5(data).hexdigest()
    if is_upper:
        return md5_hash.upper()
    return md5_hash


def get_file_md5_16(file_path, is_upper=False):
    """
        获取文件md5值
    :param file_path: 文件路径
    :param is_upper: 是否转大写 默认False
    :return:
    """
    result = get_file_md5_32(file_path, is_upper)
    return result[8:24]


def get_sha1(s: str, is_upper=False):
    """
        sha1
    :param s: 文本
    :param is_upper: 是否转大写 默认False
    :return:
    """
    # 使用sha1算法进行哈希
    sha1_hash = hashlib.sha1(s.encode()).hexdigest()
    if is_upper:
        return sha1_hash.upper()
    return sha1_hash


def get_base64_encode(s: str):
    """
        base64 编码
    :param s: 文本
    :return:
    """
    # 将字符串编码为 bytes
    data_bytes = s.encode('utf-8')
    # 使用 base64 进行编码
    encoded_bytes = base64.b64encode(data_bytes)
    # 将编码后的 bytes 转换为字符串
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string


if __name__ == '__main__':
    print(get_base64_encode(''))
