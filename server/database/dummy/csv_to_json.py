import sys
import os
import pandas as pd

# def csv_to_json(csvFilePath, jsonFilePath):
#     jsonArray = []

#     # read csv file
#     with open(csvFilePath, encoding="utf-8") as csvf:
#         # load csv file data using csv library's dictionary reader
#         csvReader = csv.DictReader(csvf)

#         # convert each csv row into python dict
#         for row in csvReader:
#             # add this python dict to json array
#             jsonArray.append(row)

#     # convert python jsonArray to JSON String and write to file
#     with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
#         jsonString = json.dumps(jsonArray, indent=4)
#         jsonf.write(jsonString)


if __name__ == "__main__":
    try:
        for file in os.listdir("./dummy_data"):
            print(f"{file}")
            # csv_to_json(
            #     f"./dummy_data/{file}", f"./dummy_data/{os.path.splitext(file)[0]}.json"
            # )
            df = pd.read_csv(file)
            df.to_json(f"{file}.json")
            break
    except ValueError as e:
        sys.exit(e)
