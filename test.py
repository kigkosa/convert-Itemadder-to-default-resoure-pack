from PIL import Image

image1 = Image.open('./default_model/textures/models/armor/leather_layer_1.png')
image2 = Image.open('./Output/tmp/armors/littleduck_armor_layer_1.png')

width1, height1 = image1.size
width2, height2 = image2.size
max_height = max(height1, height2)

total_width = width1 + width2 

combined_image = Image.new('RGBA', (total_width, max_height))
combined_image.paste(image1, (0, 0))
combined_image.paste(image2, (width1, 0))
combined_image.save('./Output/tmp/armors/leather_layer_1.png')