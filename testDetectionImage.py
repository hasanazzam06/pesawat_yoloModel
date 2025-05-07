# Mengimpor dependensi yang diperlukan
import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab.patches import cv2_imshow

# Menyediakan file konfigurasi dan file bobot model
config_path = '/content/yolo_dataset/nn/pesawat.cfg'  # Sesuaikan path file .cfg
weights_path = '/content/yolo_dataset/nn/backup/pesawat_final.weights'  # Path ke file weights
names_path = '/content/yolo_dataset/nn/pesawat.names'  # Path ke file .names (class labels)

# Membaca file konfigurasi dan weights
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

# Load label kelas
with open(names_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Menggunakan gambar baru untuk deteksi
image_path = '/content/drive/MyDrive/ProjectYolo/download.jpg'  # Ganti dengan path gambar yang ingin diuji
img = cv2.imread(image_path)
height, width, channels = img.shape

# Mengubah gambar untuk sesuai dengan format YOLO (resize dan normalisasi)
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

# Memberikan input gambar ke model
net.setInput(blob)
outs = net.forward(output_layers)

# Mengambil informasi deteksi
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:  # Threshold confidence, misal 50%
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Menggunakan Non-Maximum Suppression untuk menghindari deteksi ganda
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Menampilkan hasil deteksi
if len(indexes) > 0:
    for i in indexes.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i], 2))
        color = (0, 255, 0)  # Hijau untuk kotak deteksi
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label + " " + confidence, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Menampilkan hasil
cv2_imshow(img)
