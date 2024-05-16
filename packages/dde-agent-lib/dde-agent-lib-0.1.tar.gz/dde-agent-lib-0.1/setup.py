from setuptools import setup, find_packages

setup(
    name='dde-agent-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[

    ],
    # 其他元数据
    author='geogpt',
    author_email='zhuquezhitu@zhejianglab.com',
    description='geogpt agent library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)