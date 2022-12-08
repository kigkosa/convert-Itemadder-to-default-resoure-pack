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
                print(di[kk]['display_name'])
    with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

with open('./custom_model_data.txt', 'w') as f:
    id +=1
    f.write(str(id))