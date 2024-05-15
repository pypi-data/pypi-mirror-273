from setuptools import setup, find_packages

setup(
    # 包名
    name='l2dexapi',

    # 版本号
    version='1.2',

    # 简短描述
    description='与Live2DViewerEX相互通信',


    # 项目主页
    url='http://www.icedream.space',

    # 作者信息
    author='Esdrin',
    author_email='esdrin@icedream.space',

    # 许可证（您没有提供许可证信息，这里暂时留空）
    license='MIT License',

    # 包含的包（find_packages() 会自动查找所有包和子包）
    packages=find_packages(
        include=['L2dvExApi']
        ),

    # 依赖列表
    install_requires=[
        'websocket',
    ],

    # 其他选项，如zip_safe等
    zip_safe=False,

    # 类别
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
