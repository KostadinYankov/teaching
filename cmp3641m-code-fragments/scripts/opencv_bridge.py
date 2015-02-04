#!/usr/bin/env python
import sys
import rospy
import cv2
import numpy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:

  def __init__(self):

    cv2.namedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/video",Image,self.callback)
    #self.image_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.callback)
  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e
    gimg = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(cv_image, numpy.array((200, 230, 230)), numpy.array((255, 255, 255)))
    contours0, hierarchy = cv2.findContours( thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours0:
        a = cv2.contourArea(c)
        if a > 100.0:
            m = cv2.moments(c,True)
            print m
            cv2.drawContours(cv_image, c, -1, (255,0,0))
    print '===='    
    #print contours0
    #cv2.drawContours(cv_image, contours0, -1, (255,0,0))
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    #rospy.spin()
    while not rospy.is_shutdown():
        cv2.waitKey(3)
  except KeyboardInterrupt:
    print "Shutting down"
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)