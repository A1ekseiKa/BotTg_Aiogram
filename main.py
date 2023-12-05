from openpyxl import load_workbook


def load_xlsx(path_file):
    wb2 = load_workbook(path_file)
    ws = wb2['Лист1']
    codes_list = []
    for i in ws.values:
        codes_list.append(i)
    return codes_list


def get_address(address_list, code_id):
    if int(code_id) <= len(address_list):
        for i in address_list:
            if i[5] == int(code_id):
                # print(i[2])
                return i[0], \
                    i[1].replace(' ', '_').replace('/', '_'), \
                    i[2].replace(' ', '_').replace('/', '_'), \
                    i[3], \
                    i[4].replace(' ', '_').replace('/', '_'), \
                    i[5]
    else:
        return None
