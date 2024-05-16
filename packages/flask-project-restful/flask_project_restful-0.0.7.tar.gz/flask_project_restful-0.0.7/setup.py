"""
- author:bichuantao
- creation time:2024/5/15
"""

from setuptools import setup, find_packages

# you need to change all these
VERSION = '0.0.7'
DESCRIPTION = "flask projects系列的restful自定义扩展"
long_description = "flask projects系列的第三方扩展-flask_project_restful"

setup(
    name="flask_project_restful",

    author="bichuantao",
    author_email='17826066203@163.com',

    keywords=['python', 'flask project', 'extends', 'flask_project_restful'],
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ababbabbb/flask_project_extends',
    license='MIT',

    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'flask',
        'flask-restful',
        'flask-p'
    ]
)
