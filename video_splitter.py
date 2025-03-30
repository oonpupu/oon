import cv2
import os

print(cv2.__version__)

#여기에 파일 위치
filepath = 'D:/education/high school/data/20250324_103724.mp4'
print(f"Checking if file exists: {os.path.exists(filepath)}")


base_dir = os.path.dirname(filepath)
video_name = os.path.basename(filepath)[:-4]
output_dir = os.path.join(base_dir, video_name)
print(f"Output directory will be: {output_dir}")

try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    else:
        print(f"Directory already exists: {output_dir}")
except Exception as e:
    print(f"Error creating directory: {e}")
    exit(1)


video = cv2.VideoCapture(filepath)
if not video.isOpened():
    print(f"Could not open video: {filepath}")
    exit(1)


fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps if fps > 0 else 0
frame_interval = max(1, int(fps * 0.1))

print(f"Video properties:")
print(f"- FPS: {fps}")
print(f"- Total frames: {total_frames}")
print(f"- Duration: {duration:.2f} seconds")
print(f"- Frame interval for 0.1 sec: {frame_interval}")


count = 0
frame_index = 0

while True:
    ret, frame = video.read()
    
    if not ret:
        print(f"End of video reached after processing {frame_index} frames")
        break
    
    if frame_index % frame_interval == 0:
        output_path = os.path.join(output_dir, f"frame{count}.jpg")
        success = cv2.imwrite(output_path, frame)
        
        if success:
            print(f"Saved frame {count} (video frame {frame_index}) to {output_path}")
            count += 1
        else:
            print(f"Failed to save frame to {output_path}")
    
    frame_index += 1
    
    if frame_index % 100 == 0:
        print(f"Processed {frame_index} frames ({frame_index/total_frames*100:.1f}%)")

video.release()
print(f"Completed: Extracted {count} frames from {total_frames} total frames")
