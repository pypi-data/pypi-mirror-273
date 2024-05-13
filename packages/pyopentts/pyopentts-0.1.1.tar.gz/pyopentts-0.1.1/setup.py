from setuptools import setup, find_packages

setup(
    name="pyopentts",
    version="0.1.1",
    description="Python client for OpenTTS API",
    author="Jorge",
    author_email="jsequeira03@gmail.com",
    packages=find_packages(),
    install_requires=["requests>=2.25.1"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="text-to-speech, TTS, API, client",
)
