import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StatAssist",
    version="1.0.1",
    license='MIT',
    author="Damion J. Quintanilla",
    author_email="djq314159@gmail.com",
    description="Math tools for private or personal use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'torch>=2.3.0',
        'pandas>=2.2.2',
        'scikit-learn>=1.4.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_reqires='>=3.6',
)
