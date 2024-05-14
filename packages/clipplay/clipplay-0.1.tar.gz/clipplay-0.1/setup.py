from setuptools import setup, find_packages

setup(
    name='clipplay',
    version='0.1',
    packages=find_packages(),
    install_requires=['pyperclip'],
    author='Kaneki',
    author_email='kaneki@admin.com',
    description='A package to interact with clipboard and display its content.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/malanalysis2',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
