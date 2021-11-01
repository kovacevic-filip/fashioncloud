import csv
import copy
import json
from typing import List, Dict, Tuple


def load_data() -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    with open("/home/filip/projects/fashioncloud/pricat.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        price_values = []
        for row in reader:
            price_values.append(row)

    with open("/home/filip/projects/fashioncloud/mappings.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        mapping_values = []
        for row in reader:
            mapping_values.append(row)

    return price_values, mapping_values


def _create_mapping_dict(mapping_values: List[Dict[str, str]]) -> Dict[str, dict]:
    mapping_data = {}
    for row in mapping_values:
        if row['source_type'] not in mapping_data.keys():
            mapping_data[row['source_type']] = {}
        mapping_data[row['source_type']]['name'] = row['destination_type']
        mapping_data[row['source_type']][row['source']] = row['destination']

    return mapping_data


def merge_columns(price_values: List[Dict[str, str]]) -> List[Dict[str, str]]:
    price_values = copy.deepcopy(price_values)
    for row in price_values:
        row['size_group_code|size_code'] = f"{row['size_group_code']}|{row['size_code']}"
        del row['size_group_code']
        del row['size_code']

    return price_values


def map_data(grouped_data: List[Dict[str, str]], mapping_values: Dict[str, dict]) -> List[Dict[str, str]]:
    mapped_data = []
    for row in grouped_data:
        mapped_row = {}
        for key, value in row.items():
            if not value:
                continue
            if key in mapping_values.keys():
                column_name = mapping_values[key]['name']
                column_value = mapping_values[key][value]
                mapped_row[column_name] = column_value
            else:
                mapped_row[key] = value
        mapped_data.append(mapped_row)

    return mapped_data


def create_catalog_data(mapped_data: List[Dict[str, str]]) -> dict:
    catalog_data = {
        "brand": "",
        "supplier": "",
        "collection": "",
        "season": "",
        "article": {},
    }

    for row in mapped_data:
        catalog_data['brand'] = row['brand']
        catalog_data['supplier'] = row['supplier']
        catalog_data['collection'] = row['collection']
        catalog_data['season'] = row['season']
        if not row['article_number'] in catalog_data['article'].keys():
            catalog_data = _add_article_data(catalog_data, row)
        if row['ean'] in catalog_data['article'][row['article_number']]['variation'].keys():
            continue
        else:
            catalog_data = _add_variation_data(catalog_data, row)

    return catalog_data


def _add_article_data(catalog_data: dict, row: Dict[str, str]) -> dict:
    catalog_data = copy.deepcopy(catalog_data)
    catalog_data['article'][row['article_number']] = {}
    catalog_data['article'][row['article_number']]['article_structure'] = row['article_structure']
    catalog_data['article'][row['article_number']]['article_number_2'] = row['article_number_2']
    catalog_data['article'][row['article_number']]['article_number_3'] = row['article_number_3']
    catalog_data['article'][row['article_number']]['target_area'] = row['target_area']
    catalog_data['article'][row['article_number']]['variation'] = {}

    return catalog_data


def _add_variation_data(catalog_data: dict, row: Dict[str, str]) -> dict:
    catalog_data = copy.deepcopy(catalog_data)
    catalog_data['article'][row['article_number']]['variation'][row['ean']] = {}
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['color'] = row['color']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['size'] = row['size']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['size_name'] = row['size_name']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['currency'] = row['currency']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['price_buy_net'] = row['price_buy_net']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['price_sell'] = row['price_sell']
    catalog_data['article'][row['article_number']]['variation'][row['ean']]['material'] = row['material']

    return catalog_data


def additional_option(columns_to_merge_name: List[str], merged_column_name: str, price_values: List[Dict[str, str]])\
        -> List[Dict[str, str]]:
    price_values = copy.deepcopy(price_values)
    for row in price_values:
        merged_column_values = [f"{row[column_name]}" for column_name in columns_to_merge_name]
        row[merged_column_name] = ' '.join(merged_column_values)
        for merge_column_name in columns_to_merge_name:
            del row[merge_column_name]

    return price_values


def main():
    price_values, mapping_values = load_data()
    mapping_values = _create_mapping_dict(mapping_values)
    grouped_data = merge_columns(price_values)
    mapped_data = map_data(grouped_data, mapping_values)
    catalog_data = create_catalog_data(mapped_data)

    with open("/home/filip/projects/fashioncloud/json_values.json", "w") as json_file:
        json.dump(catalog_data, json_file)


if __name__ == "__main__":
    main()
