from openpyxl import load_workbook

class state_edit:
    def __init__(self, _statename):
        self.statename = _statename
        self.arableland = 0
        self.arable_resource = list()
        self.capped_resource = dict()
        self.uncapped_resource = dict()
        self.uncapped_resource2 = dict() #Discovered Hidden resource

    def setArable(self, arable):
        self.arableland = arable

    def setArrRes(self, bg):
        self.arable_resource.append(bg)

    def setCapRes(self, bg, size):
        self.capped_resource[bg] = size

    def setUnCapRes(self, bg, size, dep = ""):
        self.uncapped_resource[bg] = [size, False, dep]

    def setUnCapRes2(self, bg, size, dep = ""):
        self.uncapped_resource2[bg] = [size, False, dep]

def EditInfoReader(path, edit_info):
    wb_reader = load_workbook(path, data_only=True)

    ws_arrable = wb_reader["Arable Lands"]
    for row in ws_arrable.rows:
        if row[0].value == "STATE_CODE":
            print("Arable Lands Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setArable(row[1].value)
        else:
            new_state = state_edit(row[0].value)
            new_state.setArable(row[1].value)
            edit_info[row[0].value] = new_state

    ws_arr_res = wb_reader["Arable Resources"]
    for row in ws_arr_res.rows:
        if row[0].value == "STATE_CODE":
            print("Arable Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setArrRes(row[1].value)
        else:
            new_state = state_edit(row[0].value)
            new_state.setArrRes(row[1].value)
            edit_info[row[0].value] = new_state

    ws_cap_res = wb_reader["Capped Resources"]
    for row in ws_cap_res.rows:
        if row[0].value == "STATE_CODE":
            print("Capped Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setCapRes(row[1].value, row[2].value)
        else:
            new_state = state_edit(row[0].value)
            new_state.setCapRes(row[1].value, row[2].value)
            edit_info[row[0].value] = new_state

    ws_uncap_res = wb_reader["Hidden Resources"]
    for row in ws_uncap_res.rows:
        if row[0].value == "STATE_CODE":
            print("Hidden Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setUnCapRes(row[1].value, row[2].value, row[3].value)
        else:
            new_state = state_edit(row[0].value)
            new_state.setUnCapRes(row[1].value, row[2].value, row[3].value)
            edit_info[row[0].value] = new_state

    ws_uncap_res2 = wb_reader["Hidden Resources (Discovered)"]
    for row in ws_uncap_res2.rows:
        if row[0].value == "STATE_CODE":
            print("Hidden and Discovered Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setUnCapRes2(row[1].value, row[2].value, row[3].value)
        else:
            new_state = state_edit(row[0].value)
            new_state.setUnCapRes2(row[1].value, row[2].value, row[3].value)
            edit_info[row[0].value] = new_state


def Editor(state_edit_info):
    # state_edit_info = state_edit("")
    state_name = state_edit_info.statename

    raw = open("raw_data/" + state_name + ".txt", mode = 'r', encoding = 'utf-8-sig')
    new = open("modded_data/" + state_name + ".txt", mode = 'w', encoding = 'utf-8-sig')
    arr_lands = state_edit_info.arableland
    arr_res = state_edit_info.arable_resource
    capres = state_edit_info.capped_resource
    unres = state_edit_info.uncapped_resource
    unres2 = state_edit_info.uncapped_resource2
    resource_editted_num = len(unres) + len(unres2)

    while(True):
        raw_line = raw.readline()

        if not raw_line:
            raw.close()
            new.close()
            break
        elif arr_lands != 0 and "arable_land" in raw_line:
            new_str = "    arable_land = " + str(arr_lands) + "\n"
            new.writelines(new_str)
        elif len(arr_res) != 0 and "arable_resources" in raw_line:
            raw_arr_res = raw_line.split(' ')
            raw_arr_res.pop()
            for arr_res_each in arr_res:
                arr_res_each = '"' + arr_res_each + '"'
                if arr_res_each in raw_arr_res:
                    raw_arr_res.remove(arr_res_each)
                else:
                    raw_arr_res.append(arr_res_each)

            new_str = ' '.join(raw_arr_res)
            new.writelines(new_str + " }\n")
        elif len(capres) != 0 and "capped_resources" in raw_line:
            new.writelines(raw_line)

            while(True):
                raw_line2 = raw.readline()
                raw_line2s = raw_line2.split(' ')
                while not '}' in raw_line2s and '' in raw_line2s:
                    raw_line2s.remove('')
                while not '}' in raw_line and '\t' in raw_line2s:
                    raw_line2s.remove('\t')

                raw_line2_s = raw_line2s[0]
                new_str = ""
                if raw_line2_s in capres:
                    if capres[raw_line2_s] != 0:
                        new_str = "        " + raw_line2_s + " = " + str(capres[raw_line2_s]) + "\n"
                else: new_str = raw_line2
                new.writelines(new_str)

                if "}" in raw_line2:
                    break
        elif resource_editted_num != 0 and "resource = {" in raw_line and not("capped" in raw_line) and not("arable" in raw_line):
            raw_line2 = raw.readline()
            raw_line2s = raw_line2.split(' ')
            while not '}' in raw_line2s and '' in raw_line2s:
                raw_line2s.remove('')
            while not '}' in raw_line and '\t' in raw_line2s:
                raw_line2s.remove('\t')

            raw_line2s[2] = raw_line2s[2].replace('\n', '')
            raw_line2_s = raw_line2s[2][1:-1]
            if raw_line2_s in unres:
                if unres[raw_line2_s][0] != 0:
                    new.writelines(raw_line)
                    new.writelines("        type = \"" + raw_line2_s + "\"\n")
                    if unres[raw_line2_s][2] is not None:
                        new.writelines("        depleted_type = \"" + unres[raw_line2_s][2] + "\"\n")
                    new.writelines("        undiscovered_amount = " + str(unres[raw_line2_s][0]) + "\n")
                    new.writelines("    }\n")
                while not "}" in raw_line2:
                    raw_line2 = raw.readline()
                resource_editted_num = resource_editted_num - 1
                unres[raw_line2_s][1] = True
            elif raw_line2_s in unres2:
                if unres2[raw_line2_s][0] != 0:
                    new.writelines(raw_line)
                    new.writelines("        type = \"" + raw_line2_s + "\"\n")
                    if unres2[raw_line2_s][2] is not None:
                        new.writelines("        depleted_type = \"" + unres2[raw_line2_s][2] + "\"\n")
                    new.writelines("        discovered_amount = " + str(unres2[raw_line2_s][0]) + "\n")
                    new.writelines("    }\n")
                while not "}" in raw_line2:
                    raw_line2 = raw.readline()
                resource_editted_num = resource_editted_num - 1
                unres2[raw_line2_s][1] = True
            else:
                new.writelines(raw_line2)
                while "}" in raw_line2:
                    raw_line2 = raw.readline()
                    new.writelines(raw_line2)
        elif "naval_exit_id" in raw_line and resource_editted_num != 0:
            for res in unres:
                if not unres[res][1]:
                    if not unres[res][0] == 0:
                        new.writelines("    resource = {\n")
                        new.writelines("        type = \"" + res + "\"\n")
                        if unres[res][2] is not None:
                            new.writelines("        depleted_type = \"" + unres[res][2] + "\"\n")
                        new.writelines("        undiscovered_amount = " + str(unres[res][0]) + "\n")
                        new.writelines("    }\n")
                    unres[res][1] = True
                    resource_editted_num = resource_editted_num - 1
                if resource_editted_num == 0:
                    break

            for res in unres2:
                if not unres2[res][1]:
                    if not unres2[res][0] == 0:
                        new.writelines("    resource = {\n")
                        new.writelines("        type = \"" + res + "\"\n")
                        if unres2[res][2] is not None:
                            new.writelines("        depleted_type = \"" + unres2[res][2] + "\"\n")
                        new.writelines("        discovered_amount = " + str(unres2[res][0]) + "\n")
                        new.writelines("    }\n")
                    unres2[res][1] = True
                    resource_editted_num = resource_editted_num - 1
                if resource_editted_num == 0:
                    break
            new.writelines(raw_line)
        else:
            new.writelines(raw_line)


# Main
input_path = "input.xlsx"
fail_path = "error.txt"
editinfo = dict()
EditInfoReader(input_path, editinfo)
print("데이터 읽기 완료")

for state in editinfo:
    Editor(editinfo[state])

