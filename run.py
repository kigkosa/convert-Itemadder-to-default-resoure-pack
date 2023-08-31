import glob
import shutil
import os
import yaml

import json

# gen fonder ia
if not os.path.isdir('./ItemsAdder'):
    os.mkdir('./ItemsAdder') 
    os.mkdir('./ItemsAdder/contents') 
    exit()



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
    


itemadder = './ItemsAdder/contents'
item_m = {}
id = 0


fix_id_10101=False
ec_mode =False

if fix_id_10101 ==False:
    with open('./custom_model_data.txt','r') as file:
        id = int(file.read())
else:
    id = 10101
alt_dat = []
for get_namespace in os.listdir(itemadder):
    for get_file in os.listdir(itemadder+"/"+get_namespace+"/configs"):


        with open(itemadder+"/"+get_namespace+"/configs"+"/"+get_file) as file:
            documents = yaml.full_load(file)
            if not os.path.exists('./Output/assets/'+documents['info']['namespace']):
                shutil.copytree(itemadder+'/'+get_namespace+"/resourcepack/assets/"+documents['info']['namespace'],'./Output/assets/'+documents['info']['namespace'])
            if  'items' in documents: 
                
                for key in documents['items']:
                    
                    if documents['items'][key]['resource']['generate'] is False:
                        with open('./Output/assets/'+documents['info']['namespace']+'/models/'+documents['items'][key]['resource']['model_path']+'.json', 'r') as f:
                            data = json.load(f)
                        for i in data['textures']:
                            alt_dat.append(data['textures'][i])
                        

                        
                        if documents['items'][key]['resource']['material'] not in item_m:
                            item_m[documents['items'][key]['resource']['material']] = []
                        documents['items'][key]['resource']['model_path'] = documents['info']['namespace']+':'+documents['items'][key]['resource']['model_path']
                        
                        if 'model_id' in documents['items'][key]['resource'] :
                            item_m[documents['items'][key]['resource']['material']].append({ documents['items'][key]['resource']['model_id']:documents['items'][key]})
                            
                        else:
                            item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                            id=id+1
                    else:
                        if 'material' in documents['items'][key]['resource']:
                            _met = documents['items'][key]['resource']['material'].lower()
                            data = {}
                            for file in glob.glob("./default_model/**/"+_met+".json", recursive=True):
                                with open(file, 'r') as f:
                                    data = json.load(f)
                            data['textures']['layer0'] = documents['info']['namespace']+':'+documents['items'][key]['resource']['textures'][0]
                            with open('./Output/assets/'+documents['info']['namespace']+'/models/'+key+'.json', 'w') as jsonfile:
                                json.dump(data, jsonfile)
                            # alt_dat.append( documents['info']['namespace']+':'+documents['items'][key]['resource']['textures'][0])
                            documents['items'][key]['resource']['model_path'] = documents['info']['namespace']+':'+key
                            if documents['items'][key]['resource']['material'] not in item_m:
                                item_m[documents['items'][key]['resource']['material']] = []
                            if documents['items'][key]['resource']['model_id'] is not None:
                                item_m[documents['items'][key]['resource']['material']].append({ documents['items'][key]['resource']['model_id']:documents['items'][key]})
                            else:                            
                                item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                                id=id+1
                            # alt_dat.append( documents['info']['namespace']+':'+documents['items'][key]['resource']['textures'][0])
                            for i in documents['items'][key]['resource']['textures']:
                                alt_dat.append( documents['info']['namespace']+':'+i)

             

                    
        alt_dat = sorted(set(alt_dat))
        alt_data = { "sources": [  ]}
        
        for i in alt_dat:
            alt_data['sources'].append({ "type": "single", "resource": i })
    
        # /Output/assets/minecraft/atlases/blocks.json check create path
        if not os.path.exists("./Output/assets/minecraft"):
            os.mkdir('./Output/assets/minecraft')
        if not os.path.exists("./Output/assets/minecraft/atlases"):
            os.mkdir('./Output/assets/minecraft/atlases')
        if os.path.exists("./Output/assets/minecraft/atlases/blocks.json"):
            os.remove("./Output/assets/minecraft/atlases/blocks.json")
        with open('./Output/assets/minecraft/atlases/blocks.json', 'w') as jsonfile:
            json.dump(alt_data, jsonfile)

                

# slot item_m custom_model_data by id

for k in item_m:
    
    for get_default_model_type in os.listdir(f"./default_model"):
        for get_default_model in os.listdir(f"./default_model/{get_default_model_type}"):
            if get_default_model == k.lower()+".json":
                with open(f"./default_model/{get_default_model_type}/{get_default_model}", 'r') as f:
                    data = json.load(f)
                
                if 'overrides' not in data:
                    data['overrides'] = []
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
            
                
                sl = {}
                for i in data["overrides"]:
                    if "custom_model_data" in i["predicate"]:
                        sl[i["predicate"]["custom_model_data"]] = i
                # slot key sl
                data["overrides"] = []
                for i in sorted(sl):
                    data["overrides"].append(sl[i])
                with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
                    json.dump(data, jsonfile)
if fix_id_10101 ==False:
    with open('./custom_model_data.txt', 'w') as f:
        id +=1
        f.write(str(id))
if ec_mode == True:
    shutil.copy('ec_pack.mcmeta','./Output/pack.mcmeta')
    shutil.copy('How to get items.txt','./Output/How to get items.txt')
print('Done!')