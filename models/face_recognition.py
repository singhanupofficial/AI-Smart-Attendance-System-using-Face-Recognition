import os
import cv2
import numpy as np
import json
from deepface import DeepFace
from config import Config
from database import get_all_students, mark_attendance

def extract_embedding(image_path):
    """Generates face embedding using FaceNet and RetinaFace."""
    try:
        # enforce_detection=False prevents crashes if no face is found
        representations = DeepFace.represent(
            img_path=image_path,
            model_name=Config.MODEL_NAME,
            detector_backend=Config.DETECTOR_BACKEND,
            enforce_detection=False
        )
        if representations and len(representations) > 0:
            return representations[0]['embedding']
    except Exception as e:
        print(f"Embedding extraction error: {e}")
    return None

def recognize_face(frame):
    """
    Detects face in frame, extracts embedding, and matches with database.
    Returns (student_id, student_name) or (None, None).
    """
    # Save frame temporarily for DeepFace processing
    temp_path = os.path.join(Config.DATASET_DIR, 'temp_frame.jpg')
    cv2.imwrite(temp_path, frame)
    
    embedding = extract_embedding(temp_path)
    if embedding is None:
        return None, None

    students = get_all_students()
    best_match_id = None
    best_match_name = None
    max_similarity = -1

    for student in students:
        if student['Face_Embedding']:
            db_embedding = np.array(json.loads(student['Face_Embedding']))
            
            # Calculate Cosine Similarity
            dot_product = np.dot(embedding, db_embedding)
            norm_a = np.linalg.norm(embedding)
            norm_b = np.linalg.norm(db_embedding)
            similarity = dot_product / (norm_a * norm_b)
            
            if similarity > max_similarity and similarity > Config.SIMILARITY_THRESHOLD:
                max_similarity = similarity
                best_match_id = student['Student_ID']
                best_match_name = student['Name']

    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if best_match_id:
        # Mark attendance automatically
        mark_attendance(best_match_id)
        return best_match_id, best_match_name
    
    return None, None

def generate_frames(camera_index=0):
    """Generator function for webcam streaming with face recognition."""
    camera = cv2.VideoCapture(camera_index)
    recognized_names = {}  # Cache to prevent flickering and DB overload
    
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            
            # Resize for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            
            # Process every 3rd frame to save CPU
            if camera.get(cv2.CAP_PROP_POS_FRAMES) % 3 == 0:
                student_id, name = recognize_face(small_frame)
                if name:
                    recognized_names[student_id] = name

            # Draw boxes and names on the original frame
            # (Simplified: just showing recognized names on the side for this implementation)
            y_offset = 30
            for sid, sname in recognized_names.items():
                cv2.putText(frame, f"ID: {sid} - {sname}", (10, y_offset), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                y_offset += 30

            # Encode frame for web streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        camera.release()