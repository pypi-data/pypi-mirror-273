import setuptools
setuptools.setup(
    name="almgroad0770a",
    version="1.0",
    author="BKXBB",
    description="Is a FREE asynchronous library from reverse engineered Shazam API written in Python 3.6+ with asyncio and aiohttp. Includes all the methods that Shazam has, including searching for a song by file.",
    long_description="Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum and first released in 1991, Python emphasizes code readability with its clear and concise syntax, making it an ideal language for beginners and experienced programmers alike.Python supports multiple programming paradigms, including procedural, object-oriented, and functional programming. It offers dynamic typing and automatic memory management, which simplifies development by reducing the amount of code needed to perform tasks compared to lower-level languages.Python has a vast ecosystem of libraries and frameworks, making it suitable for a wide range of applications, from web development and data analysis to artificial intelligence and scientific computing. Popular frameworks such as Django and Flask are widely used for building web applications, while libraries like NumPy and Pandas are essential for data manipulation and analysis.One of Pythons key strengths is its strong community support and active development, with a large number of contributors continuously improving the language and its ecosystem.",
    long_description_content_type="text/markdown",
    url="https://github.com/dotX12/ShazamIO",
    packages=setuptools.find_packages(),
    
    install_requires=[
        "requests",
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)