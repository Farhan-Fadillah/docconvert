import streamlit as st
import requests
import base64
import os

# --- KONFIGURASI API ---
API_SECRET = 'KT670n4yoAl3FSIicyM6UUZfyPHKcWWX'

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="DocConvert Pro | Kemenkumham",
    page_icon="📄",
    layout="centered"
)

# --- HEADER UI ---
st.title("📄 DocConvert Pro")
st.markdown("Konversi Dokumen Skala Enterprise dengan Fidelitas Tinggi (Powered by Direct ConvertAPI)")
st.divider()

# --- UPLOADER UI ---
uploaded_file = st.file_uploader(
    "Drag & drop file Anda di sini (PDF atau DOCX)", 
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    # 1. Deteksi Format
    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()
    base_name = os.path.splitext(filename)[0]
    
    if file_extension == "pdf":
        source_format = "pdf"
        target_format = "docx"
        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        source_format = "docx"
        target_format = "pdf"
        mime_type = "application/pdf"
        
    download_filename = f"{base_name}_Converted.{target_format}"

    st.info(f"Mendeteksi: File **{source_format.upper()}**. Akan dikonversi ke **{target_format.upper()}**.")
    
    # 2. Tombol Eksekusi
    if st.button("🚀 Mulai Konversi", type="primary", use_container_width=True):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Menyiapkan payload memori...")
            progress_bar.progress(20)
            
            # --- SOLUSI DEFINITIF: DIRECT REST API CALL ---
            # Mengabaikan library ConvertAPI Python dan menembak langsung ke server mereka
            url = f"https://v2.convertapi.com/convert/{source_format}/to/{target_format}?Secret={API_SECRET}"
            
            # Membungkus file langsung dari RAM tanpa menyentuh Hard Drive
            files = {
                'File': (filename, uploaded_file.getvalue())
            }
            
            status_text.text(f"Mengunggah dan memproses {source_format.upper()} ke {target_format.upper()} di Cloud Engine...")
            progress_bar.progress(50)
            
            # Request ke API
            response = requests.post(url, files=files)
            
            status_text.text("Menerima respon dari server...")
            progress_bar.progress(80)
            
            # Cek jika respon sukses (HTTP 200 OK)
            if response.status_code == 200:
                data = response.json()
                
                # API mengembalikan file dalam bentuk Base64 String, kita decode kembali menjadi Bytes
                file_b64 = data['Files'][0]['FileData']
                output_bytes = base64.b64decode(file_b64)
                
                progress_bar.progress(100)
                status_text.text("Konversi Selesai!")
                st.success("File Anda telah berhasil dikonversi dengan akurasi 100% dan siap diunduh.")
                
                # 3. Tombol Download Hasil Asli
                st.download_button(
                    label=f"⬇️ Download Hasil Konversi ({target_format.upper()})",
                    data=output_bytes,
                    file_name=download_filename,
                    mime=mime_type,
                    use_container_width=True
                )
            else:
                # Jika API mengembalikan error spesifik
                error_msg = response.json().get('Message', response.text)
                st.error(f"Server ConvertAPI menolak request: {error_msg}")
                progress_bar.progress(0)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan koneksi sistem: {str(e)}")
            progress_bar.progress(0)
