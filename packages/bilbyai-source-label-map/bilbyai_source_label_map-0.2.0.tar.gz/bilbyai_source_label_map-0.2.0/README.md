# source_label_map

Converts source code into human-friendly labels

# Quickstart

```python
from bilbyai.source_label_map import get_source_labels

# Get source labels for a list of inputs.
label = get_source_labels("ben") # outputs ['Beijing Evening News']

```

Get source labels for a list of inputs.

Args:
    `inputs` (`str | Iterable[str]`): The string or list of strings to get source labels for.
    
    `when_not_found`: The action to take when a source label is not found. Set to "preserve_source_name" by default.
      - `"preserve_source_name"`: Preserve the source name as the source label. 
      - `"set_to_none"`: Set the source label to None. 
      - `"set_to_unknown"`: Set the source label to "unknown". 
      - `"throw_error"`: Raise an error if a source label is not found. 
    
    source_label_dict: A dictionary mapping source names to source labels.

Returns:
    A list of source labels for the inputs.

Raises:
    ValueError: If the when_not_found value is not recognized.
    ValueError: If the inputs are not a string or iterable of strings.
    ValueError: If when_not_found is set to "throw_error" and a source label is not found.

The project owner is [@leetdavid](https://github.com/leetdavid).

## Development

If not already in a virtual environement, create and use one.
Read about it in the Python documentation: [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html).

```
python3 -m venv .venv
source .venv/bin/activate
```

Install the pinned pip version:

```
pip install -r $(git rev-parse --show-toplevel)/pip-requirements.txt
```

Finally, install the dependencies:

```
pip install -r $(git rev-parse --show-toplevel)/dev-requirements.txt -r requirements.txt
```

## Testing

Execute tests from the library's folder (after having loaded the virtual environment,
see above) as follows:

```
python3 -m pytest tests/
```

Execute the library's CI locally with [act](https://github.com/nektos/act) as follows:

```
act -j ci-libs-source_label_map
```
