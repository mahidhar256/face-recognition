import cv2
import face_recognition
import csv
import datetime
import os

# Load known student images and create encodings
def load_known_faces(image_folder, specific_image_paths=[]):
    known_face_encodings = []
    known_face_names = []

    # Load images from the folder
    for filename in os.listdir(image_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            student_name = os.path.splitext(filename)[0]  # Extract name from filename
            image_path = os.path.join(image_folder, filename)

            try:
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)

                if encodings:  # Check if a face encoding exists
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(student_name)
                else:
                    print(f"Warning: No face detected in {filename}, skipping.")

            except Exception as e:
                print(f"Error loading {filename}: {e}")

    # Load each specific image provided in the list
    for image_path in specific_image_paths:
        specific_image_name = os.path.splitext(os.path.basename(image_path))[0]

        try:
            specific_image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(specific_image)

            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(specific_image_name)
            else:
                print(f"Warning: No face detected in {specific_image_name}, skipping.")

        except Exception as e:
            print(f"Error loading {specific_image_name}: {e}")

    return known_face_encodings, known_face_names

# Initialize CSV file
csv_file = "student_attendance.csv"
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Time"])  # Add headers

# Function to recognize faces and mark attendance
def recognize_and_record(known_face_encodings, known_face_names, tolerance=0.5):
    cap = cv2.VideoCapture(0)  # Open the default camera
    recorded_names = set()  # To avoid duplicate entries for a single session

    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return

    try:
        print("Starting the face recognition system. Press 'q' to stop.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame. Retrying...")
                continue  # Try to capture the next frame

            # Reduce frame size to increase processing speed
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Detect and encode faces in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
                name = "Unknown"

                # Find the closest match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = face_distances.argmin()

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                    # Record attendance if not recorded in session
                    if name not in recorded_names:
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with open(csv_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([name, timestamp])
                        recorded_names.add(name)
                        print(f"Recorded {name} at {timestamp}")

                # Draw rectangle and name around face
                top, right, bottom, left = [v * 4 for v in face_location]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            # Press 'q' to quit the program
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting and saving attendance data.")
                break

    finally:
        # Release the camera and close windows
        cap.release()
        cv2.destroyAllWindows()

# Folder containing known faces
known_faces_folder = r"C:\Users\kathu\Documents\known_face"  # Replace with your folder path

# List of specific image paths
specific_image_paths = [
    r"C:\Users\kathu\Desktop\face-recognition\mahi.jpg",  # Added mahi.jpg
]

# Load known faces
known_face_encodings, known_face_names = load_known_faces(known_faces_folder, specific_image_paths)

# Run the recognition and record function
recognize_and_record(known_face_encodings, known_face_names)
