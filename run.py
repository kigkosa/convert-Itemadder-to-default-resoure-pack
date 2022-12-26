import shutil
import os
import yaml

import json

# gen fonder ia
if not os.path.isdir('./ItemsAdder'):
    os.mkdir('./ItemsAdder') 
    os.mkdir('./ItemsAdder/data') 
    exit()

# itemadder new to old
if os.path.isdir('./ItemsAdder/contents'):
    if os.path.isdir('./ItemsAdder/data'):
        shutil.rmtree('./ItemsAdder/data')
        os.mkdir('./ItemsAdder/data') 
        os.mkdir('./ItemsAdder/data/items_packs')

         
    for get_namespace in os.listdir('./ItemsAdder/contents'):
        shutil.copytree('./ItemsAdder/contents/'+get_namespace+'/configs','./ItemsAdder/data/items_packs/'+get_namespace)
        shutil.copytree('./ItemsAdder/contents/'+get_namespace+'/resourcepack','./ItemsAdder/data/resource_pack')
    shutil.rmtree('./ItemsAdder/contents')


# check file and gen file
if not os.path.exists("./custom_model_data.txt"):
    with open('./custom_model_data.txt','w') as f:
        f.write('0')

# gen fonder output
if os.path.isdir('./Output'):
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
                        if documents['items'][key]['resource']['material'] not in item_m:
                            item_m[documents['items'][key]['resource']['material']] = []
                        documents['items'][key]['resource']['model_path'] = documents['info']['namespace']+':'+documents['items'][key]['resource']['model_path']
                        item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                        id=id+1

for k in item_m:

    for get_default_model_type in os.listdir(f"./default_model"):
        for get_default_model in os.listdir(f"./default_model/{get_default_model_type}"):
            if get_default_model == k.lower()+".json":
                with open(f"./default_model/{get_default_model_type}/{get_default_model}", 'r') as f:
                    data = json.load(f)
               
                if 'overrides' not in data:
                    data['overrides'] = []
                
                for d in item_m[k]:
                    for di in item_m[k]:
                        for kk in di:
                            data['overrides'].append({"predicate": {"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']})
                            if k == "BOW":
                                

                                data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1}, "model":  di[kk]['resource']['model_path']+"_0"})
                                data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1,"pull": 0.65}, "model":  di[kk]['resource']['model_path']+"_1"})
                                data['overrides'].append({"predicate": {"custom_model_data": kk ,"pulling": 1,"pull": 0.09}, "model":  di[kk]['resource']['model_path']+"_2"})
                            elif k == "SHIELD":
                                data['overrides'][0]['model'] = "item/shield"
                                data['overrides'].append({"predicate": {"custom_model_data": kk ,"blocking": 1}, "model":  di[kk]['resource']['model_path']+"_blocking"})
                            elif k == "FISHING_ROD":
                                data['overrides'].append({"predicate": {"custom_model_data": kk ,"cast": 1}, "model":  di[kk]['resource']['model_path']+"_cast"})
                            elif k == "CROSSBOW":
                                data['overrides'].append({"predicate": {"charged": 1,"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']+"_charged"})
                                data['overrides'].append({"predicate": {"charged": 1,"firework": 1,"custom_model_data": kk }, "model":  di[kk]['resource']['model_path']+"_firework"})
                

                with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
                    json.dump(data, jsonfile)

with open('./custom_model_data.txt', 'w') as f:
    id +=1
    f.write(str(id))
print('Done!')