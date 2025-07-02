from setuptools import setup, find_packages

setup(
    name='operator_whl_test',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],  # 可添加依赖
    entry_points={
        'console_scripts': [
            'operator_whl_test=operator_whl_test.main:main'
        ]
    },
    author='Your Name',
    description='A test operator for building .whl files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
)
