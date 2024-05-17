import os
import cv2
import imageio

from openCV_movement_detection.details_movement import change_frame, get_mask, contour_movement, text_movement, \
    make_video_no_roi, make_video_roi


class VideoMovementClass:

    def detect_movement(self, source_path, rois=None, no_rois=None, min_contour_area=10, circularity_threshold=0.5,
                        blur=1,
                        brightness=1, difference_between_frames=20, destination_path = '/movement_analysis/'):
        if blur % 2 == 0:
            blur -= 1
        filename = os.path.basename(source_path)
        cap = cv2.VideoCapture(source_path)
        ret, prev_frame = cap.read()
        prev_frame_gray = change_frame(prev_frame, brightness)
        if no_rois:
            prev_frame_gray = make_video_no_roi(prev_frame_gray, no_rois)
        if rois:
            prev_frame_gray = make_video_roi(prev_frame_gray, rois)
        text_list = []
        count = 0
        prev_count = 1
        while True:
            ret, next_frame = cap.read()
            if not ret:
                break
            count += 1
            if (count % difference_between_frames) == 0:
                next_frame_gray = change_frame(next_frame, brightness)
                if no_rois:
                    next_frame_gray = make_video_no_roi(next_frame_gray, no_rois)
                if rois:
                    next_frame_gray = make_video_roi(next_frame_gray, rois)
                mask = get_mask(prev_frame_gray, next_frame_gray, blur)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                movement_detected = contour_movement(contours, circularity_threshold, min_contour_area)
                text_list.append(text_movement(movement_detected, prev_count, count))
                self.save_animated_frames(filename, prev_frame, next_frame, prev_count, count, destination_path)
                prev_frame = next_frame
                prev_frame_gray = next_frame_gray
                prev_count = count
        cap.release()
        return text_list

    def save_animated_frames(self, filename, prev_frame, next_frame, prev_count, count, destination_path):
        filename = filename.replace('.mp4', '_')
        output_file = filename + str(prev_count) + '_' + str(count) + '.webp'
        output_dir = os.path.join(destination_path, filename)
        image_path = os.path.join(output_dir, output_file)
        # Check if the directory already exists
        if not os.path.exists(image_path):
            os.makedirs(output_dir, exist_ok=True)

            # Ensure consistent color space (e.g., convert BGR to RGB)
            prev_frame_rgb = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2RGB)
            next_frame_rgb = cv2.cvtColor(next_frame, cv2.COLOR_BGR2RGB)

            frames = [prev_frame_rgb, next_frame_rgb]
            frame_duration = 0.01

            # Save frames as an animated WebP
            imageio.mimsave(image_path, frames, duration=frame_duration)


