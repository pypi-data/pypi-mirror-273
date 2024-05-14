from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='adb_tool_py',
    version='0.0.2',
    author='Shota Iuchi',
    author_email='shotaiuchi.develop@gmail.com',
    description='adb_tool_py is a tool for Android Debug Bridge (adb).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ShotaIuchi/adb-tool-py',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=[
        'chardet',
    ],
    include_package_data=True
)
