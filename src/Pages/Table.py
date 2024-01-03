import html
import pandas as pd


# from app import POSTGRES_DB_URI
from src.config import TABLE_COLS
from src.Database.db import db
from src.Database.Product import Product

class Table:

    @staticmethod
    def get_template_vars(website, category) -> dict:

        # df = pd.read_sql(Product.get_most_recent(website, category), db)
        df = pd.read_sql_query(Product.get_most_recent(website, category), db.engine)
        # df = pd.read

        # raw_query_results: list = Product.get_most_recent(website, category)

        # df: pd.DataFrame = pd.DataFrame(raw_query_results)



        df['Title'] = df.apply(Table.fix_title_col, axis=1)
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
