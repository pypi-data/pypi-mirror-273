# simulaix

An efficient synthetic data framework



## Documentation

todo

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
Python 3.6 or higher.