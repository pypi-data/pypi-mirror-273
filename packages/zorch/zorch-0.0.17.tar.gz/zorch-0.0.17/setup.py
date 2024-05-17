import re
from setuptools import setup, find_packages

# 读取当前版本号
with open('./zorch/__init__.py', 'r') as f:
    version_line = f.read()
    match = re.search(r'__version__ = \'(\d+\.\d+\.\d+)\'', version_line)
    if not match:
        raise ValueError("Unable to find version string")
    version = match.group(1)

print("zorch version:", version)

setup(
    name='zorch',
    version=version,
    author='zwhy',
    author_email='zwhy2025@gmail.com',
    description='pytorch使用过程中封装的常用模块',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类器列表
    ],
    python_requires='>=3.9',
)
