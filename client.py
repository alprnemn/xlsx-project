from datetime import datetime
from openpyxl.workbook.workbook import Workbook
from utils import parse_args, upload_csv_and_get_df_from_server, add_headers_to_excel_sheet, create_excel_sheet_with_df

def main():

    # get parameters from comand line if args are valid
    args = parse_args()

    # get clean dataframe from server
    df = upload_csv_and_get_df_from_server("vehicles.csv")

    # create worksheet
    wb = Workbook()
    ws = wb.active

    #add headers to sheet
    ws, headers = add_headers_to_excel_sheet(ws, args.keys)

    # writes df rows into excel sheet and fill bg by hu value if colored is true
    ws = create_excel_sheet_with_df(df, ws, args)

    #save excel sheet '.xlsx' format
    wb.save(f"vehicles_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")


if __name__ == "__main__":
    main()