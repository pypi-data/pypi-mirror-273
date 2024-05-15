from setuptools import setup, find_packages

readme = open("./README.md", "r", encoding="utf-8")

setup(
    name="trujillo-sunat-package",
    version="0.0.1",
    packages=find_packages(),
    license="MIT",
    long_description=readme.read(),
    long_description_content_type="text/markdown; charset=UTF-8",
    description="Este paquete está diseñado específicamente para proporcionar clases que permiten a los usuarios establecer una conexión eficiente con las API SUNAT",
    author="Fernando Colque",
    install_requires=['pandas','requests'],
    author_email="fernando.colque@terranovatrading.com.pe",
)