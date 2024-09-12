import datetime
import pandas


def register(columns, objects_to_store, sheet_name):
    df = pandas.DataFrame.from_records([object_to_store_in_xls.to_dict() for object_to_store_in_xls in all_articles]
                                    , columns= columns)
    now = datetime.datetime.now()
    xlsx_filename = now.strftime('%Y-%m-%d__%H-%M-%S') + '__.xlsx'
    df.to_excel(xlsx_filename, sheet_name=sheet_name)