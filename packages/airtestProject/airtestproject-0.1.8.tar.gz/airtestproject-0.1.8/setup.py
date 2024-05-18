from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='airtestProject',
    version='0.1.8',
    packages=find_packages(include=['airtestProject', 'airtestProject.*']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "airtest==1.3.3",
        "openpyxl==1.1.0",
        "pocoui==1.0.94",
        "qrcode==7.4.2",
        "watchdog==4.0.0",
        "easyocr==1.7.1",
        "paddleocr==2.7.3",
        "loguru==0.5.3",
        "paddlepaddle==2.6.1",
        "numpy==1.22.4"
        # 项目依赖项列表
    ],
    python_requires='>=3.9',
    author="mortal_sjh",                                     # 作者
    author_email="mortal_sjh@qq.com"
)
