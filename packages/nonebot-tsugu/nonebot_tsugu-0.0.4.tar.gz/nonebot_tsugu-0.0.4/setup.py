from setuptools import find_packages, setup


with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='nonebot_tsugu',
    version='0.0.4',
    author='otae',
    author_email='otae1204@qq.com',
    description='基于tsugu-bangdream-bot项目实现的nonebot2插件',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/otae-1204/NoneBot-Tsugu',
    include_package_data=False,
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.10',
    install_requires=[
        'httpx>=0.18.2',
        "nonebot2>=2.0.0",
        "nonebot-adapter-onebot",
    ]
)