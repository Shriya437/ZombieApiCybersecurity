import cv2
import torch
import os
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
from torch.nn.functional import cosine_similarity

# ------------------------------
# CONFIG
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "admin_img_dataset")
THRESHOLD = 0.65

# ------------------------------
# LOAD MODELS
# ------------------------------
mtcnn = MTCNN(image_size=160, margin=0)
model = InceptionResnetV1(pretrained='vggface2').eval()

# ------------------------------
# BUILD FACE DATABASE
# ------------------------------
def build_face_database():
    face_db = {}

    for person in os.listdir(DATASET_PATH):
        person_path = os.path.join(DATASET_PATH, person)

        if not os.path.isdir(person_path):
            continue

        embeddings = []

        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)

            img = cv2.imread(img_path)
            if img is None:
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)

            face = mtcnn(img_pil)
            if face is None:
                continue

            emb = model(face.unsqueeze(0))
            emb = emb / emb.norm()   # normalize
            embeddings.append(emb)

        if len(embeddings) > 0:
            avg_emb = torch.mean(torch.stack(embeddings), dim=0)
            face_db[person] = avg_emb

    print(f"[INFO] Loaded {len(face_db)} admin faces")
    return face_db


# ------------------------------
# VERIFY FACE (IMAGE BASED)
# ------------------------------
def verify_face(face_db, image_path, admin_id="P1"):
    if admin_id not in face_db:
        print("[ERROR] Admin not found in DB")
        return False

    img = cv2.imread(image_path)
    if img is None:
        print("[ERROR] Image not found")
        return False

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    face = mtcnn(img_pil)
    if face is None:
        print("[ERROR] No face detected")
        return False

    test_emb = model(face.unsqueeze(0))
    test_emb = test_emb / test_emb.norm()

    sim = cosine_similarity(test_emb, face_db[admin_id])

    print(f"[INFO] Similarity: {sim.item():.4f}")

    return sim.item() > THRESHOLD


# ------------------------------
# REAL-TIME ADMIN LOGIN (WEBCAM)
# ------------------------------
def admin_login(face_db, admin_id="P1"):
    cap = cv2.VideoCapture(0)

    print("[INFO] Looking for admin face... Press Q to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb)

        face = mtcnn(img_pil)

        if face is not None:
            emb = model(face.unsqueeze(0))
            emb = emb / emb.norm()

            sim = cosine_similarity(emb, face_db[admin_id])

            if sim.item() > THRESHOLD:
                print(f"[ACCESS GRANTED] Welcome Admin ({sim.item():.3f})")
                cap.release()
                cv2.destroyAllWindows()
                return True

            cv2.putText(frame, f"Not Authorized ({sim.item():.2f})",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)

        cv2.imshow("Admin Face Login", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False


# ------------------------------
# MAIN (TEST)
# ------------------------------
if __name__ == "__main__":
    face_db = build_face_database()

    # OPTION 1: Test with image
    # result = verify_face(face_db, "test.jpg")
    # print("Access:", result)

    # OPTION 2: Webcam Login
    success = admin_login(face_db)

    if success:
        print("✅ Proceed to Zombie API Dashboard")
    else:
        print("❌ Access Denied")