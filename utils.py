import cv2

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

def para_2(image,component):
    try:
        print(component)
        if 'Order' in component.columns and not component.empty:
            # Sort component based on order
            component = component.sort_values(by='Order')
        else:
            print("Error: 'Order' column not found or DataFrame is empty")
            return None  # Return the original image or some default value

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        centers=[]
        for idx, row in component.iterrows():
            top_left = (int(row['Left'][0]), int(row['Top'][1]))
            bottom_right = (int(row['Right'][0]), int(row['Bottom'][1]))
            #get center of the paragraph from top left and bottom right
            center = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2))
            centers.append(center)
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            cv2.putText(image, str(row['Order']), (int(row['Left'][0]), int(row['Top'][1] - 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        for i in range(1, len(centers)):
            cv2.line(image, centers[i - 1], centers[i], (0, 0, 255), 2)
        
        return image
    except Exception as e:
        print(e)
        return image

def reading_order_with_line(image, euclidean, header_p, footer_p):
    regions = []
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_with_boxes = image_rgb.copy()

    # Store centers of bounding boxes
    centers = []

    for index, row in euclidean.iterrows():
        left = int(row['Left'][0])
        right = int(row['Right'][0])
        top = int(row['Top'][1])
        bottom = int(row['Bottom'][1])

        Order = int(row['Order'])
        line_number = int(row['LineNumber'])

        width = right - left
        height = bottom - top

        top_left = (left, top)
        bottom_right = (right, bottom)
        cv2.rectangle(image_with_boxes, top_left, bottom_right, (255, 0, 0), 2)

        # Calculate the center of the bounding box
        center_x = left + width // 2
        center_y = top + height // 2
        centers.append((center_x, center_y))

        label_position = (left, top - 10)
        label_position_2 = (left + 40, top - 10)
        cv2.putText(image_with_boxes, str(Order), label_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        box_with_order = {}
        box_with_order['bounding_box'] = {}
        box_with_order['bounding_box']['x'] = left
        box_with_order['bounding_box']['y'] = top
        box_with_order['bounding_box']['w'] = width
        box_with_order['bounding_box']['h'] = height
        box_with_order['order'] = Order
        box_with_order['line'] = line_number
        regions.append(box_with_order)

    # Draw thick lines connecting the centers of bounding boxes
    thickness = 5
    color = (0, 0, 255)  # Green color
    for i in range(len(centers) - 1):
        cv2.line(image_with_boxes, centers[i], centers[i + 1], color, thickness)

    # Draw header and footer lines
    image_height, image_width, _ = image_with_boxes.shape
    header_percentage = header_p
    footer_percentage = footer_p
    header_position = int(image_height * (header_percentage / 100))
    footer_position = image_height - int(image_height * (footer_percentage / 100))
    cv2.line(image_with_boxes, (0, header_position), (image_width, header_position), (255, 255, 0), 2)
    cv2.line(image_with_boxes, (0, footer_position), (image_width, footer_position), (255, 255, 0), 2)

    return image_with_boxes, regions


#New idea of getting word reading order by sorting the words from left to right and top to bottom

def get_box_id_from_coordinates(boxes_df, box_coordinates):
    """Get the index of the box in boxes_df based on its coordinates."""
    x1,y1,x2,y2 = box_coordinates
    for index, row in boxes_df.iterrows():
        if (int(row['Top'][1]) == int(y1) and
            int(row['Left'][0]) == int(x1) and
            int(row['Bottom'][1]) == int(y2) and
            int(row['Right'][0]) == int(x2)):
            return index
    return None

def get_TLBR_from_CSV(df):
    top = df['Top']
    left = df['Left']
    bottom = df['Bottom']
    right = df['Right']
   
    top_left = [int(left[0]), int(top[1])]
    bottom_right = [int(right[0]), int(bottom[1])]
   
    return [top_left[0],top_left[1], bottom_right[0], bottom_right[1]]

def sort_boxesy(box):
    return box[1]

def sort_boxesx(box):
    return box[0]

def calculate_median(boxes):
    boxes.sort()
    n = len(boxes)
    if n % 2 == 0:
        return (boxes[n//2] + boxes[n//2 - 1])/2
    else:
        return boxes[n//2]

def sort_words(boxes, image): #from Krishna Tulsyan's code
    """Sort boxes - (x, y, x+w, y+h) from left to right, top to bottom."""
    mean_height = sum([y2 - y1 for _, y1, _, y2 in boxes]) / len(boxes)
    median_height = calculate_median([y2 - y1 for _, y1, _, y2 in boxes])

    # print("MEAN HEIGHT",mean_height)
    # print("MEDIAN HEIGHT",median_height)
    # boxes.view('i8,i8,i8,i8').sort(order=['f1'], axis=0)
    current_line = boxes[0][1]
    lines = []
    tmp_line = []

    order=0
    # for expt: to see if the sorted_coordinates_y are correctly in a same line
    # for box in boxes:
    #     order+=1
    #     cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
    #     cv2.putText(image, str(order), (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
    # cv2.imwrite('/home2/sreevatsa/ops/boxes_ordered_test_2.png', image)


    for box in boxes:
        # if box[1] > current_line + mean_height:
        if box[1] >= current_line + (median_height/2):
            lines.append(tmp_line)
            tmp_line = [box]
            current_line = box[1]
            continue
        tmp_line.append(box)
    lines.append(tmp_line)

    for line in lines:
        line.sort(key=lambda box: box[0])

    return lines


def get_coordinates_from_component(component_df, boxes_df, image_file, attributes):

    (font_size, font_thickness, box_thickness, line_thickness) = attributes
    # image = cv2.imread(image_file)
    image = cv2.cvtColor(image_file, cv2.COLOR_BGR2RGB)
    order = 0
    c = 0
    centers = []  # List to store the centers of the boxes
    # boxes_df.loc[:,'Visited'] = 0
    # boxes_df.loc[:,'Order'] = -1
    for index, row in component_df.iterrows():
        c += 1
        coordinates = []
        box_ids = row['Component'][0]
        for box_id in box_ids:
            coordinates.append(get_TLBR_from_CSV(boxes_df.iloc[box_id]))

        sorted_coordinates_y = sorted(coordinates, key=sort_boxesy)
        sorted_coos = sort_words(sorted_coordinates_y, image)

        cc=0
        for line in sorted_coos:
            cc+=1
            for i, box in enumerate(line):
                # print(box)
                # box_id = get_box_id_from_coordinates(boxes_df, box)

                # if boxes_df.at[box_id, 'Visited'] == 0:
                order += 1
                center = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)  # Calculate the center of the box
                centers.append(center)  # Add the center to the list
                cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), box_thickness)
                cv2.putText(image, str(order), (box[0], box[1] - 0), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 0, 0), font_thickness)

                # Update the Order column in boxes_df with the current order value
                #box_id = get_box_id_from_coordinates(boxes_df, box)
                #boxes_df.at[box_id, 'Order'] = order
                #boxes_df.at[box_id, 'Visited'] = 1

    # Draw a line between each pair of consecutive centers
    for i in range(1, len(centers)):
        cv2.line(image, centers[i - 1], centers[i], (0, 0, 255), line_thickness)

    #boxes_df = boxes_df.sort_values(by='Order')
    #boxes_df.to_csv('//home/vatsasree/Research/scripts/applic/Reading-Order-Visualizer/boxes_df.csv', index=False)  
    # return boxes_df
    return image

def page_size(image_file):
    image = cv2.imread(image_file)
    height, width, _ = image.shape
    return height, width

# def ignore_margins(component, width_p, header, footer, image_file):
#     height, width = page_size(image_file)
#     top_margin = height*(header/100)
#     bottom_margin = height*(footer/100)
#     # left_margin = width*(left_m/100)
#     # right_margin = width*(right_m/100)
#     # vertical_margin = height*(height_p/100)
#     horizontal_margin = width*(width_p/100)
#     # for i in range(len(component)):
#     #     if((component['Top'][i][1] > height - vertical_margin) and len(component['Component'][i][0])<7):
#     #         component = component.drop(i)
#     #     elif((component['Bottom'][i][1] < vertical_margin) and len(component['Component'][i][0])<7):
#     #         component = component.drop(i)
#     #     elif(component['Right'][i][0] < horizontal_margin):
#     #         component = component.drop(i)
#     #     elif(component['Left'][i][0] > width - horizontal_margin):
#     #         component = component.drop(i)
#     #     else:
#     #         continue
#     for i in range(len(component)):
#         print(component['Top'][i][1])
#         if((component['Top'][i][1] < (top_margin)) and len(component['Component'][i][0])<10):
#             # component = component.drop(i)
#             component = component.drop(i)
#         # elif((component['Bottom'][i][1] > (height - bottom_margin)) and len(component['Component'][i][0])<10):
#         #     component = component.drop(i)
#         elif((component['Top'][i][1] > (height - bottom_margin)) and len(component['Component'][i][0])<10):
#             component = component.drop(i)
#         elif(component['Right'][i][0] < horizontal_margin):
#             component = component.drop(i)
#         elif(component['Left'][i][0] > width - horizontal_margin):
#             component = component.drop(i)
#         else:
#             continue
#     return component

def ignore_margins(component, width_p, header, footer, image_file):
    height, width = page_size(image_file)
    top_margin = height * (header / 100)
    bottom_margin = height * (footer / 100)
    horizontal_margin = width * (width_p / 100)

    # Create a boolean mask based on the conditions
    mask = (
        (component['Top'].apply(lambda x: x[1]) >= top_margin) &
        (component['Top'].apply(lambda x: x[1]) <= (height - bottom_margin)) &
        (component['Right'].apply(lambda x: x[0]) >= horizontal_margin) &
        (component['Left'].apply(lambda x: x[0]) <= (width - horizontal_margin))
    )

    # Filter the DataFrame based on the mask
    filtered_component = component[mask]

    return filtered_component.reset_index(drop=True)
