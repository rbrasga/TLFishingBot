#####################for the bot to work perfectly, you must put the exact directory of "imgs", for example, "C:/desktop/bot/imgs/Start.png"


from ast import If
import cv2
import pyautogui
import time
import random
import mss
import numpy as np
from PIL import Image
import gc
pyautogui.FAILSAFE = False
pyautogui.PAUSE=0.01 #Im using this to make loop faster

# Push F Cast Float
# Push Q Snap up with
# Push A or D depending on:
# - Continue pushing same button if fish bar is moving.
# - Push the opposite button if fish bar is not moving.

SCREENSHOT_CATCH = False

class FishBot:

	#TLWINDOW="TL 1.138.22.570"
	def __init__(self):
		# Selecting the "Q Snap up with"
		self.snapRegion = {"mon": 1, "top": (900), "left": (1225), "width": (32), "height": (32)}

		 # Selecting the "F Cast float"
		self.castRegion = {"mon": 1, "top": (841), "left": (1524), "width": (25), "height": (25)}

		 # Selecting the "F Cast float"
		self.recoverRegion = {"mon": 1, "top": (805), "left": (1525), "width": (24), "height": (24)}

		 # Selecting the "Capture Bar"
		self.fishRegion = {"mon": 1, "top": (782), "left": (1450), "width": (13), "height": (143)}

		 # Selecting the "Fishing Pole Stamina Bar"
		self.staminaRegion = {"mon": 1, "top": (784), "left": (1475), "width": (8), "height": (138)}

		# Starting screenshotting object
		self.sct = mss.mss()

	def screenGrab(self, region):
		IMG = None
		while IMG == None:
			try:
				IMG = self.sct.grab(region)
			except Exception as e:
				print(e)
				print(f"[Error] Unable to take screenshot. {region}")
				time.sleep(0.1)
		return IMG

	def getFishBar(self):
		#RGB 255,255,224 (+-10)
		# X Range: 782-924
		# Along Y Axis 1455

		# (left, top, width, height)
		fishbarImg = self.screenGrab(self.fishRegion)
		fishbarImg = np.array(fishbarImg)
		foundFish = None
		try:
			foundFish = pyautogui.locate("imgs/fishbar3.png", fishbarImg, grayscale=True, confidence=.5)
		except Exception as ImageNotFoundException:
			print("foundFish failed")
		if foundFish == None: return None
		_, top, _, _ = foundFish
		return top
	
	def needStamina(self):
		staminaImg = self.screenGrab(self.staminaRegion)
		staminaImg = np.array(staminaImg)
		foundStam = None
		try:
			foundStam = pyautogui.locate("imgs/stamina.png", staminaImg, grayscale=True, confidence=.7)
		except Exception as ImageNotFoundException:
			print("foundStam failed")
		return foundStam == None
	
	def main(self):


		# Select Application Window
		throneWindows = pyautogui.getWindowsWithTitle("TL 1")
		throneWindow = None
		for window in throneWindows:
			if "TL 1" in window.title:
				throneWindow = window
				break
		cv2.namedWindow("visuals", cv2.WINDOW_NORMAL)
		throneWindow.activate()
		
		q_count = 0
		wasCast = False
		CASTED = time.time()
		while True:
			# Sleep for 0.1 - 0.2s
			animationSleepTime = .1 + (.1 * random.random())
			if wasCast and time.time() - CASTED > 60:
				wasCast = False
				
			# Screenshot
			snapImg = self.screenGrab(self.snapRegion)
			snapImg = np.array(snapImg)

			castImg = self.screenGrab(self.castRegion)
			castImg = np.array(castImg)

			# Looking for the Q
			foundQ = None
			try:
				foundQ = pyautogui.locate("imgs/Q.png", snapImg, grayscale=True, confidence=.7)
			except Exception as ImageNotFoundException:
				print("foundQ failed")
			if foundQ:
				# Pressing Q
				pyautogui.keyDown('q')
				pyautogui.keyUp('q')
				q_count += 1
				print(f"Pressing Q (Snap up with) {q_count}")
				ActiveKey = "d"
				pyautogui.keyDown(ActiveKey)
				
				# Progress Tracker
				track_progress = []
				# Continue down this chain until the fish is caught
				#don't break out of fishing loop until at least 30 seconds after "caught"
				START = time.time()
				while True:
					# Fishing attempt failed
					if time.time() - START > 5:
						recoverImg = self.screenGrab(self.recoverRegion)
						recoverImg = np.array(recoverImg)
						foundF = None
						try:
							foundF = pyautogui.locate("imgs/F2.png", recoverImg, grayscale=True, confidence=.7)
						except Exception as ImageNotFoundException:
							print("foundF failed")
						if foundF == None:
							# Screenshot
							if SCREENSHOT_CATCH:
								monitor = self.sct.monitors[1]
								catchImg = self.sct.grab(monitor)
								mss.tools.to_png(catchImg.rgb, catchImg.size, output=f"fish_caught_{q_count}.png")
							print("Reeling in completed...")
							break
					top = self.getFishBar()
					if top == None: continue
					# Measure progress until progress since last check is 0.
					if len(track_progress) == 0:
						#Add the current offset
						track_progress.append(top)
						continue
					track_progress.append(top)
					progress = track_progress[-1] - track_progress [-2]
					if progress <= 0:
						track_progress = []
						pyautogui.keyUp(ActiveKey)
						if ActiveKey == "d":
							ActiveKey = "a"
						else:
							ActiveKey = "d"
						pyautogui.keyDown(ActiveKey)
					
					# Let stamina recover if it is low
					if self.needStamina():
						pyautogui.keyUp(ActiveKey)
						time.sleep(.3 + animationSleepTime)
						pyautogui.keyDown(ActiveKey)
					time.sleep(animationSleepTime)
					#pyautogui.keyUp(ActiveKey)
					
				pyautogui.keyUp(ActiveKey)
				time.sleep(5)
				wasCast = False
				continue

			foundF = None
			try:
				foundF = pyautogui.locate("imgs/F.png", castImg, grayscale=True, confidence=.7)
			except Exception as ImageNotFoundException:
				print("foundF failed")
			# Looking for the F
			if not wasCast and foundF:
				pyautogui.keyDown('f')
				pyautogui.keyUp('f')
				print("F Cast float")
				time.sleep(2 + animationSleepTime)
				wasCast = True
				CASTED = time.time()
				
			time.sleep(0.125)
			
# Runs the main function
if __name__ == '__main__':
	f = FishBot()
	f.main()
	"""
	# Select Application Window
	throneWindows = pyautogui.getWindowsWithTitle("TL 1")
	throneWindow = None
	for window in throneWindows:
		if "TL 1" in window.title:
			throneWindow = window
			break
	cv2.namedWindow("visuals", cv2.WINDOW_NORMAL)
	throneWindow.activate()
	time.sleep(2)
	self.sct = mss.mss()
	monitor = self.sct.monitors[1]
	#castImg = self.sct.grab(monitor)
	castImg = self.sct.grab(self.castRegion)
	castImg = np.array(castImg)
	#mss.tools.to_png(castImg.rgb, castImg.size, output="fishing_image_test.png")
	try:
		foundF = pyautogui.locate("imgs/F.png", castImg, grayscale=True, confidence=.7)
		print(f"foundF success. {foundF}")
		_,top,_,_=foundF
		print(f"TOP!!! {top}")
	except Exception as ImageNotFoundException:
		print("foundF failed")
	"""
	
