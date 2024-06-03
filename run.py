import glob
import shutil
import os
import yaml

import json

import requests
import io
import zipfile

from PIL import Image

def hex_to_rgb(hex_color):
    # Remove the '#' character if it's there
    hex_color = hex_color.lstrip('#')
    
    # Convert the hex string to RGB tuple
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb
def hex_to_dec(hex_color):
    hex_color = hex_color.lstrip('#')
    return str(int(hex_color, 16))


def add_img_armor(input_img,output_img):
    image1 = Image.open(output_img)
    image2 = Image.open(input_img)

    width1, height1 = image1.size
    width2, height2 = image2.size
    max_height = max(height1, height2)
    # if height1 < height2:        
    #     image1 = image1.resize(((width2*2), height2))
    if height2 < height1:        
        # image1 = Image.open()
        image1 = Image.open("./default_model/textures/models/armor_16/"+os.path.basename(output_img))
        max_height = min(height1, height2)
        with open('./Output/assets/minecraft/shaders/core/rendertype_armor_cutout_no_cull.fsh', 'r') as f:
            shader = f.read()
        shader = shader.replace("#define TEX_RES 32","#define TEX_RES 16")
        with open('./Output/assets/minecraft/shaders/core/rendertype_armor_cutout_no_cull.fsh', 'w') as f:
            f.write(shader)
            
    width1, height1 = image1.size
    width2, height2 = image2.size


    total_width = width1 + width2 

    combined_image = Image.new('RGBA', (total_width, max_height))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (width1, 0))
    combined_image.save(output_img)

if not os.path.exists("./pack.mcmeta"):
    with open('./pack.mcmeta', 'w') as f:
        f.write('{"pack":{"pack_format":16,"supported_formats": {"min_inclusive": 16, "max_inclusive": 24},"description":""}}')
if not os.path.isdir("./default_model"):
    # https://github.com/kigkosa/convert-Itemadder-to-default-resoure-pack/raw/master/default_model.zip
    response = requests.get('https://github.com/kigkosa/convert-Itemadder-to-default-resoure-pack/raw/master/default_model.zip')
    response.raise_for_status()
    zip_file = io.BytesIO(response.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('./')

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


fix_id_10101=True

list_give_items = []
list_give_items_1_20_6 = []
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
                        namespace = documents['info']['namespace']
                        model_path = documents['items'][key]['resource']['model_path']

                        
                        with open('./Output/assets/'+namespace+'/models/'+model_path+'.json', 'r') as f:
                            data = json.load(f)
                        
                        for i in data['textures']:
                            alt_dat.append(data['textures'][i])
                        
     

                        if documents['items'][key]['resource']['material'] == "BOW":
                            for tx in ["","_0","_1","_2"]:
                                with open('./Output/assets/'+namespace+'/models/'+model_path+tx+'.json', 'r') as f:
                                    data2 = json.load(f)                                
                                for i in data2['textures']:
                                    if data2['textures'][i] not in alt_dat:
                                        alt_dat.append(data2['textures'][i])    
                            
                        if documents['items'][key]['resource']['material'] == "CROSSBOW":
                            for tx in ["","_0","_1","_2","_charged","_firework"]:
                                with open('./Output/assets/'+namespace+'/models/'+model_path+tx+'.json', 'r') as f:
                                    data2 = json.load(f)                                
                                for i in data2['textures']:
                                    if data2['textures'][i] not in alt_dat:
                                        alt_dat.append(data2['textures'][i])    
                       
                        if documents['items'][key]['resource']['material'] == "FISHING_ROD":
                            for tx in ["","_cast"]:
                                with open('./Output/assets/'+namespace+'/models/'+model_path+tx+'.json', 'r') as f:
                                    data2 = json.load(f)                                
                                for i in data2['textures']:
                                    if data2['textures'][i] not in alt_dat:
                                        alt_dat.append(data2['textures'][i])    
                       
                        if documents['items'][key]['resource']['material'] not in item_m:
                            item_m[documents['items'][key]['resource']['material']] = []
                        documents['items'][key]['resource']['model_path'] = documents['info']['namespace']+':'+documents['items'][key]['resource']['model_path']
                        
                        if 'model_id' in documents['items'][key]['resource'] :
                            item_m[documents['items'][key]['resource']['material']].append({ documents['items'][key]['resource']['model_id']:documents['items'][key]})
                            list_give_items.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"{CustomModelData:"+str(documents['items'][key]['resource']['model_id'])+",display:{Name:'[{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}]'}}")
                            list_give_items_1_20_6.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"[custom_model_data="+str(documents['items'][key]['resource']['model_id'])+",custom_name='{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}']")
                            
                        else:
                            item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                            list_give_items.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"{CustomModelData:"+str(id)+",display:{Name:'[{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}]'}}")
                            list_give_items_1_20_6.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"[custom_model_data="+str(id)+", custom_name='{\"text\":\""+documents['items'][key]["display_name"]+"\", \"italic\":false}']")
                     

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
                                list_give_items.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"{CustomModelData:"+str(documents['items'][key]['resource']['model_id'])+",display:{Name:'[{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}]'}}")
                                list_give_items_1_20_6.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"[custom_model_data="+str(documents['items'][key]['resource']['model_id'])+", custom_name='{\"text\":\""+documents['items'][key]["display_name"]+"\", \"italic\":false}']")
                            else:                            
                                item_m[documents['items'][key]['resource']['material']].append({ id:documents['items'][key]})
                                list_give_items.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"{CustomModelData:"+str(id)+",display:{Name:'[{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}]'}}")
                                list_give_items_1_20_6.append(namespace+":"+model_path+"  |  /minecraft:give @p minecraft:"+documents['items'][key]['resource']['material'].lower()+"[custom_model_data="+str(id)+", custom_name='{\"text\":\""+documents['items'][key]["display_name"]+"\", \"italic\":false}']")
                                id=id+1
                            # alt_dat.append( documents['info']['namespace']+':'+documents['items'][key]['resource']['textures'][0])
                            for i in documents['items'][key]['resource']['textures']:
                                alt_dat.append( documents['info']['namespace']+':'+i)
                        else:
                            if 'specific_properties' in documents['items'][key]:
                                if 'armor' in documents['items'][key]['specific_properties']:
                                    namespace = documents['info']['namespace']
                                    
                                    texture_path = documents['items'][key]['resource']['textures'][-1] .replace(".png","")
                                    alt_dat.append( namespace+":"+texture_path)
                                    # print(documents['items'][key]['specific_properties']['armor']['slot'])
                                    _met = documents['items'][key]['specific_properties']['armor']['slot'].lower()
                                    armor_list = {"head":"leather_helmet","chest":"leather_chestplate","legs":"leather_leggings","feet":"leather_boots"}
                                    data = {}
                                    for file in glob.glob("./default_model/**/"+armor_list[_met]+".json", recursive=True):
                                        with open(file, 'r') as f:
                                            data = json.load(f)
                                    icon_json = {"parent": "minecraft:item/generated","textures": {"layer0": "item/empty","layer1": namespace+":"+texture_path}}
                                    # wite json
                                    with open('./Output/assets/'+namespace+'/models/'+key+'.json', 'w') as jsonfile:
                                        json.dump(icon_json, jsonfile)
                                    if 'overrides' not in data:
                                        data['overrides'] = []
                                    _color=documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['color']              
                                    list_give_items.append(namespace+":"+key+"  |  /minecraft:give @p minecraft:"+armor_list[_met].lower()+"{CustomModelData:"+str(id)+",display:{Name:'[{\"text\":\""+documents['items'][key]["display_name"]+"\",\"italic\":false}]',color:"+hex_to_dec(_color)+"}}")
                                    list_give_items_1_20_6.append(namespace+":"+key+"  |  /minecraft:give @p minecraft:"+armor_list[_met].lower()+"[custom_model_data="+str(id)+", custom_name='{\"text\":\""+documents['items'][key]["display_name"]+"\", \"italic\":false}',dyed_color={rgb:"+hex_to_dec(_color)+"}]")
                                    data['overrides'].append({"predicate": {"custom_model_data": id }, "model":  namespace+":"+key})
                                    id=id+1                                   
                                    
                                
                                    
                                    
                                    
                                    

                                    # red and edit file
                                    with open('./Output/assets/minecraft/models/item/'+armor_list[_met]+'.json', 'w') as jsonfile:
                                        json.dump(data, jsonfile)
                                    if not os.path.exists("./Output/assets/minecraft/textures"):
                                        os.makedirs("./Output/assets/minecraft/textures")
                                    if not os.path.exists("./Output/assets/minecraft/textures/item"):
                                        os.makedirs("./Output/assets/minecraft/textures/item")
                                        shutil.copy("./default_model/textures/item/empty.png","./Output/assets/minecraft/textures/item")
                                    if not os.path.exists("./Output/assets/minecraft/textures/models/armor"):                                        
                                        shutil.copytree("./default_model/textures/models/armor","./Output/assets/minecraft/textures/models/armor")
                                    
                                    
                                    if 'chest' ==_met:
                                        _layer_1 =documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['layer_1']
                                        _layer_2 =documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['layer_2']
                                        _color=documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['color']
                                        
                                        if not os.path.exists("./Output/tmp/armors"):
                                            os.makedirs("./Output/tmp/armors")       
                                        if not os.path.exists("./Output/assets/minecraft/shaders"):
                                            shutil.copytree("./default_model/shaders", "./Output/assets/minecraft/shaders")

                                        img = Image.open(itemadder+'/'+get_namespace+"/resourcepack/assets/"+namespace+"/textures/"+_layer_1+".png")
                                        img = img.convert("RGBA")
                                        pixels = img.load()
                                        # print(hex_to_rgb(_color))
                                        pixels[0,0] = hex_to_rgb(_color)
                                        img.save("./Output/tmp/armors/"+os.path.basename(_layer_1)+".png")
                                        add_img_armor("./Output/tmp/armors/"+os.path.basename(_layer_1)+".png","./Output/assets/minecraft/textures/models/armor/leather_layer_1.png")

                                        
                                        img = Image.open(itemadder+'/'+get_namespace+"/resourcepack/assets/"+namespace+"/textures/"+_layer_2+".png")
                                        img = img.convert("RGBA")
                                        pixels = img.load()
                                        pixels[0,0] = hex_to_rgb(_color)
                                        if not os.path.exists("./Output/tmp/armors"):
                                            os.makedirs("./Output/tmp/armors")                                 
                                        img.save("./Output/tmp/armors/"+os.path.basename(_layer_2)+".png")
                                        add_img_armor("./Output/tmp/armors/"+os.path.basename(_layer_2)+".png","./Output/assets/minecraft/textures/models/armor/leather_layer_2.png")
                                        

                            

                                    


             

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
                # data["overrides"] = []
                # for i in sorted(sl):
                #     data["overrides"].append(sl[i])
                with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
                    json.dump(data, jsonfile)
for items in glob.glob("./Output/assets/minecraft/models/item/*.json"):
    with open(items, 'r') as f:
        data = json.load(f)
    _id_max = data['overrides'][-1]['predicate']['custom_model_data']+1
    data['overrides'].append({ "predicate": { "custom_model_data": _id_max }, "model": "item/"+os.path.basename(items).replace(".json","") })
    with open(items, 'w') as jsonfile:
        json.dump(data, jsonfile)

if fix_id_10101 ==False:
    with open('./custom_model_data.txt', 'w') as f:
        id +=1
        f.write(str(id))
if os.path.exists("./Output/tmp"):
    shutil.rmtree("./Output/tmp")
# list_give_items to text
with open('./Output/give_items.txt', 'w') as f:
    for i in list_give_items:
        f.write(i+'\n\n')
with open('./Output/give_items_1_20_6.txt', 'w') as f:
    for i in list_give_items_1_20_6:
        f.write(i+'\n\n')
# if os.path.exists("C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output"):
#     shutil.rmtree("C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output")
# shutil.copytree('./Output', 'C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output')    

print('Done!')