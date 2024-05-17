import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="InforeWss",
    version="1.0.1",
    author="wangdashuai",
    author_email="hanchaodaming@outlook.com",
    description="封装wss服务，可以快速连接，方便调试",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leslie110",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "websockets",
    ],
    python_requires='>=3.7',

)
