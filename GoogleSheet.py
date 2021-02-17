import jenkins
import time
import os
import json

from configs import GoogleSheetConfig
from configs import JenkinsConfig


class JenkinsAPI():
    """[summary]
    jenkins 데이터를 추출하기 위한 클래스
    """

    def __init__(self):
        """[summary]
        IRIS-E2E의 가장 마지막 빌드의 테스트 결과를 추출
        """
        current_job = os.getenv('JOB_NAME', default='IRIS-E2E')

        jenkins = self.new_jenkins()
        build_info = jenkins.get_job_info(current_job)
        last_build_number = build_info['lastBuild']['number']
        self.result = jenkins.get_build_test_report(
            'IRIS-E2E', last_build_number)

    def new_jenkins(self):
        CONFIG = JenkinsConfig()
        return jenkins.Jenkins(
            CONFIG.url,
            CONFIG.user,
            CONFIG.password
        )

    def check_pass_or_fail(self, input_test_case_name):
        for test_suit in self.result["suites"]:
            for test_case in test_suit["cases"]:
                api_test_case_name = test_case["name"].encode(
                    'utf-8').decode('utf-8')
                if input_test_case_name in api_test_case_name:
                    return test_case["status"]


class GoogleSheet():
    def __init__(self, tab_name):
        self.worksheet = GoogleSheetConfig().doc.worksheet(tab_name)
        self.length_of_sheet = len(
            self.worksheet.get()) - 13  # 작성된 test-map의 갯수 13이 위에 통계
        self.update_cell_position = 22  # 테스트 결과가 담길 셀의 위치
        self.test_case_position = 'N'  # 테스트 케이스 이름의 위치
        self.test_case_state_position = 'C'  # 자동 / 구현 예정의 위치
        self.pass_format = {
            "backgroundColor": {
                "red": 180,
                "green": 60,
                "blue": 27
            },
        }
        self.error_format = {
            "backgroundColor": {
                "red": 27,
                "green": 180,
                "blue": 124
            },
        }

    def get_cell_data(self, cell_label):
        return self.worksheet.acell(cell_label).value

    def get_row_data(self, row_number):
        return self.worksheet.row_values(row_number)

    def update_cell(self, row_number, data):
        self.worksheet.update_cell(row_number, self.update_cell_position, "")
        if data == "PASSED" or data == "FIXED":
            self.worksheet.format(f"V{row_number}", self.pass_format)

        elif data == "FAILED" or data == "REGRESSION":
            self.worksheet.format(f"V{row_number}", self.error_format)

        self.worksheet.update_cell(
            row_number, self.update_cell_position, data)


if __name__ == '__main__':
    jenkins = JenkinsAPI()
    google = GoogleSheet('minsoo-test')

    for index in range(google.length_of_sheet):
        print(f"{index} 번째 작업...")
        time.sleep(2)
        test_case = google.get_cell_data(
            f"{google.test_case_position}{index+14}")
        result = jenkins.check_pass_or_fail(test_case)
        google.update_cell(row_number=index+14, data=result)
