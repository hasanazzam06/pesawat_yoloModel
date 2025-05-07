import os

def create_file_list(image_folder, output_file):
    # List untuk menyimpan path gambar
    file_list = []
    
    # Cek jika folder ada
    if os.path.exists(image_folder):
        # Iterasi semua file di folder gambar
        for filename in os.listdir(image_folder):
            # Cek apakah file berformat .jpg atau .png (sesuaikan dengan format gambar yang digunakan)
            if filename.endswith(('.jpg', '.png')):
                # Buat path relatif file gambar
                file_path = os.path.join(image_folder, filename)
                file_list.append(file_path.replace("\\", "/"))  # Ganti backslash untuk Windows dengan slash
        
        # Tulis file list ke file output
        with open(output_file, 'w') as f:
            for file_path in file_list:
                f.write(file_path + '\n')
        print(f"{output_file} berhasil dibuat dengan {len(file_list)} gambar.")
    else:
        print(f"Folder {image_folder} tidak ditemukan.")

# Folder gambar dan output file
image_folder_train = 'data_pesawat/images/train'  # Ganti dengan path folder gambar training
output_train_txt = 'data_pesawat/train.txt'  # Ganti dengan nama file output yang diinginkan

image_folder_val = 'data_pesawat/images/val'  # Ganti dengan path folder gambar validasi
output_val_txt = 'data_pesawat/valid.txt'  # Ganti dengan nama file output yang diinginkan

# Buat train.txt dan valid.txt
create_file_list(image_folder_train, output_train_txt)
create_file_list(image_folder_val, output_val_txt)
