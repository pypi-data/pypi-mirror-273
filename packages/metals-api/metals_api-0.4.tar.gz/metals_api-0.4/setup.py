from setuptools import setup, find_packages

with open("README.md","r") as f:
    description = f.read()

setup(
    name='metals_api',
    version='0.4',
    description = 'A Python package to get the latest metals prices from the Metals-API',
    author = 'Metals-API',
    author_email = 'support@metals-api.com',
    url = 'https://github.com/Zyla-Labs/pypi-metals-api',
    keywords = ['metals-api', 'precious metals api',  'metals api', 'metals, precious metals' , 'gold' , 'silver', 'Platinum', 'Palladium', 'Ruthenium', 'Rhodium', 'forex data', 'rates', 'money', 'usd', 'eur', 'btc', 'forex api', 'gbp to usd', 'gbp to eur', 'eur to usd', 'api', 'currency api', 'exchange rate api', 'get currency rates api', 'currency rates php', 'usd to eur api','copper','nickel','aluminium','TIN', 'Zinc'],
    packages=find_packages(),
    install_requires=[
        
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)