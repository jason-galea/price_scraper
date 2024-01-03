import html
import pandas as pd
# import json

from src.config import TABLE_COLS
from src.Database import CATEGORY_CLASS_DICT


class Table:
    """
    Container class for methods related to the "Table" page
    """

    @staticmethod
    def get_template_vars(website, category) -> dict:

        # products: list = Product.get_most_recent(website, category)
        products: list = CATEGORY_CLASS_DICT[category].get_most_recent(website)
        # products: list = CATEGORY_CLASS_DICT[category].get_most_recent(website, category)

        # print(f"==> DEBUG: products = {products}")
        print(f"==> DEBUG: products[0] = {products[0]}")
        # print(f"==> DEBUG: products[0].__dict__ = {products[0].__dict__}")

        # for p in products:
        #     print(f"==> DEBUG: product = {json.dumps(p, indent=4)}")

        df: pd.DataFrame = pd.DataFrame(products)
        df = df.set_index('UTCTime')
        print(f"==> DEBUG: df = {df}")


        df['Title'] = df.apply(Table.fix_title_col, axis=1)
        # df['Title'] = df["Title"].apply(Table.fix_title_col, axis=1)
        df['TitleLink'] = df.apply(
            lambda row: f"<a href={row['URL']}>{row['Title']}</a>",
            axis=1,
        )

        ### Restrict & sort cols
        df = df[TABLE_COLS[category]['display_cols']]
        df = df.sort_values(TABLE_COLS[category]['sort_col'], ignore_index=True)

        ### Escape all cols except "TitleLink"
        df[[
            c
            for c in list(df.columns)
            if (c != 'TitleLink')
        ]].apply( html.escape, axis=1 )

        return {
            # 'latest_file': latest_file,
            # 'latest_file_basename': latest_file_basename, ### Signposting
            'table_html': df.to_html(escape=False)
        }


    @staticmethod
    def fix_title_col(row) -> str:
        match_replace_dict = {
            'Hard Drive': 'HDD',
            '3.5in ': '',
            'WD ': '',
        }
        result = str(row["Title"])

        for match, replace in match_replace_dict.items():
            result = result.replace(match, replace)

        return result
