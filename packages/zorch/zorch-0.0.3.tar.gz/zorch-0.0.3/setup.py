
import re
from setuptools import setup, find_packages


def increment_version():
    # 读取文件
    with open('./zorch/__init__.py', 'r') as f:
        # 找到 对应的版本号
        version_line = f.read()  #
        match = re.search(r'(\d+\.\d+\.\d+)', version_line)
       
        if not match:
            raise ValueError("Unable to find version string")

        # 解析版本号的部分
        major, minor, patch = map(int,match.group(1).split('.'))
        # 增加 PATCH 部分
        patch += 1
        # 重建版本号字符串
        new_version = f"{major}.{minor}.{patch}"

    # 重新打开文件以写入模式
    with open('./zorch/__init__.py', 'w') as f:
        # 写入到原始位置,不修改其他内容
        f.write("__version__ = '{}'\n".format(new_version))
        
    return new_version
    
version = increment_version()


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

