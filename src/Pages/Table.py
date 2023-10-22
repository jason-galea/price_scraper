import html
import pandas as pd


from src.config import TABLE_COLS

class Table:
    
    @staticmethod
    def get_template_vars(website, category) -> dict:

        # ### Filter to files containing the chosen website & category
        # filtered_files = [ item
        #     for item in get_json_filenames()
        #     if (listContainsAllValues(item.split('.')[0].split("_"), [website, category]))
        # ]
        # # print(f"filtered_files = {filtered_files}")
        # latest_file = max(filtered_files, key=os.path.getctime)
        # latest_file_basename = os.path.basename(latest_file)

        ### DEBUG
        # print(f"latest_file = {latest_file}")
        # print(f"latest_file_basename = {latest_file_basename}")

        # ### Read JSON --> DataFrame
        # df: pd.DataFrame = pd.read_json(latest_file)


        ### TODO: Query DB for latest entry for website & category
        utctime_for_latest_matching_data = "asd"
        
        ### TODO: Query DB for data matching above UTCtime
        df = pd.read_sql_query()


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
