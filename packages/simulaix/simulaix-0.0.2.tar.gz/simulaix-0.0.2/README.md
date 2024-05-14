# Simulaix

An efficient synthetic data framework


---
Introduction to Simulaix:
- [About Simulaix](#about-simulaix)
    - [Why Simulaix?](#why-simulaix)
    - [Features](#features)
    - [Roadmap](#roadmap)
- [Installation](#installation)
    - [Usage](#usage)



## About Simulaix

Simulaix is a synthetic data generation framework that allows you to create synthetic data for machine learning and deep learning applications. It provides a simple and easy-to-use API to generate synthetic data for various applications. 


## Why Simulaix?


## Features
- [ ] add face generation
- [ ] add img generation



## Installation

```sh 
# install from PyPI
pip install simulaix

```


## Usage

```python
import simulaix as sim

# create a synthetic data generator
generator = sim.Generator(type='face', size=(200, 200))
generator.generate(num_samples=1000, output_dir='data/face')

```





## Requirements
Python 3.7 or higher.