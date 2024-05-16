from setuptools import setup, find_packages

setup(
    name = 'qnn',
    packages = find_packages(exclude=['examples']),
    version = '0.0.0a',
    license='MIT',
    description = 'Quantize Neural Network',
    author = 'JiauZhang',
    author_email = 'jiauzhang@163.com',
    url = 'https://github.com/JiauZhang/qnn',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = 'text/markdown',
    keywords = [
        'Deep Learning',
        'Quantize Neural Network',
        'Artificial Intelligence',
    ],
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)