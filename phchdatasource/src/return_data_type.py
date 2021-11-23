
def adapter_list_of_dict(rows, columns) -> list:
    final_res = []
    for row in rows:
        cells = row.split("\t")
        print(cells)
        tmp = {}
        for index in range(len(cells)):
            tmp[columns[index]] = cells[index]

        final_res.append(tmp)
    return final_res


def adapter_list_of_list(rows, columns) -> list:
    final_res = []
    final_res.append(columns)
    for row in rows:
        final_res.append(row.split("\t"))
    return final_res

