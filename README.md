# get_ittf_info

Python package that helps scrape Table Tennis athletes and tournaments information from 'Table Tennis Guide' website and 'ITTF' official website

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ get-ittf-info==0.2.4
```

## Usage

- Web data scraping: Extract Table Tennis athletes and tournaments information from  '[Table Tennis Guide](https://tabletennis.guide/rating_ittf.php?gender=1)' website and '[ITTF](https://results.ittf.link/index.php)' official website. Includes:
  - Latest ranking for both male and female table tennis athletes.
  - Profile for registered atheletes in ITTF system.
  - All previous players participation information in World Table Tennis Championships.
- Data visualization: Do some basic analysis of our obtained dataset.
  - Bar chart visualization for the frequency of the selected column of the input dataframe
  - Pie chart  visualization for the percentages of different elements in the selected column of the input dataframe

## License

`get_ittf_info` was created by Mengdi Zhang. It is licensed under the terms of the MIT license.

## Credits

`get_ittf_info` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
