import cv2
import cvzone
import os

def addShirt(frame, landmarks, imgIndex, rightCounter, leftCounter, shirtList, shirtDir, ratio, shirtRatio, speed, rightButtonImg, leftButtonImg):
    # Get positions of landmarks 11 and 12
    landmark11 = landmarks[11][1:3]
    landmark12 = landmarks[12][1:3]
    print(landmark11, landmark12)
    
    # Load the current shirt image
    shirtImg = cv2.imread(os.path.join(shirtDir, shirtList[imgIndex]), cv2.IMREAD_UNCHANGED)

    # Calculate the shirt image width based on the distance between landmarks 11 and 12
    shirtWidth = int((landmark11[0] - landmark12[0]) * ratio)

    # Resize the shirt image
    if shirtWidth > 0 and shirtRatio > 0:
        shirtImg = cv2.resize(shirtImg, (shirtWidth, int(shirtWidth * shirtRatio)))


    # Calculate the current scale and offset
        currentScale = (landmark12[0] - landmark12[0]) / 190
        offset = int(44 * currentScale), int(48 * currentScale)


    # Overlay the shirt image onto the frame
    try:
        frame = cvzone.overlayPNG(frame, shirtImg, (landmark12[0]  - offset[0], landmark12[1] -  - offset[1] ))
    except:
        print("Error")
        pass

    # Overlay the button images onto the frame
    frame = cvzone.overlayPNG(frame, rightButtonImg, (1074, 293))
    frame = cvzone.overlayPNG(frame, leftButtonImg, (72, 293))
    
    # Check if the user is pointing to the right button
    if landmarks[16][1] < 300:
        # Increment the right counter and draw a progress indicator
        rightCounter += 1
        cv2.ellipse(frame, (139, 360), (66, 66), 0, 0,
                    rightCounter * speed, (0, 255, 0), 20)
        # If the progress indicator completes a full circle, change the current shirt image
        if rightCounter * speed > 360:
            rightCounter = 0
            if imgIndex < len(shirtList) - 1:
                imgIndex += 1
    # Check if the user is pointing to the left button
    elif landmarks[15][1] > 900:
        # Increment the left counter and draw a progress indicator
        leftCounter += 1
        cv2.ellipse(frame, (1138, 360), (66, 66), 0, 0,
                    leftCounter * speed, (0, 255, 0), 20)
        # If the progress indicator completes a full circle, change the current shirt image
        if leftCounter * speed > 360:
            leftCounter = 0
            if imgIndex > 0:
                imgIndex -= 1
    else:
        # If the user is not pointing to any button, reset the counters
        rightCounter = 0
        leftCounter = 0

    return frame, imgIndex, rightCounter, leftCounter