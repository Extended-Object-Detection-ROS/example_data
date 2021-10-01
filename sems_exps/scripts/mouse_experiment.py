#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import rospy
from extended_object_detection.msg import SimpleObjectArray

from cv_bridge import CvBridge
import cv2
from sensor_msgs.msg import Image

class MouseExperiment(object):
    def __init__(self):
        rospy.init_node('mouse_experiment')
        
        self.compare_objects = rospy.get_param('~compare_objects', ['MouseDnnOnly', 'MouseSoftTrack'])
        
        self.cnt_object = rospy.get_param('~cnt_object', 'Colors')
        
        self.stop_frames = rospy.get_param('~stop_frames', [10, 38, 70])
        
        self.save_path = rospy.get_param('~save_path', '/tmp')        
        self.scores = [[], []]
        self.cnt = []
        
        
        
        rospy.Subscriber('simple_objects', SimpleObjectArray, self.so_cb)
        
        if len(self.stop_frames):
            rospy.Subscriber('detected_image', Image, self.im_cb)
            self.cv_bridge = CvBridge()
            self.cntr = 0
            
    def im_cb(self, msg):
        if self.cntr in self.stop_frames:
            rgb_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            cv2.imwrite(self.save_path+f"/stop_frame_{self.cntr}.jpg", rgb_image)
        
        self.cntr+=1
        
    def so_cb(self, msg):
        for id, obj_name in enumerate(self.compare_objects):            
            flag = False
            for obj in msg.objects:            
                if obj.type_name == obj_name:
                    self.scores[id].append(obj.score)
                    flag = True
                    break
            if not flag:
                self.scores[id].append(0)
        cnt = 0;
        for obj in msg.objects:
            if self.cnt_object == obj.type_name:
                cnt+=1
        self.cnt.append(cnt)
        
                                        
    def run(self):
        while not rospy.is_shutdown():
            plt.cla()
            plt.plot(self.scores[0], label = "{} avg {:.2f}".format(self.compare_objects[0], np.mean(self.scores[0])))
            plt.plot(self.scores[1], label = "{} avg {:.2f}".format(self.compare_objects[1], np.mean(self.scores[1])))
            #plt.plot(np.array(self.cnt)/max(self.cnt), label="color objects number")
            plt.grid()
            plt.title("Degree of confidence")
            plt.legend()            
            plt.pause(0.1)
            
        plt.savefig(self.save_path+"/scores.jpg")
        print(f"Saved image to {self.save_path+'/scores.jpg'}")

if __name__ == '__main__':        
    me = MouseExperiment()
    me.run()
