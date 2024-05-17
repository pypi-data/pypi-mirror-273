from openCV_movement_detection import video_movement_class


def print_hi():
    movement = video_movement_class.VideoMovementClass()
    return movement.detect_movement('C:/Users/lenhe/Documents/videos-testen/cartoon_test.mp4')


if __name__ == '__main__':
    print(print_hi())
