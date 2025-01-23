from utils import *
from flask import Flask, render_template, url_for, request
import os
import json
import cv2
import pandas as pd
import numpy as np

app = Flask(__name__)

# Specify the path to the folder containing your images

IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/final_images_combined_extended'
# IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/extended_dataset'
# IMAGE_FOLDER = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/M6doc_mz'
# IMAGE_FOLDER = "/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/subset"
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


image_files = [i.split('.')[0] for i in os.listdir(IMAGE_FOLDER)]
image_files_full = os.listdir(IMAGE_FOLDER)

# CSV_PATH = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/csv/final_set_categories_combined'
# csv_files = [i.split('.')[0] for i in os.listdir(CSV_PATH)]
# csv_files_full = os.listdir(CSV_PATH)

image_files.sort()
image_files_full.sort()

# csv_files.sort()
# csv_files_full.sort()


# common_images = list(set(image_files).intersection(csv_files))
# print('len(common_images):',len(common_images))

# common_images.sort()
# image_files = common_images

total_images = len(image_files)
# print("Image files:",image_files_full)

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
        print("Current image full:",current_image)
        global image_path

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        
        # Check for image file with the correct extension
        for ext in possible_extensions:
            # image_path = f'images/subset/{current_image}{ext}'
            # if os.path.exists(os.path.join(IMAGE_FOLDER.split('images/subset')[0],image_path)):
            image_path = f'images/final_images_combined_extended/{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER.split('images/final_images_combined_extended')[0],image_path)):
            # image_path = f'images/extended_dataset/{current_image}{ext}'
            # if os.path.exists(os.path.join(IMAGE_FOLDER.split('images/extended_dataset')[0],image_path)):
            # image_path = f'images/M6doc_mz/{current_image}{ext}'
            # if os.path.exists(os.path.join(IMAGE_FOLDER.split('images/M6doc_mz')[0],image_path)):
                break
        else:
            return "Image file not found."
        return render_template('index_hisam_new.html', image_path=image_path, current_image=current_image, image_files=image_files)
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

@app.route('/display_layout/<int:image_index>>')
def show_image_layout(image_index):
    json_path = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/lines_paras_jsons/reading_order_results_1191.json'

    import pandas as pd
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_csv = image_files[image_index]

        print("current image:",current_image)

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in possible_extensions:
            current_image_full = f'{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER, current_image_full)):
                break

        print("current image full:",current_image_full)

        img_path = os.path.join(IMAGE_FOLDER, current_image_full)
        print('img_path',img_path)
        
        import json
        f = json.load(open(json_path, 'r'))

        img_with_layout = display_hisam_newapproach_layout(img_path, f[current_image])
        
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_img_with_gts.jpg')
        print("Temp output path:",temp_output_path)
        cv2.imwrite(temp_output_path, img_with_layout)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        print("Relative path:",relative_path)
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index_hisam_new.html', current_image=current_image.split('.')[0], image_path='/images/output_images/output_img_with_gts.jpg', image_files=image_files)

    else:

        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index_hisam_new.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


@app.route('/display_fparas/<int:image_index>>')
def show_image_fparas(image_index):
    json_path = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/lines_paras_jsons/reading_order_results_1191.json'

    import pandas as pd
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_csv = image_files[image_index]

        print("current image:",current_image)

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in possible_extensions:
            current_image_full = f'{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER, current_image_full)):
                break

        print("current image full:",current_image_full)

        img_path = os.path.join(IMAGE_FOLDER, current_image_full)
        print('img_path',img_path)
        
        import json
        f = json.load(open(json_path, 'r'))

        img_with_layout = display_hisam_newapproach_fparas(img_path, f[current_image])
        
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_img_with_gts.jpg')
        print("Temp output path:",temp_output_path)
        cv2.imwrite(temp_output_path, img_with_layout)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        print("Relative path:",relative_path)
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index_hisam_new.html', current_image=current_image.split('.')[0], image_path='/images/output_images/output_img_with_gts.jpg', image_files=image_files)

    else:

        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index_hisam_new.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


@app.route('/display_sparas/<int:image_index>>')
def show_image_sorted_paras(image_index):
    json_path = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/lines_paras_jsons/reading_order_results_1191.json'

    import pandas as pd
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_csv = image_files[image_index]

        print("current image:",current_image)

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in possible_extensions:
            current_image_full = f'{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER, current_image_full)):
                break

        print("current image full:",current_image_full)

        img_path = os.path.join(IMAGE_FOLDER, current_image_full)
        print('img_path',img_path)
        
        import json
        f = json.load(open(json_path, 'r'))

        img_with_layout = display_hisam_newapproach_sparas(img_path, f[current_image])
        
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_img_with_gts.jpg')
        print("Temp output path:",temp_output_path)
        cv2.imwrite(temp_output_path, img_with_layout)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        print("Relative path:",relative_path)
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index_hisam_new.html', current_image=current_image.split('.')[0], image_path='/images/output_images/output_img_with_gts.jpg', image_files=image_files)

    else:

        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index_hisam_new.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


@app.route('/display_lines_sorted/<int:image_index>>')
def show_image_sorted_lines(image_index):
    json_path = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/lines_paras_jsons/reading_order_results_1191.json'

    import pandas as pd
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_csv = image_files[image_index]

        print("current image:",current_image)

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in possible_extensions:
            current_image_full = f'{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER, current_image_full)):
                break

        print("current image full:",current_image_full)

        img_path = os.path.join(IMAGE_FOLDER, current_image_full)
        print('img_path',img_path)
        
        import json
        f = json.load(open(json_path, 'r'))

        img_with_layout = display_hisam_newapproach_lines_sorted(img_path, f[current_image])
        
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_img_with_gts.jpg')
        print("Temp output path:",temp_output_path)
        cv2.imwrite(temp_output_path, img_with_layout)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        print("Relative path:",relative_path)
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index_hisam_new.html', current_image=current_image.split('.')[0], image_path='/images/output_images/output_img_with_gts.jpg', image_files=image_files)

    else:

        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index_hisam_new.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")


@app.route('/display_words_sorted/<int:image_index>>')
def show_image_sorted_words(image_index):
    json_path = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/lines_paras_jsons/reading_order_results_1191.json'

    import pandas as pd
    if 0 <= image_index < total_images:
        current_image = image_files[image_index]
        current_image_csv = image_files[image_index]

        print("current image:",current_image)

        possible_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        for ext in possible_extensions:
            current_image_full = f'{current_image}{ext}'
            if os.path.exists(os.path.join(IMAGE_FOLDER, current_image_full)):
                break

        print("current image full:",current_image_full)

        img_path = os.path.join(IMAGE_FOLDER, current_image_full)
        print('img_path',img_path)
        
        import json
        f = json.load(open(json_path, 'r'))

        img_with_layout = display_hisam_newapproach_words_sorted(img_path, f[current_image])
        
        output_folder = '/home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/static/images/output_images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

        temp_output_path = os.path.join(output_folder, 'output_img_with_gts.jpg')
        print("Temp output path:",temp_output_path)
        cv2.imwrite(temp_output_path, img_with_layout)
        
        relative_path = os.path.relpath(temp_output_path, app.config['UPLOAD_FOLDER'])
        print("Relative path:",relative_path)
        
        #return render_template('conn_image.html', image_path=temp_output_path)
        return render_template('index_hisam_new.html', current_image=current_image.split('.')[0], image_path='/images/output_images/output_img_with_gts.jpg', image_files=image_files)

    else:

        # return "Invalid image index"
        print("Invalid image index")
        return render_template("index_hisam_new.html", current_image=None,image_path=None,image_files=image_files, error_message="Invalid image index")



if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5007)

