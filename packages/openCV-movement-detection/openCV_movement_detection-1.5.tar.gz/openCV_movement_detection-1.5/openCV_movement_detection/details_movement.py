import cv2
import numpy as np


def get_mask(frame1, frame2, blur):
    frame_diff = cv2.absdiff(frame2, frame1)
    frame_diff = cv2.medianBlur(frame_diff, blur)
    frame_diff = apply_erosion(frame_diff, 2, 2)
    mask = cv2.adaptiveThreshold(frame_diff, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)

    return mask


def adjust_brightness(frame, brightness):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.multiply(v, brightness)
    v = np.clip(v, 0, 255).astype(np.uint8)
    hsv = cv2.merge((h, s, v))
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return frame


def apply_erosion(img, size, iterations):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)


def change_frame(frame, brightness):
    frame_bright = adjust_brightness(frame, brightness)
    frame_gray = cv2.cvtColor(frame_bright, cv2.COLOR_BGR2GRAY)
    frame_gray = apply_erosion(frame_gray, 1, 5)
    return frame_gray


def contour_movement(contours, circularity_threshold, min_contour_area):
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            circularity = cv2.contourArea(contour) / (np.pi * radius ** 2)
            if circularity < circularity_threshold:
                return True


def text_movement(movement_detected, prev_count, count):
    if movement_detected:
        return "Movement detected!" + " Between : frame " + str(prev_count) + " and frame " + str(count)
    else:
        return "No movement detected." + " Between : frame " + str(prev_count) + " and frame " + str(count)


def make_video_no_roi(frame, no_rois):
    frame_roi = frame.copy()
    for no_roi in no_rois:
        startX, endX = int(no_roi['startX']), int(no_roi['endX'])
        startY, endY = int(no_roi['startY']), int(no_roi['endY'])
        frame_roi[startY:endY, startX:endX] = 0
    return frame_roi


def make_video_roi(frame, rois):
    frame_roi = np.zeros_like(frame)  # Create black canvas of the same size as the input frame

    for roi in rois:
        startX, endX = int(roi['startX']), int(roi['endX'])
        startY, endY = int(roi['startY']), int(roi['endY'])

        # Copy the ROI from the original frame onto the black canvas
        frame_roi[startY:endY, startX:endX] = frame[startY:endY, startX:endX]

    return frame_roi
