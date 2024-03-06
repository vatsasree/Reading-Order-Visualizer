from utils import *
from flask import Flask, render_template, url_for, request
import os
import json
import cv2
import pandas as pd
import numpy as np

app = Flask(__name__)

# Specify the path to the folder containing your images
IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/Pagg/Dataset/Dataset'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

# Load the JSON data
with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/dicc1_19042024.json', 'r') as json_file:
    image_data = json.load(json_file)

# Get the list of image files in the folder
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif','.tif'))]
#sort image files
image_files.sort()
total_images = len(image_files)
print("Image files:",image_files)

def load_image(image_path):
    return cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image_path))


@app.route('/')
def index():
    # get query parameters
    image_index = request.args.get('image_index', default=0, type=int)
    return show_image(image_index)

@app.route('/image/<int:image_index>')
def show_image(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        # image_path = 'images/subsubset/' + current_image
        image_path = 'images/Pagg/Dataset/Dataset/' + current_image
        return render_template('index.html', image_path=image_path, current_image=current_image, image_files=image_files)
    else:
        return "Invalid image index"

@app.route('/next/<int:image_index>')
def next_image(image_index):
    next_index = (image_index + 1) % total_images
    return show_image(next_index)

@app.route('/prev/<int:image_index>')
def prev_image(image_index):
    prev_index = (image_index - 1) % total_images
    return show_image(prev_index)

# Route to display image with connections
@app.route('/conn_image/<int:image_index>')
def conn_image(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        image = load_image(image_path)

        euclidean_data = image_data.get(current_image_sp, {}).get('connections', {}).get('euclidean')
        euclidean_df = pd.DataFrame(euclidean_data)
        
        image_with_connections = conn(image, euclidean_df)
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_conn_image.jpg')
        cv2.imwrite(temp_output_path, image_with_connections)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])

        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_conn_image.jpg', image_files=image_files)

    else:
    
        return "Invalid image index"


@app.route('/para_image/<int:image_index>')
def para_image(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)

        euclidean_data = image_data.get(current_image_sp, {}).get('paragraph', {}).get('euclidean')
        euclidean_df = pd.DataFrame(euclidean_data)
        
        component_data = image_data.get(current_image_sp, {}).get('paragraph', {}).get('component')
        component_df = pd.DataFrame(component_data)
        
        target_components = image_data.get(current_image_sp,{}).get('paragraph',{}).get('target_components')
        
        image_with_para = para(image, target_components,euclidean_df, component_df)

        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_para_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_para_image.jpg', image_files=image_files)

    else:
    
        return "Invalid image index"
    

@app.route('/final_order/<int:image_index>')
def final_order(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)

        euclidean_data = image_data.get(current_image_sp, {}).get('reading_order', {}).get('new_euclidean')
        euclidean_df = pd.DataFrame(euclidean_data)
        
        header_p = 10
        footer_p = 10
        image_with_para,_ = reading_order_with_line(image,euclidean_df, header_p, footer_p)

        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_final_order_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_final_order_image.jpg', image_files=image_files)

    else:
    
        return "Invalid image index"


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

