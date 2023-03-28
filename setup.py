import setuptools


setuptools.setup(
    name="princessAPI",
    version="2.0.0",
    description="アイドルマスターミリオンライブ!シアターデイズのAPI(PrincessAPI)のPythonラッパー",
    author="Share Nakatani",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["cachetools", "requests"],
)