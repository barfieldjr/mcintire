# Free McIntire

I was never a comm student, but this is what I imagine they do.

## About

This repo contains a collection of scripts that pull Company SEC filing data. This data comes directly from the [sec.gov](www.sec.gov) website.

# Getting Started

1. Clone this repo

```bash
git clone https://github.com/barfieldjr/mcintire.git
cd mcintire
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

# Usage

## Get Company 10-Q Section 1, Part 2

This script will download and print the second part of the first section of a company's most recent 10-Q filing.

```bash
python sec-10q-s1p2.py [ticker]
```

# Disclaimer

However, this repo does not include any grade inflation or the necessary tools to sell your soul to a consulting company.
