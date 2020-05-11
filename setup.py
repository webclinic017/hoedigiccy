# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="hoedigiccy",
    version="1.0.0",
    packages=[
        "hoedigiccy",
        "hoedigiccy.utils",
        "hoedigiccy.platform",
    ],
    description="Asynchronous event I/O driven quantitative trading framework.",
    url="https://github.com/redhoe/hoedigiccy",
    author="RedHoe",
    author_email="lamusxiao@qq.com",
    license="MIT",
    keywords=[
        "hoedigiccy", "quant", "framework", "async", "asynchronous", "digiccy", "digital", "currency", "marketmaker",
        "binance", "okex", "huobi", "bitmex", "deribit", "kraken", "gemini", "kucoin"
    ],
    install_requires=[
        "aiohttp==3.6.2",
        "aioamqp==0.14.0",
        "motor==2.0.0"
    ],
)
