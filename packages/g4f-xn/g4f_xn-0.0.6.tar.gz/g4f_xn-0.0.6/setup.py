from setuptools import setup, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'library for easy access to GPT models based on g4f'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name="g4f_xn",
    version=VERSION,
    author="Xandr0v",
    author_email="<olegalexandrov468@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['g4f', 'pyaudio', 'pydub', 'colorama'],
    keywords=['python', 'g4f', 'gpt'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)