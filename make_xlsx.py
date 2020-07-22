import pandas as pd
from pandas import DataFrame as df
from collections import Counter


def make_file(name, row_list):
    """
        xlsx 파일을 만들어주는 함수

            Parameters:
                name : str, 
                    xlsx파일 일므 
                row_list : list
                    필요한 데이터들이 담긴 list

            Returns:
                name.xlsx 
    """

    data = {
        "Test Suites": [],
        "Test Cases": [],
        "Result": [],
        "Number of Tests": []
    }

    for test_suits in row_list:

        length = len(test_suits["testcase"][0]["name"])
        data["Test Suites"].append(test_suits["name"])
        data["Number of Tests"].append(length)
        for _ in range(length-1):
            data["Test Suites"].append(" ")
            data["Number of Tests"].append(" ")

        for test in test_suits["testcase"]:
            data["Test Cases"] += test["name"]
            data["Result"] += test["result"]

    suites = len(list(filter(lambda x: x != " ", data["Test Suites"])))
    case = len(data["Test Cases"])
    success = Counter(data["Result"])

    data["Test Suites"].append(suites)
    data["Test Cases"].append(case)
    data["Result"].append(f"Success : {success['✓']}, Fail : {success['✕']}")
    data["Number of Tests"].append(f"Total : {case}")

    df2 = df(data=data)
    # print_df(df2)
    with pd.ExcelWriter(f"{name}.xlsx", mode="w", engine="openpyxl") as writer:
        df2.to_excel(writer, index=False, encoding="utf-8")
