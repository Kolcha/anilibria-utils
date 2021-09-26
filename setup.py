import setuptools

setuptools.setup(
    name="anilibria-utils",
    version="0.1.0",
    author="Nick Korotysh",
    author_email="kolchaprogrammer@list.ru",
    description="download torrents from www.anilibria.tv",
    url="https://github.com/Kolcha/anilibria-utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['lxml', 'requests'],
    python_requires='>=3.6',
)
