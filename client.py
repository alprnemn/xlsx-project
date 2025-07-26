from utils import parse_args, upload_csv_and_get_df_from_server

def main():

    # get parameters from comand line if args are valid
    args = parse_args()

    # get clean dataframe from server
    df = upload_csv_and_get_df_from_server("vehicles.csv")

    print(df.info())

if __name__ == "__main__":
    main()