
# xlsx-to-html-extractor

`xlsx-to-html-extractor` is a Python utility that converts Excel sheets to HTML files. It provides options to include formulas, grid labels, and cell titles.

## Features

- Convert Excel sheets to HTML files.
- Option to include formulas in the HTML output.
- Option to add grid labels (row and column numbers).
- Option to add cell titles showing the cell addresses.

## Installation

You can install the package using pip:

```bash
pip install xlsx-to-html-extractor`` 
```

## Usage

### Basic Usage

Here's a basic example of how to use the `XlsxExtractor` class:

```python
from xlsx_to_html_extractor import XlsxExtractor

# Initialize the extractor
extractor = XlsxExtractor(
    source_xlsx='data.xlsx',
    dest_html_file='result.html',
    show_formulas=False,
    grid_labels=True,
    cell_titles=True
)

# Extract the data and save to HTML
extractor.extract()` 
```

### Parameters

-   `source_xlsx`: Path to the source Excel file.
-   `dest_html_file`: Path to the destination HTML file.
-   `show_formulas`: Boolean flag to include formulas in the HTML output.
-   `grid_labels`: Boolean flag to add grid labels (row and column numbers).
-   `cell_titles`: Boolean flag to add cell titles showing the cell addresses.

## Examples

### Including Formulas

To include formulas in the HTML output, set `show_formulas` to `True`:

```python
from xlsx_to_html_extractor import XlsxExtractor

extractor = XlsxExtractor(
    source_xlsx='data.xlsx',
    dest_html_file='result.html',
    show_formulas=True,
    grid_labels=True,
    cell_titles=True
)

extractor.extract()
```

### Adding Grid Labels

To add grid labels (row and column numbers), set `grid_labels` to `True`:

```python
from xlsx_to_html_extractor import XlsxExtractor

extractor = XlsxExtractor(
    source_xlsx='data.xlsx',
    dest_html_file='result.html',
    show_formulas=False,
    grid_labels=True,
    cell_titles=False
)

extractor.extract()
```

### Adding Cell Titles

To add cell titles showing the cell addresses, set `cell_titles` to `True`:

```python
from xlsx_to_html_extractor import XlsxExtractor

extractor = XlsxExtractor(
    source_xlsx="data.xlsx",
    dest_html_file="result.html",
    show_formulas=False,
    grid_labels=False,
    cell_titles=True
)
extractor.extract()
```

## License

This project is licensed under the MIT License.