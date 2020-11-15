from read_xml import clean
from make_xlsx import make_file

if __name__ == "__main__":

    row_list = clean()
    make_file("TRE", row_list)
