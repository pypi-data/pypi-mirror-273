from setuptools import setup, find_packages

VERSION = '1.3'
DESCRIPTION = 'Binary polarity detection'
LONG_DESCRIPTION = '''A fine-tuned DistilBERT model for binary polarity detection in text.
                        Returns 1 if detected positive; 0 if detected negative.'''

# Setting up
setup(
    name="binpolar",
    version=VERSION,
    author="Joyce Lee",
    author_email="<leejoy1610@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['transformers', 'huggingface_hub'],
    keywords=['python', 'text', 'polarity'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)