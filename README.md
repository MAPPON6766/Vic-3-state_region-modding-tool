# Intoduction
Modding tool for state_region in Victoria 3. The tool will help you editting state_region.txt file which defines arable lands, arable resources, quantified resources and its amount

If there was an error after running or if the program did not work properly, please leave it on Issues. I would appreciate it if you could upload the excel file as well.

# How To Use It
If you downloaded files withe executable version, then file consists of two executable program, `splitter.exe` and `editor.exe`, and one excel file named `input.xlsx`. This is how to use it.
 1. Copy and paste ALL text files in `.../Victoria 3/game/map_data/state_regions` to `state_regions` folder in the program.
 2. Run `splitter.exe`. The excutable separates text files in the state_regions folder by state. The execution results can be found in the `raw_data` folder.
 3. Edit `input.xlsx`. `input.xlsx` consists of 5 worksheets, `Arable Lands`, `Arable Resources`  `Capped Resouces`, `Uncapped Resources` and `Uncapped Resources (Discovered)`.
    * `Arable Lands` : Write the state code(e.g. `STATE_SVEALAND`) and number on this worksheet to replace the arable land in the state with the filled number.
    * `Arable Resources` : Write the state code and building group code(e.g. `bg_tea_plantations`). If the building group is arable in the state, it will be deleted. Vice versa, the building group unavailable in the state will become available.
    * `Capped Resources` : Write the state code, building group code and amount. If you want to eliminate the original resource, write 0 for the amount.
    * `Uncapped Resources` : Write the state code, building group code, amount and depleted types(Optional). If you want to eliminate the original resource, write 0 for the amount.
    * `Uncapped Resources (Discovered)`: Write the state code, building group code, amount and depleted types(Optional). If you want to eliminate the original resource, write 0 for the amount. What is written on worksheet discovered at the start of the game, like the Rubber Plantation in Brazil. 
 4. Run 'editor.exe`. This executable modifies the text files in `raw_data` folder based on `input.xlsx` and saves them in `modded_data`.
 5. Copy and paste text files in `modded_files` to `(your mod folder)\map_data\state_regions` folder.
 6. Run Victoria 3 and check the verification.
 
 # Caution
 * Do NOT delete folder state_regions, modded_data and raw_data
 * Do NOT change the worksheet name
 * Do NOT change the name of text files in state_regions and raw_data
 * Follow CORRECTLY input.xlsx format.
 
 # Known Issues
  * Program do NOT run properly when you added capped resources in the state with no capped resouces originally.
 
 # pre-Installation via python
 This program used `openpyxl` library. You should download the libray before use python file. : `pip install openpyxl`
