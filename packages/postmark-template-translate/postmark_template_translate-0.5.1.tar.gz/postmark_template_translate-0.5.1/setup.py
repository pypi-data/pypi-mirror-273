from setuptools import setup, find_packages

setup(
    name='postmark-template-translate',
    version='0.5.1',
    packages=find_packages(include=['app', 'app.*']),  # Incluye todos los subpaquetes
    install_requires=[
        'postmarker',
        'beautifulsoup4',
        'googletrans==4.0.0-rc1',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            # Aquí puedes definir comandos de consola si es necesario
        ],
    },
    author='Daniel Alvarado',
    author_email='dani.alvarado@kirbic.com',
    description='A library to send Postmark templates with translated content',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DanielDls-exe/postmark_template_translate',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

