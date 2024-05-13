from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lxs-SimpleTools',
    version='1.0.2',
    author='liuxiansong',
    author_email='326427540@qq.com',
    description='处理字符串和时间简单工具函数',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),  # 自动查找并包含所有的包
    install_requires=[

    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)