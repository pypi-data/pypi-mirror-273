def number_plate_detection():
    code = """
            !pip install easyocr
            !pip install imutils

            import cv2
            import matplotlib.pyplot as plt
            import numpy as np
            import easyocr
            import imutils

            image = cv2.imread("C:/Users/mahna/Downloads/car.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB))

            bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #noise reduction
            edged = cv2.Canny(bfilter, 30, 200)  # edge detection
            plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

            location = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                counter = 0
                if len(approx) == 4:
                        location = approx
                        counter = counter+1
                        if(counter == 3):
                            print(location)
                            break
            
            location

            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(image, image, mask = mask)

            plt.imshow(new_image)

            (x,y) = np.where(mask==255)
            (x1,y1) = (np.min(x), np.min(y))
            (x2,y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]

            plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            result

            result[0][1]
            """
    
    print(code)

print(number_plate_detection())