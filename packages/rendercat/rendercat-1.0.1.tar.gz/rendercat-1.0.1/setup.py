from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def requirements():
    with open('REQUIREMENTS.txt', 'r') as f:
        res = []
        for i in f:
            res.append(i)
        return res


setup(
    name='rendercat',
    version='1.0.1',
    author='TimofeyFilkin',
    author_email='timofejfilkin@gmail.com',
    description='3D engine made for pygame',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/TimofeyFilkin/RenderCat',
    packages=find_packages(),
    install_requires=requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='python 3d opengl pygame',
    project_urls={},
    python_requires='>=3.7'
)
