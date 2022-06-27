# random scratchpad
import yaml

my_dict = {}

def emptycheck(dict):
    if not dict:
        print("Empty")
    else:
        print("Full")


#emptycheck(my_dict)

my_dict["entry"] = "cottage cheese"

#emptycheck(my_dict) 

# !! Prints all the major (outermost) keys of the giant json document: 
# print(results_dict.keys())

# This succsesfully changes a loaded yaml file into a dict!!! 
with open("raw_data.yaml", "r") as file:
    yamlize = yaml.load(file, yaml.FullLoader)
    print(yamlize)

print(type(yamlize))

for key in yamlize:
    print(key)

'''
# Lol this just recreated all the original json files 
for key in results_dict:
    rootname = key
    txtfilename = rootname + ".json"
    with open(txtfilename, "w") as file:
        file.write(json.dumps(results_dict[rootname]))
#    with open(rootname.json)
with open("ngfw_zones.json", "w") as file:
    file.write(json.dumps(results_dict['ngfw_zones']))
'''
