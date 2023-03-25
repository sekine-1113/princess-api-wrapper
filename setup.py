import setuptools


setuptools.setup(
    name="princess",
    version="1.2.2",
    description="アイドルマスターミリオンライブ!シアターデイズのAPI(PrincessAPI)のPythonラッパー",
    author="Sekine Toshiaki",
    packages=setuptools.find_packages(),
    install_requires=["cachetools", "requests"]
)