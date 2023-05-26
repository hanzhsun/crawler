# -*- encoding=utf8 -*-
__author__ = "chichikin"

from airtest.core.api import *
import logging
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
from poco.drivers.ios import iosPoco
poco = iosPoco()

width, height = device().get_current_resolution()
start_pt = (width, 0.9*height)
end_pt = (width, 0.24*height)

end_pt1 = (width, 0)

end_pt2 = (width, 0.46*height)

def swipe_std():
    swipe(start_pt, end_pt)

def swipe_fast():
    swipe(start_pt, end_pt1)
    
def swipe_video():
    swipe(start_pt, end_pt2)
    
def reply():
    while True:
        pos = exists(Template(r"tpl1647488792912.png",threshold=0.8, record_pos=(-0.359, -0.221), resolution=(1536, 2048)))
        #pos1 = exists(Template(r"tpl1647488831540.png", record_pos=(-0.283, -0.221), resolution=(1536, 2048)))
        if pos:
            #print(pos)
            #print(pos1)
            touch(pos)
            sleep(1) 
        else: 
            break           
        
pic = "../pic/"
i = 0
j = 0

#while True:
while i<1:

    #reply()
    
    with poco.freeze() as fpoco:
        if fpoco("作者").exists() or fpoco("作者赞过").exists() or fpoco("你的关注").exists():
            snapshot(filename=pic+str(i)+".jpg")
            i = i+1
        if fpoco("- THE END -").exists():
            break
        
    #swipe_std()
    
    #swipe_fast()
    
    swipe_video()
    
    j = j+1
    if j == 100:
        sleep(20)
