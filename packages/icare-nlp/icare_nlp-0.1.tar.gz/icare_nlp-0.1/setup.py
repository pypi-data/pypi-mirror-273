from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
VERSION = '0.1'
DESCRIPTION = 'From CV detection to answer questions'
# 配置
setup(
    name="icare_nlp",
    version=VERSION,
    author_email="23037086r@connect.polyu.hk",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    package_data={
        "icare_nlp": ["resources/*", "*"],
    },
    include_package_data=True,
    install_requires=[],
    keywords=['icare', 'language']
)