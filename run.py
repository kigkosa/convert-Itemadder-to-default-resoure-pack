import glob
import shutil
import os
import yaml

import json

import requests
import io
import zipfile

from PIL import Image

import random

def generate_random_unused_unicode():
    # Generate a random integer within a range of less common Unicode characters
    code_point = random.randint(0xE000, 0xF8FF)
    
    # Convert the integer to a Unicode character
    unicode_char = chr(code_point)
    
    return unicode_char

def pain_armor(part_file,hex):
    img = Image.open(part_file)
    img = img.convert("RGBA")
    pixels = img.load()
    pixels[0,0] = hex_to_rgb(hex)
    img.save(part_file)

def font_image_unicode(name):
    list_unicode = []
    with open("./storage/font_images_unicode_cache.yml", 'r', encoding='utf-8') as file:
        history = yaml.safe_load(file)
    if history != None:
        for his in history:
            if his == name:
                return history[his]
            list_unicode.append(history[his])
    unicode = generate_random_unused_unicode()
    while unicode in list_unicode:
        unicode = generate_random_unused_unicode()
    with open("./storage/font_images_unicode_cache.yml", 'a', encoding='utf-8') as file:
        yaml.dump({name:unicode}, file, sort_keys=False,allow_unicode=True)
    return unicode


def item_get_cmdata(type:str,name:str):
    # read yml
    _custommodeldata = 10101
    history = {}
    with open("./storage/items_cache.yml", 'r', encoding='utf-8') as file:
        _history = yaml.safe_load(file)
        if _history != None:
            history = _history
    
    if type.upper() in history:
        if name in history[type.upper()]:
            return int(history[type.upper()][name])
        else:
            _custommodeldata = max(history[type.upper()].values())+1
            history[type.upper()][name] = _custommodeldata
    else:        
        history[str(type.upper())] = {name:_custommodeldata}
    with open("./storage/items_cache.yml", 'w', encoding='utf-8') as file:
        yaml.dump(history, file,sort_keys=False)
    return int(_custommodeldata)
    
        

def hex_to_rgb(hex_color):
    # Remove the '#' character if it's there
    hex_color = hex_color.lstrip('#')
    
    # Convert the hex string to RGB tuple
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    return rgb
def hex_to_dec(hex_color):
    hex_color = hex_color.lstrip('#')
    return str(int(hex_color, 16))


def add_img_armor(input_img,layer_name,input_colors):
    max_height_size = 0
    max_width_size = 0
    
    for part_img in input_img:
        _im = Image.open(part_img)
        _width, _height = _im.size
        if _height > max_height_size:
            max_height_size = _height
        if _width > max_width_size:
            max_width_size = _width
    for part_img in input_img:
        _im = Image.open(part_img)
        _width, _height = _im.size
        _im = _im.resize((max_width_size, max_height_size),Image.NEAREST)
        _im.save("./Output/tmp/armors/"+layer_name+"/"+os.path.basename(part_img))
        pain_armor("./Output/tmp/armors/"+layer_name+"/"+os.path.basename(part_img),input_colors[os.path.basename(part_img)])
        os.remove(part_img)
    shutil.copy(f"./default_model/textures/models/armor_{max_height_size}/leather_{layer_name}.png",f"./Output/assets/minecraft/textures/models/armor/leather_{layer_name}.png")
    
    
    image1 = Image.open(f"./Output/assets/minecraft/textures/models/armor/leather_{layer_name}.png")
    width1, height1 = image1.size
    
    for img_armor in glob.glob("./Output/tmp/armors/"+layer_name+"/*"):
        image2 = Image.open(img_armor)
        width2, height2 = image2.size
        total_width = width1 + width2
        combined_image = Image.new('RGBA', (total_width, max_height_size))
        combined_image.paste(image1, (0, 0))
        combined_image.paste(image2, (width1, 0))
        combined_image.save(f"./Output/assets/minecraft/textures/models/armor/leather_{layer_name}.png")
        image1 = Image.open(f"./Output/assets/minecraft/textures/models/armor/leather_{layer_name}.png")
        width1, height1 = image1.size

    if max_height_size == 32:
        with open('./Output/assets/minecraft/shaders/core/rendertype_armor_cutout_no_cull.fsh', 'r') as f:
            shader = f.read()
        shader = shader.replace("#define TEX_RES 32","#define TEX_RES 16")
        with open('./Output/assets/minecraft/shaders/core/rendertype_armor_cutout_no_cull.fsh', 'w') as f:
            f.write(shader)



if not os.path.exists("./storage"):
    os.mkdir("./storage")
if not os.path.exists("./storage/font_images_unicode_cache.yml"):
    with open('./storage/font_images_unicode_cache.yml', 'w', encoding='utf-8') as f:
        f.write('')
if not os.path.exists("./storage/items_cache.yml"):
    with open('./storage/items_cache.yml', 'w', encoding='utf-8') as f:
        f.write('')



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

# gen fonder output
if os.path.isdir('./Output'):
    shutil.rmtree('./Output')
if not os.path.isdir('./Output'):
    os.mkdir('./Output') 
    os.mkdir('./Output/assets') 
    shutil.copyfile('./pack.mcmeta','./Output/pack.mcmeta')
    os.mkdir('./Output/assets/minecraft') 

    


itemadder = './ItemsAdder/contents'
item_m = {}
id = 10101


fix_id_10101=False

list_give_items = []
list_give_items_1_20_6 = []


alt_dat = []
json_fonts = {"providers": []}
txt_fonts = []
armor_layer_1_lists = []
armor_layer_2_lists = []
armor_layer_1_lists_colors = {}
armor_layer_2_lists_colors = {}

for get_namespace in os.listdir(itemadder):
    if os.path.exists(f"{itemadder}/{get_namespace}/resourcepack/assets/minecraft"):
        if os.path.exists("./Output/assets/minecraft"):
            shutil.rmtree("./Output/assets/minecraft")
        shutil.copytree(f"{itemadder}/{get_namespace}/resourcepack/assets/minecraft", f"./Output/assets/minecraft")
    for get_file in os.listdir(itemadder+"/"+get_namespace+"/configs"):


        with open(itemadder+"/"+get_namespace+"/configs"+"/"+get_file) as file:
            documents = yaml.full_load(file)
            namespace = documents['info']['namespace']

            if not os.path.exists('./Output/assets/'+documents['info']['namespace']):
                shutil.copytree(itemadder+'/'+get_namespace+"/resourcepack/assets/"+documents['info']['namespace'],'./Output/assets/'+documents['info']['namespace'])
            
            if 'font_images' in documents:
                for font_image in documents["font_images"]:
                    _unicode = font_image_unicode(namespace+":"+font_image)
                    json_fonts["providers"].append({
                        "file": namespace+":"+documents["font_images"][font_image]["path"],
                        "chars": [str(_unicode)],      
                        "height": documents["font_images"][font_image]["scale_ratio"],
                        "ascent": documents["font_images"][font_image]["y_position"],
                        "type": "bitmap"
                    })
                    txt_fonts.append(str(namespace+":"+font_image+": "+_unicode))

            if  'items' in documents: 
                
                for key in documents['items']:
                    
                    if documents['items'][key]['resource']['generate'] is False:

                        if fix_id_10101 == False:
                            id = item_get_cmdata(documents['items'][key]['resource']['material'],namespace+":"+key)

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
                            
                            if fix_id_10101 == False:
                                id = item_get_cmdata(documents['items'][key]['resource']['material'],namespace+":"+key)
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
                                    _met = documents['items'][key]['specific_properties']['armor']['slot'].lower()
                                    armor_list = {"head":"leather_helmet","chest":"leather_chestplate","legs":"leather_leggings","feet":"leather_boots"}
                                    data = {}
                                    if fix_id_10101 == False:
                                        id = item_get_cmdata(armor_list[_met],namespace+":"+key)
                                    texture_path = documents['items'][key]['resource']['textures'][-1] .replace(".png","")
                                    alt_dat.append( namespace+":"+texture_path)
                                    # print(documents['items'][key]['specific_properties']['armor']['slot'])
                                    
                                    
                                    
                                    icon_json = {"parent": "minecraft:item/generated","textures": {"layer0": "item/empty","layer1": namespace+":"+texture_path}}
                                    # wite json
                                    with open('./Output/assets/'+namespace+'/models/'+key+'.json', 'w') as jsonfile:
                                        json.dump(icon_json, jsonfile)



                                    if not os.path.exists("./Output/assets/minecraft/models/item"):
                                        os.makedirs("./Output/assets/minecraft/models/item")
                                    if not os.path.exists('./Output/assets/minecraft/models/item/'+armor_list[_met]+'.json'):
                                        for file in glob.glob("./default_model/**/"+armor_list[_met]+".json", recursive=True):
                                            with open(file, 'r') as f:
                                                data = json.load(f)
                                    else:
                                        with open('./Output/assets/minecraft/models/item/'+armor_list[_met]+'.json') as f:
                                            data = json.load(f)
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
                                        shutil.copytree("./default_model/textures/models/armor_overlay","./Output/assets/minecraft/textures/models/armor")
                                    
                                    
                                    if 'chest' ==_met:
                                        _layer_1 =documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['layer_1']
                                        _layer_2 =documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['layer_2']
                                        _color=documents['armors_rendering'][documents['items'][key]['specific_properties']['armor']['custom_armor']]['color']
                                        
                                        if not os.path.exists("./Output/tmp/armors"):
                                            os.makedirs("./Output/tmp/armors/layer_1")       
                                            os.makedirs("./Output/tmp/armors/layer_2")       
                                        if not os.path.exists("./Output/assets/minecraft/shaders"):
                                            shutil.copytree("./default_model/shaders", "./Output/assets/minecraft/shaders")


                                        # pain_armor("./Output/assets/"+namespace+"/textures/"+_layer_1+".png",_color)
                                        armor_layer_1_lists_colors[os.path.basename(_layer_1+".png")]  = _color
                                        armor_layer_1_lists.append("./Output/assets/"+namespace+"/textures/"+_layer_1+".png")
                                        # pain_armor("./Output/assets/"+namespace+"/textures/"+_layer_2+".png",_color)
                                        armor_layer_2_lists_colors[os.path.basename(_layer_2+".png")]  = _color
                                        armor_layer_2_lists.append("./Output/assets/"+namespace+"/textures/"+_layer_2+".png")

alt_dat = sorted(set(alt_dat))
alt_data = { "sources": [  ]}
if armor_layer_1_lists != []:
    add_img_armor(armor_layer_1_lists,"layer_1",armor_layer_1_lists_colors)
if armor_layer_2_lists != []:
    add_img_armor(armor_layer_2_lists,"layer_2",armor_layer_2_lists_colors)

for i in alt_dat:
    alt_data['sources'].append({ "type": "single", "resource": i })

# /Output/assets/minecraft/atlases/blocks.json check create path
if not os.path.exists("./Output/assets/minecraft"):
    os.mkdir('./Output/assets/minecraft')
if alt_data["sources"] != []:
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
                with open('./Output/assets/minecraft/models/item/'+k.lower()+'.json', 'w') as jsonfile:
                    json.dump(data, jsonfile)
for items in glob.glob("./Output/assets/minecraft/models/item/*.json"):
    with open(items, 'r') as f:
        data = json.load(f)
    _id_max = data['overrides'][-1]['predicate']['custom_model_data']+1
    data['overrides'].append({ "predicate": { "custom_model_data": _id_max }, "model": "item/"+os.path.basename(items).replace(".json","") })
    with open(items, 'w') as jsonfile:
        json.dump(data, jsonfile)

if os.path.exists("./Output/tmp"):
    shutil.rmtree("./Output/tmp")
# list_give_items to text
if list_give_items != []:
    with open('./Output/give_items.txt', 'w') as f:
        for i in list_give_items:
            f.write(i+'\n\n')
if list_give_items_1_20_6 != []:
    with open('./Output/give_items_1_20_6.txt', 'w') as f:
        for i in list_give_items_1_20_6:
            f.write(i+'\n\n')

if json_fonts["providers"] != []:
    if not os.path.exists("./Output/assets/minecraft/font"):
        os.makedirs("./Output/assets/minecraft/font")
    with open('./Output/assets/minecraft/font/default.json', 'w',encoding="utf-8") as f:
        json.dump(json_fonts, f,ensure_ascii=False)
    with open("./Output/font_unicode.txt","w",encoding="utf-8") as f:
        for i in txt_fonts:
            f.write(i+"\n")

if len(os.listdir("./Output/assets/minecraft")) == 0:
    shutil.rmtree("./Output/assets/minecraft")



# if os.path.exists("C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output"):
#     shutil.rmtree("C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output")
# shutil.copytree('./Output', 'C:/Users/kig/AppData/Roaming/PrismLauncher/instances/1.20.2(1)/.minecraft/resourcepacks/Output')    

print('Done!')