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
# IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/selected'
# IMAGE_FOLDER = "/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/Pagg/Prima"
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

# Load the JSON data
# with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/jsons/dataset/dic_dataset_new2.json', 'r') as json_file:
#     image_data = json.load(json_file)

# with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/jsons/dataset/dic_dataset_new2_2.json', 'r') as json_file_2:
#     image_data_2 = json.load(json_file_2)

# with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/jsons/dataset/dic_dataset_new2_3.json', 'r') as json_file_3:
#     image_data_3 = json.load(json_file_3)

# with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/jsons/dataset/dic_dataset_new2_4.json', 'r') as json_file_4:
#     image_data_4 = json.load(json_file_4)

with open('/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/dic_dataset1_chebyshev.json' , 'r') as json_file_5:
    image_data_5 = json.load(json_file_5)

# image_data.update(image_data_2)
# image_data.update(image_data_3)
# image_data.update(image_data_4)

image_data = image_data_5

print("Length of image data after merging:",len(image_data))

# Get the list of image files in the folder
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif','.tif'))]
image_files_json = image_data.keys()

#add png extension to image_files_json
image_files_json = [f+'.jpg' for f in image_files_json]
print("Image files json:",len(image_files_json))

#find common images between image_files and image_files_json
common_images = list(set(image_files).intersection(set(image_files_json)))
print("Common images:",len(list(common_images)))

#sort image files
# image_files.sort()
#sort strings based on numeric values
common_images.sort(key=lambda x: int(x.split('.')[0]))
image_files = common_images

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
        # image_path = 'images/selected/' + current_image
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
    
        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


@app.route('/para_image_1/<int:image_index>')
def para_image_1(image_index):
    
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)

        # euclidean_data = image_data.get(current_image_sp, {}).get('paragraph', {}).get('euclidean')
        # euclidean_df = pd.DataFrame(euclidean_data)
        
        component_data = image_data.get(current_image_sp, {}).get('paragraph_before_pinp', {}).get('component')
        component_df = pd.DataFrame(component_data)
        print("CD:",component_df)
        # target_components = image_data.get(current_image_sp,{}).get('paragraph',{}).get('target_components')
        
        image_with_para = para_2(image, component_df)
        print("Image with para:",image_with_para)
        if image_with_para is None:
            return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Reading Order for this image currently not available. Please try another image.")
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_para_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_para_image.jpg', image_files=image_files, error_message=None)

    else:
    
        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")
    
@app.route('/para_image_2/<int:image_index>')
def para_image_2(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)


        component_data = image_data.get(current_image_sp, {}).get('paragraph_after_pinp_not_ordered', {}).get('component')
        component_df = pd.DataFrame(component_data)
        
        image_with_para = para_2(image, component_df)
        if image_with_para is None:
            return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Reading Order for this image currently not available. Please try another image.")

        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_para_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_para_image.jpg', image_files=image_files)

    else:
    
        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")
    

@app.route('/para_image_3/<int:image_index>')
def para_image_3(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)

        component_data = image_data.get(current_image_sp, {}).get('paragraph_after_pinp_ordered', {}).get('component')
        component_df = pd.DataFrame(component_data)
        
        image_with_para = para_2(image, component_df)
        if image_with_para is None:
            return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Reading Order for this image currently not available. Please try another image.")

        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_para_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_para_image.jpg', image_files=image_files)

    else:
    
        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")
    

@app.route('/final_order/<int:image_index>')
def final_order(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_sp = image_files[image_index].split('.')[0]
        print("CI:",current_image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        
        image = load_image(image_path)

        component_df = pd.DataFrame(image_data.get(current_image_sp, {}).get('reading_order', {}).get('new'))
        euclidean_df_2 = pd.DataFrame(image_data.get(current_image_sp, {}).get('reading_order', {}).get('euclidean'))

        # euclidean_data = image_data.get(current_image_sp, {}).get('reading_order', {}).get('new_euclidean')
        # euclidean_df = pd.DataFrame(euclidean_data)
        
        header_p = 10
        footer_p = 10
        # image_with_para,_ = reading_order_with_line(image,euclidean_df, header_p, footer_p)
        image_with_para = get_coordinates_from_component(component_df, euclidean_df_2,image)

        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_final_order_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_final_order_image.jpg', image_files=image_files)

    else:
    
        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)

