## Bank of Ghana Exchange Rate Python Library

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Support this Project](#support-these-projects)

## Overview
Current Version: 0.1.6

The unofficial Python API client library for Bank of Ghana allows individuals to pull historical and real-time exchange rates data using the Python programming language. 
Learn more by visiting https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/

## Requirements
```bash
python_requires='>=3.5' or later

install_requires=[
        'requests',
        'urllib3',
        'bs4',
        'lxml'
    ]
```

## Installation

```python

pip install https://buc2017.s3.us-east-2.amazonaws.com/bank_of_ghana_fx_rates-0.1.6-py3-none-any.whl

```
```python
from bog import scraper
from bog.scraper import RatesURL

url = RatesURL()
url.setUrl('https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/')

print(url.getUrl())

scraper.run(url)

```

## Installation from repo

Here is a simple example of using the `bank-of-ghana-fx-rate` library to grab the exchange rate data.

First, clone this repo to your local system. After you clone the repo, make sure
to run the `setup.py` file, so you can install any dependencies you may need. To
run the `setup.py` file, run the following command in your terminal.

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

```bash
pip install -e .
```

## Clone Repo
```bash
git clone https://github.com/donwany/bank-of-ghana-fx-rates

cd bank-of-ghana-fx-rates

python scraper.py --url [PATH-TO-REMOTE-LINK]
```
If you not specify any url, the default url is used. See example below:

## Example
```bash
python scraper.py

python scraper.py https://www.bog.gov.gh/treasury-and-the-markets/treasury-bill-rates/

python scraper.py https://www.bog.gov.gh/treasury-and-the-markets/historical-interbank-fx-rates/
```

## Support this Project
**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Theophilus Siameh](https://www.youtube.com/channel/UCLR6pmwKhA0OsJBLeY0WF_A/videos?view_as=subscriber).
