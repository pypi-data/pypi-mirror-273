from setuptools import setup, find_packages

setup(
    # 包名
    name='L2dvEXApi',

    # 版本号
    version='1.1',

    # 简短描述
    description='API for Live2DViewerEX',
    keywords=("live2d", "api"),

    # 详细描述
    long_description_content_type='text/markdown',
    long_description=open('README.md',"r",encoding='utf-8').read(),

    # 项目主页
    url='http://www.icedream.space',

    # 作者信息
    author='Esdrin',
    author_email='esdrin@icedream.space',

    # 许可证
    license='MIT License',

    # 包含的包（find_packages() 会自动查找所有包和子包）
    packages=find_packages(
        include=['L2dvExApi']
        ),

    # 依赖列表
    install_requires=[
        'websocket-client',
    ],

    # 其他选项，如zip_safe等
    zip_safe=False,
    
    # 平台
    platforms="any",

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
