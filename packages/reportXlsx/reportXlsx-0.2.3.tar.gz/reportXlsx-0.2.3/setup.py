from setuptools import setup, find_packages

setup(
    name='reportXlsx',
    version='0.2.3',
    packages=find_packages(),
    package_data={
        'reportXlsx': ['resources/*.xml','resources/*.dll'],
    },
    include_package_data=True,
    install_requires=[
        'pandas','openpyxl','pythonnet','xlwings'
    ],
    description='这是一个操作xlsx的库',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bailulue',
    author='bailu',
    author_email='yabailu@chinatelecom.cn'
)
