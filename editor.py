from openpyxl import load_workbook

class state_edit:
    def __init__(self, _statename):
        self.statename = _statename
        self.arableland = 0
        self.arable_resource = list()
        self.capped_resource = dict()
        self.hidden_resource = dict()

    def setArable(self, arable):
        self.arableland = arable

    def setArrRes(self, bg):
        self.arable_resource.append(bg)

    def setCapRes(self, bg, size):
        self.capped_resource[bg] = size

    def setHiddenRes(self, bg, size, dep = "", discvd = False):
        self.hidden_resource[bg] = [size, dep, discvd]

class state_info(state_edit):
    def __init__(self, _statename):
        super().__init__(_statename)
        self.longstr_raw_data = []
        self.naval_exit_id = -1

    def appendStr(self, str):
        self.longstr_raw_data.append(str)

    def setNavalExit(self, id):
        self.naval_exit_id = id

def EditInfoReader(path, edit_info):
    wb_reader = load_workbook(path, data_only=True)

    ws_arrable = wb_reader["Arable Lands"]
    for row in ws_arrable.rows:
        if row[0].value == "STATE_CODE":
            print("Arable Lands Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setArable(str(row[1].value))
        elif row[0].value is not None:
            new_state = state_edit(row[0].value)
            new_state.setArable(str(row[1].value))
            edit_info[row[0].value] = new_state

    ws_arr_res = wb_reader["Arable Resources"]
    for row in ws_arr_res.rows:
        if row[0].value == "STATE_CODE":
            print("Arable Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setArrRes(row[1].value)
        elif row[0].value is not None:
            new_state = state_edit(row[0].value)
            new_state.setArrRes(row[1].value)
            edit_info[row[0].value] = new_state

    ws_cap_res = wb_reader["Capped Resources"]
    for row in ws_cap_res.rows:
        if row[0].value == "STATE_CODE":
            print("Capped Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setCapRes(row[1].value, str(row[2].value))
        elif row[0].value is not None:
            new_state = state_edit(row[0].value)
            new_state.setCapRes(row[1].value, str(row[2].value))
            edit_info[row[0].value] = new_state

    ws_uncap_res = wb_reader["Hidden Resources"]
    for row in ws_uncap_res.rows:
        if row[0].value == "STATE_CODE":
            print("Hidden Resources Started")
        elif row[0].value in edit_info:
            edit_info[row[0].value].setHiddenRes(row[1].value, str(row[2].value), row[3].value, row[4].value)
        elif row[0].value is not None:
            new_state = state_edit(row[0].value)
            new_state.setHiddenRes(row[1].value, str(row[2].value), row[3].value, row[4].value)
            edit_info[row[0].value] = new_state


def Editor(state_edit_info):
    #state_edit_info = state_edit()
    state_name = state_edit_info.statename
    raw_data_path = "raw_data/" + state_name + ".txt"
    modded_data_path = "modded_data/" + state_name + ".txt"
    state_info_raw = state_info(state_name)

    raw_data_r = open(raw_data_path, mode='r', encoding='utf-8-sig')
    mod_data_w = open(modded_data_path, mode = 'w', encoding= 'utf-8-sig')

    while(True):
        r_line = raw_data_r.readline()

        if not r_line:
            print(state_name + " Completed")
            raw_data_r.close()
            break
        elif r_line.find("arable_land") != -1:
            r_line = r_line.replace('\n', '')
            r_line_s = r_line.split(' ')
            state_info_raw.setArable(r_line_s[-1])
        elif r_line.find("arable_resource") != -1:
            r_line.replace('\n', '')
            r_line.replace('\t', '')
            r_line_s = r_line.split(' ')
            for res in r_line_s:
                if res != '' :
                    res = res.strip('"')
                    state_info_raw.setArrRes(res)
        elif r_line.find("capped_resource") != -1:
            while(True):
                r_line2 = raw_data_r.readline()

                if r_line2.find('}') != -1:
                    break
                r_line2.replace('\n', '')
                r_line2.replace('\t', '')
                r_line2_s = r_line2.split(' ')
                res_type = r_line2_s[-3]
                res_amount = r_line2_s[-1]
                state_info_raw.setCapRes(res_type, res_amount)
        elif r_line.find("resource") != -1 and r_line.find("capped_resource") == -1:
            discovered = True
            res_type = ""
            res_amount = 0
            dep_type = ""

            while(True):
                r_line2 = raw_data_r.readline()

                if r_line2.find('}') != -1:
                    state_info_raw.setHiddenRes(res_type, res_amount, dep_type, discovered)
                    break
                elif r_line2.find('type') != -1:
                    r_line2 = r_line2.replace('\n', '')
                    r_line2 = r_line2.replace('\t', '')
                    r_line2_s = r_line2.split(' ')
                    res_type = r_line2_s[-1].strip('"')
                elif r_line2.find('discovered') != -1:
                    r_line2 = r_line2.replace('\n', '')
                    r_line2 = r_line2.replace('\t', '')
                    r_line2_s = r_line2.split(' ')
                    res_amount = r_line2_s[-1].strip('"')
                    if r_line2.find('undiscovered') != -1: discovered = False
                elif r_line2.find('depleted_type') != -1:
                    r_line2 = r_line2.replace('\n', '')
                    r_line2 = r_line2.replace('\t', '')
                    r_line2_s = r_line2.split(' ')
                    dep_type = r_line2_s[-1].strip('"')
        elif r_line.find("naval_exit_id") != -1:
            r_line = r_line.replace('\n', '')
            r_line_s = r_line.split(' ')
            state_info_raw.setNavalExit(r_line_s[-1])
        elif r_line != "}\n":
            state_info_raw.appendStr(r_line)

    mod_data_w.writelines(''.join(state_info_raw.longstr_raw_data))
    if state_edit_info.arableland != 0:
        state_info_raw.setArable(state_edit_info.arableland)
    if len(state_edit_info.arable_resource) != 0:
        for res in state_edit_info.arable_resource:
            if res not in state_info_raw.arable_resource:
                state_info_raw.setArrRes(res)
            else:
                state_info_raw.arable_resource.remove(res)
    if len(state_edit_info.capped_resource) != 0:
        for res in state_edit_info.capped_resource:
            state_info_raw.capped_resource[res] = state_edit_info.capped_resource[res]
    if len(state_edit_info.hidden_resource) != 0:
        for res in state_edit_info.hidden_resource:
            state_info_raw.hidden_resource[res] = state_edit_info.hidden_resource[res]

    mod_data_w.writelines("    arable_land = " + state_info_raw.arableland + "\n")
    mod_data_w.writelines("    arable_resources = { ")
    for res in state_info_raw.arable_resource:
        if res != "" and res != "=" and res != "arable_resources" and res != "{" and res != "}" and res != "}\n":
            mod_data_w.writelines('"' + res + '" ')
    mod_data_w.writelines('}\n')
    mod_data_w.writelines("    capped_resources = {\n")
    for res in state_info_raw.capped_resource:
        amount = state_info_raw.capped_resource[res]
        if "\n" in amount: amount = amount.replace("\n", "")
        if amount != "0":
            mod_data_w.writelines("        " + res + " = " + amount + "\n")
    mod_data_w.writelines("    }\n")
    for res in state_info_raw.hidden_resource:
        amount = state_info_raw.hidden_resource[res][0]
        dept_type = state_info_raw.hidden_resource[res][1]
        discvd = state_info_raw.hidden_resource[res][2]

        if amount != "0":
            mod_data_w.writelines("    resource = {\n")
            mod_data_w.writelines("        type = \"" + res + "\"\n")
            if dept_type is not None and dept_type != "":
                mod_data_w.writelines("        depleted_type = \"")
                mod_data_w.writelines(dept_type)
                mod_data_w.writelines("\"\n")
            mod_data_w.writelines("        ")
            if not discvd:
                mod_data_w.writelines("un")
            mod_data_w.writelines("discovered_amount = ")
            mod_data_w.writelines(amount)
            mod_data_w.writelines("\n")
            mod_data_w.writelines("    }\n")
    if state_info_raw.naval_exit_id != -1:
        mod_data_w.writelines("    naval_exit_id = ")
        mod_data_w.writelines(str(state_info_raw.naval_exit_id))
        mod_data_w.writelines("\n")
    mod_data_w.writelines("}")
    mod_data_w.close()
# Main
input_path = "input.xlsx"
fail_path = "error.txt"
editinfo = dict()
EditInfoReader(input_path, editinfo)
print("Input Data Reading Completed")

for state in editinfo:
    Editor(editinfo[state])

