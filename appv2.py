import jenkins
import json
import os
import pandas as pd

from configs import JenkinsConfig
from pandas import DataFrame as df


CONFIG = JenkinsConfig()


def new_jenkins():
    return jenkins.Jenkins(
        CONFIG.url,
        CONFIG.user,
        CONFIG.password
    )


if __name__ == "__main__":
    current_job = os.getenv('JOB_NAME', default='IRIS-E2E')
    jenkins = new_jenkins()
    build_info = jenkins.get_job_info(current_job)
    last_build_number = build_info['lastBuild']['number']

    result = jenkins.get_build_test_report('IRIS-E2E', last_build_number)
    # with open("jenkins.json", "w", encoding="utf-8") as data:
    #     json.dump(result, data)
    # parsing

    data = {
        "Test Suites": [],
        "Test Cases": [],
        "Result": [],
        "Number of Tests": []
    }
    count_of_testsuites = len(result["suites"])
    cases = 0
    success = 0
    fail = 0
    for suite in result["suites"]:
        # 해당 테스트 스윗의 테스트 갯수
        count_of_testcase = len(suite["cases"])
        # 테스트 케이스 갯수
        cases += count_of_testcase

        # suits name
        suite_name = suite["name"]
        data["Test Suites"].append(suite_name)
        data["Number of Tests"].append(count_of_testcase)

        # test case
        for case in suite["cases"]:
            case_name = " ".join(case["name"].split(" ")[1:])
            data["Test Cases"].append(case_name)

            if case["status"] == "PASSED" or case["status"] == "FIXED":
                data["Result"].append('✓')
                success += 1
            else:
                data["Result"].append('X')
                fail += 1

        # 공백 채우기
        for _ in range(count_of_testcase - 1):
            data["Test Suites"].append(" ")
            data["Number of Tests"].append(" ")

    data["Test Suites"].append(f"All Test Suites: {count_of_testsuites}")
    data["Test Cases"].append(f"All Tests: {cases}")
    data["Result"].append(f"success: {success}")
    data["Number of Tests"].append(f"fail: {fail}")

    # print(num_of_test, num_of_suites, num_of_case, data)
    df2 = df(data=data)
    # print_df(df2)
    with pd.ExcelWriter("TRE.xlsx", mode="w", engine="openpyxl") as writer:
        df2.to_excel(writer, index=False, encoding="utf-8")
