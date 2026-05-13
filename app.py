import streamlit as st
import time
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="DocConvert Pro | Kemenkumham",
    page_icon="📄",
    layout="centered"
)

# --- FUNGSI DOWNLOAD (SIMULASI/DUMMY UNTUK PROTOTIPE) ---
# Di sistem nyata, ini akan membaca file hasil konversi beneran.
def create_dummy_result(filename, target_format):
    content = f"""=========================================
 DOKUMEN SIMULASI DOCCONVERT PRO
=========================================

Ini adalah file hasil konversi untuk keperluan prototipe UI/UX.

[Data Pekerjaan]
- File Asli     : {filename}
- Format Target : {target_format.upper()}
- Status        : Berhasil Dikonversi dengan Fidelitas Tinggi.
"""
    return content.encode('utf-8')

# --- HEADER UI ---
st.title("📄 DocConvert Pro")
st.markdown("Konversi Dokumen Skala Enterprise dengan Fidelitas Tinggi")
st.divider()

# --- UPLOADER UI ---
uploaded_file = st.file_uploader(
    "Drag & drop file Anda di sini (PDF atau DOCX)", 
    type=["pdf", "docx", "doc"]
)

if uploaded_file is not None:
    # 1. Deteksi Format
    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()
    
    if file_extension == "pdf":
        source_format = "PDF"
        target_format = "DOCX"
    else:
        source_format = "Word"
        target_format = "PDF"

    # Menampilkan Status Deteksi
    st.info(f"Mendeteksi: File **{source_format}**. Akan dikonversi ke **{target_format}**.")
    
    # 2. Tombol Eksekusi
    if st.button("🚀 Mulai Konversi", type="primary", use_container_width=True):
        
        # --- PROSES SIMULASI / INTEGRASI ENGINE ---
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Memulai inisiasi job...")
        time.sleep(1)
        
        status_text.text(f"Membaca {filename} dan memecah menjadi chunk...")
        progress_bar.progress(25)
        time.sleep(1.5)
        
        status_text.text(f"Memproses {target_format} menggunakan parallel workers...")
        progress_bar.progress(60)
        time.sleep(2)
        
        status_text.text("Menggabungkan hasil (Merging)...")
        progress_bar.progress(85)
        time.sleep(1)
        
        progress_bar.progress(100)
        status_text.text("Konversi Selesai!")
        st.success("File Anda telah berhasil dikonversi dan siap diunduh.")
        
        # 3. Tombol Download
        dummy_file_data = create_dummy_result(filename, target_format)
        base_name = os.path.splitext(filename)[0]
        
        # Supaya tidak error saat di buka (seperti kasus MS Word sebelumnya),
        # untuk prototipe ini kita paksa unduh sebagai .txt
        download_filename = f"{base_name}_Converted.txt" 
        
        st.download_button(
            label=f"⬇️ Download Hasil Konversi",
            data=dummy_file_data,
            file_name=download_filename,
            mime="text/plain",
            use_container_width=True
        )