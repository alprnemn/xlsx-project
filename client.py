import pandas as pd
import requests


def main():

    with open("vehicles.csv", "rb") as f:
        try:
            res = requests.post("http://localhost:8000/upload", files={"file": f})
            data = res.json()
        except Exception as e:
            RuntimeError(e)

if __name__ == "__main__":
    main()