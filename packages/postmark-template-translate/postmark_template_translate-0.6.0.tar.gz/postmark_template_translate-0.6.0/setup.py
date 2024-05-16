from setuptools import setup, find_packages

setup(
    name='postmark_template_translate',
    version='0.6.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'postmarker',
        'beautifulsoup4',
        'googletrans==4.0.0-rc1',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    author='Daniel Alvarado',
    author_email='danieldls.ucv@gmail.com',
    description='A library to send Postmark templates with translated content',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DanielDls-exe/postmark_template_translate',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
