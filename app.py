


from flask import Flask, render_template, url_for, request
import os
import json
import cv2
import pandas as pd
import numpy as np

app = Flask(__name__)

# Specify the path to the folder containing your images
IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/static/images/'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

# Load the JSON data
with open('/home/vatsasree/Research/scripts/applic/dictt.json', 'r') as json_file:
    image_data = json.load(json_file)

# Get the list of image files in the folder
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
total_images = len(image_files)
print("Image files:",image_files)

def load_image(image_path):
    return cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], image_path))


def conn(image, euclidean):

    #image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    image_with_boxes = image.copy()

    for index, row in euclidean.iterrows():
        left = int(row['Left'][0])
        right = int(row['Right'][0])
        top = int(row['Top'][1])
        bottom = int(row['Bottom'][1])
        box_id = int(row['Id'])

        width = right - left
        height = bottom - top

        top_left = (left, top)
        bottom_right = (right, bottom)

        cv2.rectangle(image_with_boxes, top_left, bottom_right, (255, 0, 0), 2)

        label_position = (left, top - 10)
        cv2.putText(image_with_boxes, str(box_id), label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        top_adjacent_id = int(row['Top_Box'][1])
        bottom_adjacent_id = int(row['Bottom_Box'][1])
        left_adjacent_id = int(row['Left_Box'][1])
        right_adjacent_id = int(row['Right_Box'][1])

        if top_adjacent_id != 0:
            top_adjacent_row = euclidean[euclidean['Id'] == top_adjacent_id].iloc[0]
            top_adjacent_center = int(top_adjacent_row['Bottom'][0]) , int(top_adjacent_row['Bottom'][1])
            cv2.line(image_with_boxes, (int(left) + width // 2, int(top)), top_adjacent_center, (0, 255, 0), 2)

        if bottom_adjacent_id != 0:
            bottom_adjacent_row = euclidean[euclidean['Id'] == bottom_adjacent_id].iloc[0]
            bottom_adjacent_center = int(bottom_adjacent_row['Top'][0]) , int(bottom_adjacent_row['Top'][1])
            cv2.line(image_with_boxes, (int(left) + width // 2, int(bottom)), (int(bottom_adjacent_center[0]), int(bottom_adjacent_center[1])), (0, 255, 0), 2)

        if left_adjacent_id != 0:
            left_adjacent_row = euclidean[euclidean['Id'] == left_adjacent_id].iloc[0]
            left_adjacent_center = int(left_adjacent_row['Right'][0]) , int(left_adjacent_row['Right'][1])
            cv2.line(image_with_boxes, (int(left), int(top) + height // 2), (int(left_adjacent_center[0]), int(left_adjacent_center[1])), (0, 255, 0), 2)

        if right_adjacent_id != 0:
            right_adjacent_row = euclidean[euclidean['Id'] == right_adjacent_id].iloc[0]
            right_adjacent_center = int(right_adjacent_row['Left'][0]) , int(right_adjacent_row['Left'][1])
            cv2.line(image_with_boxes, (int(right), int(top) + height // 2), (int(right_adjacent_center[0]), int(right_adjacent_center[1])), (0, 255, 0), 2)

    return image_with_boxes


def para(image, target_components, euclidean,component):

    count = 0
    image_with_boxes = image.copy()
    # print(type(component))
    for idx1,rowcomp in component.iterrows():
        left1 = []
        right1 = []
        top1 = []
        bottom1 = []
        for index, row in euclidean.iterrows():
            box_id = int(row['Id'])
            # print(type(box_id))
            # print(type(rowcomp['Component'][0][0]))
            if box_id in rowcomp['Component'][0]:
                order = rowcomp['Order']
                right_box1 = row['Right']
                left_box1 = row['Left']
                top_box1 = row['Top']
                bottom_box1 = row['Bottom']
                right_box = right_box1[0]
                left_box = left_box1[0]
                top_box = top_box1[1]
                bottom_box = bottom_box1[1]
                # print(right_box,left_box,top_box,bottom_box)
                # right_box = parse_string(right_box1,"[",",")
                # left_box = parse_string(left_box1,"[",",")
                # top_box = parse_string(top_box1,",","]")
                # bottom_box = parse_string(bottom_box1,",","]")
                if(int(round(float(left_box)))!=-1):
                    left1.append(int(round(float(left_box))))
                if(int(round(float(right_box)))!=-1):
                    right1.append(int(round(float(right_box))))
                if(int(round(float(top_box)))!=-1):
                    top1.append(int(round(float(top_box))))
                if(int(round(float(bottom_box)))!=-1):
                    bottom1.append(int(round(float(bottom_box))))
            # print(left1,right1,top1,bottom1)  
        l = min(left1)
        r = max(right1)
        t = min(top1)
        b = max(bottom1)
        center_top = [int(l+r)/2, int(t)]
        center_bottom = [int(l+r)/2, int(b)]
        center_right = [int(r), int(t+b)/2]
        center_left = [int(l), int(t+b)/2]
        larger_box_top_left = (int(l - 20), int(t - 20))
        larger_box_bottom_right = (int(r + 10), int(b + 10))

        cv2.rectangle(image_with_boxes, larger_box_top_left, larger_box_bottom_right, (0, 0, 255), 2)
        # cv2.putText(image_with_boxes, str(component['Order'][count]), (int(l - 20), int(t - 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.putText(image_with_boxes, str(order), (int(l - 20), int(t - 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        count = count + 1

    #cv2.imwrite(output_path, cv2.cvtColor(image_with_boxes, cv2.COLOR_RGB2BGR))
    return image_with_boxes


@app.route('/')
def index():
    # get query parameters
    image_index = request.args.get('image_index', default=0, type=int)
    return show_image(image_index)

@app.route('/image/<int:image_index>')
def show_image(image_index):
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        image_path = 'images/' + current_image
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

        # Assuming `euclidean` is available for the current image from your data
        # Replace this with the actual data retrieval logic for 'euclidean'
        # You might want to adapt this depending on your data structure

        euclidean_data = image_data.get(current_image_sp, {}).get('connections', {}).get('euclidean')
        
        euclidean_df = pd.DataFrame(euclidean_data)
        
        # Call the conn function to generate an image with connections
        
        image_with_connections = conn(image, euclidean_df)
        # Specify the folder for saving the output images
        output_folder = '/home/vatsasree/Research/scripts/applic/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the result in the output folder
        temp_output_path = os.path.join(output_folder, 'output_conn_image.jpg')
        cv2.imwrite(temp_output_path, image_with_connections)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])

        
        # Render the template with the image path
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

        # Assuming `euclidean` is available for the current image from your data
        # Replace this with the actual data retrieval logic for 'euclidean'
        # You might want to adapt this depending on your data structure

        euclidean_data = image_data.get(current_image_sp, {}).get('paragraph', {}).get('euclidean')
        euclidean_df = pd.DataFrame(euclidean_data)
        
        component_data = image_data.get(current_image_sp, {}).get('paragraph', {}).get('component')
        component_df = pd.DataFrame(component_data)
        
        target_components = image_data.get(current_image_sp,{}).get('paragraph',{}).get('target_components')
        # Call the conn function to generate an image with connections
        
        image_with_para = para(image, target_components,euclidean_df, component_df)

        ## Specify the folder for saving the output images
        output_folder = '/home/vatsasree/Research/scripts/applic/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        # Save the result in the output folder
        temp_output_path = os.path.join(output_folder, 'output_para_image.jpg')
        cv2.imwrite(temp_output_path, image_with_para)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        
        
        # Render the template with the image path
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index.html', current_image=current_image, image_path='/images/output_images/output_para_image.jpg', image_files=image_files)

    else:
    
        return "Invalid image index"

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

