import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import gc
import time

#This library contains all the computer vision functionalities
import faces_recognizer  
#This file contains all the read/write fonctionalities
import file_handlers
import os

cap = cv2.VideoCapture(0)

APP_ICON_PATH = os.path.dirname(os.path.realpath(__file__)) + "/images/icon.ico"
APP_WIDTH = 920 #minimal width of the gui
APP_HEIGHT = 534 #minimal height of the gui
WIDTH  = int(cap.get(3)) #webcam's picture width
HEIGHT = int(cap.get(4)) #wabcam's picture height
#number of face-encodings to be created of each new face 
NUMBER_OF_FACES_ENCODINGS = 1 
NAME_ADDED = False
RECOGNIZE = False

#The faces are saved as pickle files, it's not actually
#a database, it's a "database"
def add_to_database(KNOWN_FACES, name):
	KNOWN_FACES[name] = faces_recognizer.KNOWN_FACES_ENCODINGS
	file_handlers.create_file(name)
	file_handlers.save_encodings(name)
	#updating the current known faces dict with the freshly 
	#added faces' encodings
	KNOWN_FACES = file_handlers.load_known_faces() 
	return KNOWN_FACES

def refresh_database(name):
	KNOWN_FACES = {}
	for _ in range(NUMBER_OF_FACES_ENCODINGS):
		_, frame = cap.read()
		if frame is not None:
			faces_recognizer.KNOWN_FACES_ENCODINGS, NUMBER_OF_FACES_IN_FRAME = faces_recognizer.create_face_encodings(frame)
			#If there's more than one face in the frame, then it is not a valid face encoding
			if len(faces_recognizer.KNOWN_FACES_ENCODINGS) and NUMBER_OF_FACES_IN_FRAME==1:
				KNOWN_FACES = add_to_database(KNOWN_FACES, name)
				#GUI animation stuff:
				name_entry.delete(0, 'end')
				name_entry.focus()
			else:
				#Showing a message to the user that there's no valid face to encode
				messagebox.showinfo(message='Either no face, or multiple faces has been detected!\nPlease try again when problem resolved.',
									title = "Invalid name")
				name_entry.delete(0, 'end')
				name_entry.focus()
	return KNOWN_FACES

def add_new_known_face():
	faces_recognizer.KNOWN_FACES = refresh_database(name = NEW_NAME.get().lower())
	faces_recognizer.KNOWN_FACES = file_handlers.load_known_faces()

def display_frames_per_second(frame, start_time):
	END_TIME = abs(start_time-time.time())
	TOP_LEFT = (0,0)
	BOTTOM_RIGHT = (116,26)
	TEXT_POSITION = (8,20)
	TEXT_SIZE = 0.6
	FONT = cv2.FONT_HERSHEY_SIMPLEX
	COLOR = (0,255,0) #BGR
	cv2.rectangle(frame, TOP_LEFT, BOTTOM_RIGHT, (0,0,0), cv2.FILLED)
	cv2.putText(frame, "FPS: {}".format(round(1/max(0.0333,END_TIME),1)), TEXT_POSITION, FONT, TEXT_SIZE,COLOR)
	return frame

#converting a fame object to an image object
def convert_to_image(frame):
	#the screen works with RGB, opencv encodes pictures in BGR
	#so to correctly display the images, color wise, we have
	#to convert them from BGR to RGB 
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	image = Image.fromarray(frame)
	return image

def recognize_faces (frame):
	frame = faces_recognizer.identify_faces(frame)
	return frame

######################################
#### Main function to update frame ###
######################################

def update_frame():
    START_TIME = time.time()
    global image, photo  # Define 'photo' here
    _, frame = cap.read()
    if frame is not None:
        frame = cv2.flip(frame, 1)
        if RECOGNIZE:
            frame = recognize_faces(frame)
        frame = display_frames_per_second(frame, START_TIME)
        image = convert_to_image(frame)
        photo = ImageTk.PhotoImage(image=image)  # Defining 'photo' here
        canvas.create_image(WIDTH, HEIGHT, image=photo, anchor="se")  # Updating canvas image
    root.after(round(10), update_frame)  # updating displayed image after: round(1000/FPS) [in milliseconds]

####################################
#### Buttons' callback functions ###
####################################

def name_authentification():
	global NAME_ADDED
	if NEW_NAME.get().lower() in faces_recognizer.KNOWN_FACES.keys() or not len(NEW_NAME.get()):
		messagebox.showinfo(message='Sorry! Either the name already exists or invalid!\t\nPlease try again.', title = "Error!!!")
		name_entry.delete(0, 'end')
		name_entry.focus()
		NAME_ADDED = False
	if NAME_ADDED:
		return True

def enter_name(*args):
	global NAME_ADDED
	NEW_NAME.get()
	NAME_ADDED = True
	#if the entered name is valid (non empty & non existant in the known faces dir), 
	#then adding to known faces dir
	if name_authentification(): 
		add_new_known_face()

def take_screenshot():
	try:
		IM = image
		SAVE_PATH = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")))
		IM.save(SAVE_PATH)
	except:
		pass

def enable_recognition():
	global RECOGNIZE
	if RECOGNIZE:
		RECOGNIZE = False
		recognition_button["bg"] = "black"
		recognition_button["text"] = "Start Face Recognization"
	else:
		RECOGNIZE = True
		recognition_button["bg"] = "red"
		recognition_button["text"] = "Stop Face Recognization"

# loading all the known faces in the database to the KNOWN_FACES dict
faces_recognizer.KNOWN_FACES = file_handlers.load_known_faces()

# start of GUI
root = tk.Tk()

# general characteristics of the GUI

root.wm_iconbitmap(APP_ICON_PATH)
root.title("Face Recognizer")
root.minsize(APP_WIDTH, APP_HEIGHT)
root["bg"]="#000000"

####################
### GUI elements ###
####################

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.place(relx=0.03, rely=0.052)

recognition_button = tk.Button(canvas, text = "Start Face Recognization", command = enable_recognition,
							   bg = "black", fg = "white", activebackground = 'white')
recognition_button.place(relx=0.74, rely=0.93, relwidth=0.24, relheight=0.06)
recognition_button.bind(enable_recognition)
recognition_button.focus()

MESSAGE = tk.StringVar()
MESSAGE.set("Enter name and press register \nface button to register face")
message_label=tk.Label(root,textvariable=MESSAGE, bg="white", fg="red")
message_label.place(relx=0.97,rely=0.080,relwidth=0.2,relheight=0.1,anchor="ne")
message_label.config(font=(None, 8))

NEW_NAME = tk.StringVar()
name_entry = ttk.Entry(root, text="Your Name", textvariable=NEW_NAME, foreground="black")
name_entry.place(relx=0.97, rely=0.19,relheight=0.05,relwidth = 0.2, anchor = "ne")
name_entry.bind('<Return>', enter_name)

name_button = ttk.Button(root, text="Register Face",command=enter_name)
name_button.place(relx=0.97,rely=0.26,relheight=0.05,relwidth=0.2,anchor="ne")
name_button.bind(enter_name)

screenshot_button = ttk.Button(root,text="Take a screenshot",command=take_screenshot)
screenshot_button.place(relx=0.97,rely=0.895,relheight=0.05,relwidth=0.2,anchor="ne")
screenshot_button.bind(take_screenshot)

#####################
### Initial frame ###
#####################

_, frame = cap.read()
if frame is not None:
	image = convert_to_image(frame)
	photo = ImageTk.PhotoImage(image=image)
	canvas.create_image(WIDTH, HEIGHT, image=photo, anchor="se")

##################################
### Executeing the main method ###
##################################

if __name__ == '__main__':
	update_frame()

#creating the GUI.
root.mainloop()

#free memory
cap.release()
gc.collect()