import json
import xmltodict
import glob

FILE_LIST = glob.glob('reports/*.xml')


def read_XML_files():
    """
        xml 을 읽어서 json이 담긴 리스트로 반환

            Parameters:
                None

            Returns:
                list: json 데이터가 담긴 리스트
    """
    r = []
    for file in FILE_LIST:
        with open(file=file, mode='r', encoding='utf-8') as f:
            xml_data = xmltodict.parse(f.read())
            xml_json = json.dumps(xml_data)
            xml_dict = json.loads(xml_json)
            r.append(xml_dict)
    else:
        return r


def clean():
    """
        json이 담긴 리스트를 가져와서 필요한 json 데이터들로 정리

            Parameters:
                None

            Returns:
                list: 필요한 json 데이터가 담긴 리스트
                    name : str , testcase : list 
                                                     name : str, result : str
    """
    val = []
    datas = read_XML_files()
    for data in datas:
        try:
            suite_name = data['testsuites']['testsuite']['@name']
            test = data['testsuites']['testsuite']['testcase']
        except KeyError:
            pass
        else:
            if isinstance(test, dict):
                a = []
                a.append(test)
                test = a
            val.append(
                {
                    'name': suite_name,
                    'testcase': [
                        {
                            "name": [x['@name'].lstrip(suite_name) for x in test],
                            "result": ["✓" if 'failure' not in r else "✕" for r in test],
                        }
                    ]
                }
            )

    return val
