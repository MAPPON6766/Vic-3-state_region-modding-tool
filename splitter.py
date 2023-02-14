def SplitState(path):
    txtreader = open(path, mode='r', encoding='utf-8-sig')

    while(True):
        t_line = txtreader.readline()

        if not t_line:
            print(path + "완료")
            txtreader.close()
            break

        if t_line.find("STATE") != -1:
            spilted = t_line.split(" ")
            state_name = spilted[0]
            txtwriter = open("raw_data/" + state_name + ".txt", mode = 'w', encoding = 'utf-8-sig')
            txtwriter.writelines("#Original File : " + path + "\n")
            txtwriter.writelines(t_line)

            while(True):
                t_line_2 = txtreader.readline()
                txtwriter.writelines(t_line_2)
                if t_line_2 == "}\n" or t_line_2 == "}":
                    txtwriter.close()
                    break

SplitState("state_regions/00_west_europe.txt")
SplitState("state_regions/01_south_europe.txt")
SplitState("state_regions/02_east_europe.txt")
SplitState("state_regions/03_north_africa.txt")
SplitState("state_regions/04_subsaharan_africa.txt")
SplitState("state_regions/05_north_america.txt")
SplitState("state_regions/06_central_america.txt")
SplitState("state_regions/07_south_america.txt")
SplitState("state_regions/08_middle_east.txt")
SplitState("state_regions/09_central_asia.txt")
SplitState("state_regions/10_india.txt")
SplitState("state_regions/11_east_asia.txt")
SplitState("state_regions/12_indonesia.txt")
SplitState("state_regions/13_australasia.txt")
SplitState("state_regions/14_siberia.txt")