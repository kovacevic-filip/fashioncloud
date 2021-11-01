from catalog_mapping import _create_mapping_dict, merge_columns, map_data, create_catalog_data, _add_article_data, \
    _add_variation_data, merge_custom_columns


def test_create_mapping_dict_correct_output():
    mapping_values = [{
        "source": "EU|37|1",
        "destination": "Europe size 37 blue",
        "source_type": "size_group_code|size_code|color_code",
        "destination_type": "test_column"
    }]

    expected_output = {
        "size_group_code|size_code|color_code": {
            "name": "test_column",
            "EU|37|1": "Europe size 37 blue"
        }
    }

    assert _create_mapping_dict(mapping_values) == expected_output


def test_create_mapping_dict_wrong_output():
    mapping_values = [{
        "source": "EU|37|1",
        "destination": "Europe size 37 blue",
        "source_type": "size_group_code|size_code|color_code",
        "destination_type": "test_column"
    }]

    not_expected_output = {
        "size_group_code|size_code|color_code": {
            "name": "test_column",
            "EU|37|1": "Europe size 37 red"
        }
    }

    assert _create_mapping_dict(mapping_values) != not_expected_output


def test_merge_columns_correct_output():
    price_values = [{
        "ean": "8719245200978",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]
    mapping_values = {
        "supplier|brand": {},
        "collection|season": {}
    }

    expected_output = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco BV|Via Vai",
        "collection|season": "NW 17-18|winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]

    assert merge_columns(price_values, mapping_values) == expected_output


def test_merge_columns_wrong_output():
    price_values = [{
        "ean": "8719245200978",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]
    mapping_values = {
        "supplier|brand": {},
        "collection|season": {}
    }

    expected_output = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco BV Via Vai",
        "collection|season": "NW 17-18 winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]

    assert merge_columns(price_values, mapping_values) != expected_output


def test_map_data_correct_output():
    grouped_data = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco BV|Via Vai",
        "collection|season": "NW 17-18|winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]
    mapping_values = {
        "supplier|brand": {
            "name": "supplier|brand",
            "Rupesco BV|Via Vai": "Rupesco test supplier brand"
        },
        "collection|season": {
            "name": "Test column name",
            "NW 17-18|winter": "Winter is coming"
        }
    }

    expected_output = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco test supplier brand",
        "Test column name": "Winter is coming",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]

    assert map_data(grouped_data, mapping_values) == expected_output


def test_map_data_wrong_output():
    grouped_data = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco BV|Via Vai",
        "collection|season": "NW 17-18|winter",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]
    mapping_values = {
        "supplier|brand": {
            "name": "supplier brand",
            "Rupesco BV|Via Vai": "Rupesco test supplier brand"
        },
        "collection|season": {
            "name": "Test column name",
            "NW 17-18|winter": "Winter is coming"
        }
    }

    expected_output_wrong_column_name = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco test supplier brand",
        "Test column name": "Winter is coming",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]

    expected_output_wrong_column_value = [{
        "ean": "8719245200978",
        "supplier|brand": "Rupesco test supplier brand",
        "Test column name": "Winter is not coming",
        "article_structure_code": "10",
        "article_number": "15189-02"
    }]

    assert map_data(grouped_data, mapping_values) != expected_output_wrong_column_name
    assert map_data(grouped_data, mapping_values) != expected_output_wrong_column_value


def test_create_catalog_data_correct_output():
    mapped_data = [{
        "ean": "Test value",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "Winter Collection 2017/2018",
        "season": "Winter",
        "article_structure": "Pump",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color": "Nero",
        "size": "European size 38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Aviation",
        "target_area": "Test shoes"
    }]

    expected_output = {
        "brand": "Via Vai",
        "supplier": "Rupesco BV",
        "collection": "Winter Collection 2017/2018",
        "season": "Winter",
        "article": {
            "15189-02": {
                "article_structure": "Pump",
                "article_number_2": "15189-02 Aviation Nero",
                "article_number_3": "Aviation",
                "target_area": "Test shoes",
                "variation": {
                    "Test value": {
                        "color": "Nero",
                        "size": "European size 38",
                        "size_name": "38",
                        "currency": "EUR",
                        "price_buy_net": "58.5",
                        "price_sell": "139.95",
                        "material": "Aviation"
                    }
                }
            }
        }
    }

    assert create_catalog_data(mapped_data) == expected_output


def test_create_catalog_data_wrong_output():
    mapped_data = [{
        "ean": "Test value",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "Winter Collection 2017/2018",
        "season": "Winter",
        "article_structure": "Pump",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color": "Nero",
        "size": "European size 38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Wood",
        "target_area": "Test Shoes"
    }]

    expected_output = {
        "brand": "Via Vai",
        "supplier": "Rupesco BV",
        "collection": "Winter Collection 2017/2018",
        "season": "Winter",
        "article": {
            "15189-02": {
                "article_structure": "Pump",
                "article_number_2": "15189-02 Aviation Nero",
                "article_number_3": "Aviation",
                "target_area": "Woman Shoes",
                "variation": {
                    "Test value": {
                        "color": "Nero",
                        "size": "European size 38",
                        "size_name": "38",
                        "currency": "EUR",
                        "price_buy_net": "58.5",
                        "price_sell": "139.95",
                        "material": "Aviation"
                    }
                }
            }
        }
    }

    assert create_catalog_data(mapped_data) != expected_output
    
    
def test_merge_custom_columns_correct_output():
    columns_to_merge_name = ["supplier", "brand", "collection"]
    merged_column_name = "supplier_brand_collection"
    values_data = [{
        "ean": "8719245200978",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color_code": "1",
        "size_group_code": "EU",
        "size_code": "38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Aviation",
        "target_area": "Woman Shoes"
    }]

    expected_output = [{
        "ean": "8719245200978",
        "supplier_brand_collection": "Rupesco BV Via Vai NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color_code": "1",
        "size_group_code": "EU",
        "size_code": "38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Aviation",
        "target_area": "Woman Shoes"
    }]

    assert merge_custom_columns(columns_to_merge_name, merged_column_name, values_data) == expected_output


def test_merge_custom_columns_wrong_output():
    columns_to_merge_name = ["supplier", "brand", "collection"]
    merged_column_name = "supplier|brand|collection"
    values_data = [{
        "ean": "8719245200978",
        "supplier": "Rupesco BV",
        "brand": "Via Vai",
        "collection": "NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color_code": "1",
        "size_group_code": "EU",
        "size_code": "38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Aviation",
        "target_area": "Woman Shoes"
    }]

    expected_output = [{
        "ean": "8719245200978",
        "supplier_brand_collection": "Rupesco BV Via Vai NW 17-18",
        "season": "winter",
        "article_structure_code": "10",
        "article_number": "15189-02",
        "article_number_2": "15189-02 Aviation Nero",
        "article_number_3": "Aviation",
        "color_code": "1",
        "size_group_code": "EU",
        "size_code": "38",
        "size_name": "38",
        "currency": "EUR",
        "price_buy_net": "58.5",
        "price_sell": "139.95",
        "material": "Aviation",
        "target_area": "Woman Shoes"
    }]

    assert merge_custom_columns(columns_to_merge_name, merged_column_name, values_data) != expected_output


if __name__ == "__main__":
    test_create_mapping_dict_correct_output()
    test_create_mapping_dict_wrong_output()
    test_merge_columns_correct_output()
    test_merge_columns_wrong_output()
    test_map_data_correct_output()
    test_map_data_wrong_output()
    test_create_catalog_data_correct_output()
    test_create_catalog_data_wrong_output()
    test_merge_custom_columns_correct_output()
    test_merge_custom_columns_wrong_output()
