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