# save-return

Save the return value of the decorated function to a versioned pickle file.

## Save

```python
import save_return

@save_return.save('value_of_pi')
def calc_pi():
    return 4

pi = calc_pi()
```

This will `pickle.save` `pi` to `./data/save_return/value_of_pi/yyyymmdd_HHMMSS_MS_00000.pkl`

If used inside a Jupyter notebook named `x.ipynb`, 
it will instead save to `./x.ipynb.save_return/value_of_pi/yyyymmdd_HHMMSS_MS_00000.pkl`

Use `@save_return.save(..., save_dir="some-dir")` to customize the save location.

```python
pi = calc_pi()
```

Call it again will save `pi` to `./data/save_return/value_of_pi/yyyymmdd_HHMMSS_MS_00001.pkl`

## Load

The `load` function is just a wrapper around `pickle`:

```python
pi = save_return.load('./data/save_return/value_of_pi/yyyymmdd_HHMMSS_MS_00000.pkl')
```