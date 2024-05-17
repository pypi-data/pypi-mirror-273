import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="lljz_tools",
    version="0.2.15.4",
    author="liulangjuanzhou",
    author_email="liulangjuanzhou@gmail.com",
    description="常用工具封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    package_data={
        "my_tools": ["*.html", "*.js"]
    },
    install_requires=['openpyxl', 'gevent', 'colorlog>=6.8.2'],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
