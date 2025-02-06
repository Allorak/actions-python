from setuptools import setup, find_packages

setup(
    name="actions-python",
    version="0.3.0",
    author="Mike Moiseev",
    author_email="mvmoiseev@miem.hse.ru",
    description="A simple Python packaging for managing event-like actions and validating handlers argument types.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Allorak/actions-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English"
    ],
    python_requires='>=3.8'
)
