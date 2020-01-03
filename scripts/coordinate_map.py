# This script is to generate a coordinate map with overlayed text for OSRS world map
# The centre location of the world map is located at the observeratory (Point 3889, 2827)
# 1 square tile in game is 1.875 minutes
# 1 square tile is equivalent to a 3x3 pixel on the osrs world map
# 1 degree = 60 minutes = 32 squares ( 8 squares = 15 minutes )

# World map resolution 8306 x 4850 (BASED ON "osrs_world_map_july18_2019.PNG")
# Extra 1 pixel border around the whole map

# From the centre the first interval of 5 degrees starts at x = 49, y = 427
# Longitude =  40.5 degrees west - 46 degrees east
# Latitude = 29.4 degrees north - 21.06 degrees south
from PIL import Image, ImageDraw, ImageFont
import sys

im = Image.open("../resources/osrs_world_map_july18_2019.PNG")
fnt = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 80)

#-3840 start of 40 degrees west
im.putpixel((3889,2827),(255,0,153))

# Draw coordinate lines every 5 degrees (5 degrees = 480 pixels)
draw = ImageDraw.Draw(im)
for x in range(49,8306,480):
    draw.line([(x,0), (x,4850)], (255,0,153), 5)

    if (x < 3889):
        label = str(int((3889 - x) / 480) * 5) + "W"
    elif (x > 3889):
        label = str(int((x - 3889 ) / 480) * 5) + "E"
    else:
        label = "0"
    draw.text((x-20,41),label, font=fnt, fill=(255,255,255,255))
    draw.text((x-20,4759),label, font=fnt, fill=(255,255,255,255))

for y in range(427,4850,480):
    draw.line([(5,y), (8306,y)], (255,0,153), 5)

    if (y < 2827):
        label = str(int((2827 - y) / 480) * 5) + "N"
    elif (y > 2827):
        label = str(int((y - 2827 ) / 480) * 5) + "S"
    else:
        label = "0"

    draw.text((51,y-40),label, font=fnt, fill=(255,255,255,255))
    draw.text((8115,y-40),label, font=fnt, fill=(255,255,255,255))

im.save("osrs_coordinate_map.png", "PNG")

