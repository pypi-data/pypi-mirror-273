
import re
from setuptools import setup, find_packages

from importlib_metadata import version

def increment_version(version_str):
    # 使用正则表达式匹配版本号的部分
    match = re.match(r'(\d+\.\d+\.\d+)', version_str)
    if not match:
        raise ValueError("Invalid version string")
    # 解析版本号的部分
    major, minor, patch = map(int, match.group(0).split('.'))
    # 增加 PATCH 部分
    patch += 1
    # 重建版本号字符串
    new_version = f"{major}.{minor}.{patch}"
    return new_version

def get_package_version(package_name):
    try:
        return version(package_name)
    except:
        return "0.0.0"
curr_version = get_package_version('zorch')
version = increment_version(curr_version)


print("zorch version:", type(version), version)
setup(
    name='zorch',
    version=version,
    author='zwhy',
    author_email='zwhy2025@gmail.com',
    description='A brief description of the package',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your_package_name',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类器列表
    ],
    python_requires='>=3.9',
)

