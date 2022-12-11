import shutil
import os
import yaml

import json

# gen fonder ia
if not os.path.isdir('./ItemsAdder'):
    os.mkdir('./ItemsAdder') 
    os.mkdir('./ItemsAdder/data') 
    exit()

# check file and gen file
if not os.path.exists("./custom_model_data.txt"):
    with open('./custom_model_data.txt','w') as f:
        f.write('0')

# gen fonder output
shutil.rmtree('./Output')
if not os.path.isdir('./Output'):
    os.mkdir('./Output') 
    os.mkdir('./Output/assets') 
    shutil.copyfile('./pack.mcmeta','./Output/pack.mcmeta')
    os.mkdir('./Output/assets/minecraft') 
    os.mkdir('./Output/assets/minecraft/models') 
    os.mkdir('./Output/assets/minecraft/models/item') 
    

itemadder = './ItemsAdder/data/resource_pack/assets'
for get_namespace in os.listdir(itemadder):
    shutil.copytree(itemadder+'/'+get_namespace,'./Output/assets/'+get_namespace)
itemadder = './ItemsAdder/data/items_packs'
item_m = {}
id = 0
with open('./custom_model_data.txt','r') as file:
    id = int(file.read())
for get_namespace in os.listdir(itemadder):
    for get_file in os.listdir(itemadder+"/"+get_namespace):
        with open(itemadder+"/"+get_namespace+"/"+get_file) as file:
            documents = yaml.full_load(file)
            if  'items' in documents: 
                for key in documents['items']:
                    if documents['items'][key]['resource']['generate'] is False:
                        # if documents['items'][key]['resource']['material'] in item_m:
                        if documents['items'][key]['resource']['material'] not in item_m:
                            item_m[documents['items'][key]['resource']['material']] = []
                        # print(documents['items'][key]['resource']['model_path'])
                        documents['items'][key]['resource']['model_path'] = documents['info']['namespace']+':'+documents['items'][key]['resource']['model_path']
                        item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                        id=id+1

for k in item_m:
    data = {"parent": "minecraft:item/generated","textures": {"layer0": "minecraft:item/"+k.lower()},"overrides": []}
    for d in item_m[k]:
        for di in item_m[k]:
            for kk in di:
                data['overrides'].append({"predicate": {"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']})
                
                if k == "BOW":
                    data["display"] = {"thirdperson_righthand":{"rotation":[-80,260,-40],"translation":[-1,-2,2.5],"scale":[0.9,0.9,0.9]},"thirdperson_lefthand":{"rotation":[-80,-280,40],"translation":[-1,-2,2.5],"scale":[0.9,0.9,0.9]},"firstperson_righthand":{"rotation":[0,-90,25],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]},"firstperson_lefthand":{"rotation":[0,90,-25],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]}}
                    data['overrides'].append({"predicate":{"pulling":1},"model":"item/bow_pulling_0"})
                    data['overrides'].append({"predicate":{"pulling":1,"pull":0.65},"model":"item/bow_pulling_1"})
                    data['overrides'].append({"predicate":{"pulling":1,"pull":0.9},"model":"item/bow_pulling_2"})
                    
                    data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1}, "model":  di[kk]['resource']['model_path']+"_0"})
                    data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1,"pull": 0.65}, "model":  di[kk]['resource']['model_path']+"_1"})
                    data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1,"pull": 0.09}, "model":  di[kk]['resource']['model_path']+"_2"})
                elif k == "SHIELD":
                    data["parent"] = "builtin/entity"
                    data["gui_light"] = "front"
                    data["display"] = {"thirdperson_righthand":{"rotation":[0,90,0],"translation":[10,6,-4],"scale":[1,1,1]},"thirdperson_lefthand":{"rotation":[0,90,0],"translation":[10,6,12],"scale":[1,1,1]},"firstperson_righthand":{"rotation":[0,180,5],"translation":[-10,2,-10],"scale":[1.25,1.25,1.25]},"firstperson_lefthand":{"rotation":[0,180,5],"translation":[10,0,-10],"scale":[1.25,1.25,1.25]},"gui":{"rotation":[15,-25,-5],"translation":[2,3,0],"scale":[0.65,0.65,0.65]},"fixed":{"rotation":[0,180,0],"translation":[-2,4,-5],"scale":[0.5,0.5,0.5]},"ground":{"rotation":[0,0,0],"translation":[4,4,2],"scale":[0.25,0.25,0.25]}}
                    data["textures"]= {"particle": "block/dark_oak_planks" }
                    data['overrides'].append({"predicate": {"custom_model_data": kk ,"blocking": 1}, "model":  di[kk]['resource']['model_path']+"_blocking"})
                elif k == "FISHING_ROD":
                    data["parent"] = "item/handheld_rod"
                    data['overrides'].append({"predicate": {"cast": 1},"model": "item/fishing_rod_cast"})
                    data['overrides'].append({"predicate": {"custom_model_data": kk ,"cast": 1}, "model":  di[kk]['resource']['model_path']+"_cast"})
                elif k == "CROSSBOW":
                    data['textures']['layer0'] = 'item/crossbow_standby'
                    data["display"] = {"thirdperson_righthand":{"rotation":[-90,0,-60],"translation":[2,0.1,-3],"scale":[0.9,0.9,0.9]},"thirdperson_lefthand":{"rotation":[-90,0,30],"translation":[2,0.1,-3],"scale":[0.9,0.9,0.9]},"firstperson_righthand":{"rotation":[-90,0,-55],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]},"firstperson_lefthand":{"rotation":[-90,0,35],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]}}
                    # data['display'].append({"thirdperson_righthand":{"rotation":[-90,0,-60],"translation":[2,0.1,-3],"scale":[0.9,0.9,0.9]},"thirdperson_lefthand":{"rotation":[-90,0,30],"translation":[2,0.1,-3],"scale":[0.9,0.9,0.9]},"firstperson_righthand":{"rotation":[-90,0,-55],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]},"firstperson_lefthand":{"rotation":[-90,0,35],"translation":[1.13,3.2,1.13],"scale":[0.68,0.68,0.68]}})
                    data['overrides'].append({"predicate": {"pulling": 1 }, "model":  'item/crossbow_pulling_0'})
                    data['overrides'].append({"predicate": {"pulling": 1,"pull": 0.58 }, "model":  'item/crossbow_pulling_1'})
                    data['overrides'].append({"predicate": {"pulling": 1,"pull": 1.0 }, "model":  'item/crossbow_pulling_2'})
                    data['overrides'].append({"predicate": {"charged": 1 }, "model":  'item/crossbow_arrow'})
                    data['overrides'].append({"predicate": {"charged": 1,"firework": 1 }, "model":  'item/crossbow_firework'})
                    data['overrides'].append({"predicate": {"charged": 1,"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']+"_charged"})
                    data['overrides'].append({"predicate": {"charged": 1,"firework": 1,"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']+"_firework"})
                elif k == "SEA_LANTERN":
                    data["parent"] = "minecraft:block/sea_lantern"


                print(k)
    with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

with open('./custom_model_data.txt', 'w') as f:
    id +=1
    f.write(str(id))