# impactchartdemo

This repo introduces impact chart analysis and demonstrates how to generate impact charts.
Impact charts are a new way of visualizing the impact of one variable on another in a data
set. They are driven by interpretable Machine Learning (ML).

## Introductory Notebook with Synthetic Data

For an introduction showing what they do, and a comparison to traditional techniques,
please see the 
[Synthetic Data.ipynb](https://github.com/vengroff/impactchartdemo/blob/main/Synthetic%20Data.ipynb) 
notebook. This notebooks uses synthetic data to highlight what impact chart analysis can do.

## Run the Notebook Live in a Hosted Environment

Once you have read through the notebook, you might want to run it live, modify it,
and see the resutls. Thanks to [mybinder.org](mybinder.org), you can do this in 
a cloud-based hosted environment without any need to install anything.

Just click [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/vengroff/impactchartdemo/0.1.3?labpath=Synthetic+Data.ipynb) to
launch.

## More Background

You can read more
about impact charts in 
[Impact Charts: A Tool for Identifying Systematic Bias in Social Systems and Data ](https://datapinions.com/wp-content/uploads/2024/01/impactcharts.pdf).

## Running in a local virtual environment

To run the demo in your own virtual environment, try this:

```python
pip install impactchartdemo
```

```python
jupyter-lab &
```

This should fire up the jupyter lab server and open a browser tap to it. From there, you can open 
`Synthetic Data.ipynb`.

## An Example with Real Data

If you would like to see a demo on real data instead of synthetic data, check out
[Housing Value.ipynb](https://github.com/vengroff/impactchartdemo/blob/main/Housing%20Value.ipynb) 
