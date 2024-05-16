from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    # 包名
    name='miraihttpapi',

    # 版本号
    version='1.3',

    # 简短描述
    description='Use mirai-api-http(v2+) http polling to interconnect the interface',
    keywords=("mirai", "api"),


    long_description_content_type='text/markdown',
    long_description=open('README.md',"r",encoding='utf-8').read(),
    

    # 项目主页
    url='http://www.icedream.space',

    # 作者信息
    author='Esdrin',
    author_email='esdrin@icedream.space',

    # 许可证
    license='MIT LICENSE',

    # 包含的包（find_packages() 会自动查找所有包和子包）
    packages=find_packages(
        include=['miraihttpapi']
        ),

    # 依赖列表
    install_requires=[
        'PyYAML',
        'requests',
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
