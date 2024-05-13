from setuptools import setup, find_packages

setup(
    name="OpenTTSClient",
    version="0.1.0",
    description="Python client for OpenTTS API",
    author="Your Name",
    author_email="your.email@example.com",
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
