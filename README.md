Solution to the task is written in functions. It can be run by writing `python catalog_mapping`. I have used functions for fast implementation, although there are other possible solutions like using objects. Where methods on each object would enable the specific object to check whether data it received are correct as well as to clean specific data (strip on string, check for some illogic data...).
The code is written for specific usecase that is given in examples. 

To load csv files, you will need to write path to `price.csv` and `mapping.csv` files in `load_data` function.
Write path for result `json` file in `main` function which is at the end of `catalog_mapping.py`.

I have solved both tasks in `Bonus points` section in `instructions.pdf`. Name of the function for merging custom columns is `merge_custom_columns`.
The function takes list of column names to be merged, name of the destination column as well as name of the file that contains all the data.
Order of values in destination column matches order of column names in list argument. 

example: `merge_custom_columns([price_buy_net, currency, material], price_buy_net_currency_material, values_csv)` will merge columns `price_buy_net`, `currency` and `material` into column named `price_buy_net_currency_material` and values will be `58.5 EUR Aviation` for the first article.
Values are separated by empty space, although if necessary I can easily adapt the function to accept different separators as argument.
The function will merge columns and their values, but it will fail in creating final file if the name of the column is different than the ones in example.

I have created unit tests for almost every function. Only functions that are not tested are `load_data` (since I have used try-except I thought there is no need to test it) and functions `_add_article_data` and `_add_variant_data` (they are called in `create_catalog_data` function that is tested so that ensures they will work)
Tests are located in the `test.py` file.
