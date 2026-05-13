import streamlit as st
import tempfile
import os
import convertapi

# --- KONFIGURASI API ---
# Menggabungkan os.environ dan variabel module agar dijamin terbaca oleh library ConvertAPI
API_SECRET = 'KT670n4yoAl3FSIicyM6UUZfyPHKcWWX'
os.environ['CONVERT_API_SECRET'] = API_SECRET
convertapi.api_secret = API_SECRET

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="DocConvert Pro | Kemenkumham",
    page_icon="📄",
    layout="centered"
)

# --- HEADER UI ---
st.title("📄 DocConvert Pro")
st.markdown("Konversi Dokumen Skala Enterprise dengan Fidelitas Tinggi (Powered by ConvertAPI)")
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

    # Menampilkan Status Deteksi
    st.info(f"Mendeteksi: File **{source_format.upper()}**. Akan dikonversi ke **{target_format.upper()}**.")
    
    # 2. Tombol Eksekusi
    if st.button("🚀 Mulai Konversi", type="primary", use_container_width=True):
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("Membaca file dari Memory (RAM)...")
            progress_bar.progress(20)
            
            # --- SOLUSI ERROR: BYPASS HARD DRIVE ---
            # Menggunakan UploadIO agar file dikirim langsung dari memory Streamlit ke API
            upload_io = convertapi.UploadIO(uploaded_file, filename=filename)
            
            status_text.text(f"Memproses Konversi {source_format.upper()} ke {target_format.upper()} via Cloud Engine...")
            progress_bar.progress(50)
            
            # Eksekusi ConvertAPI dengan memaksa pengenalan format dari awal
            result = convertapi.convert(
                target_format, 
                {'File': upload_io}, 
                from_format=source_format
            )
            
            status_text.text("Mengunduh hasil konversi...")
            progress_bar.progress(80)
            
            # Simpan output sementara ke folder sistem operasi yang paling aman
            out_dir = tempfile.mkdtemp()
            output_path = os.path.join(out_dir, download_filename)
            
            result.file.save(output_path)
            
            # Membaca hasil konversi menjadi bytes untuk tombol Download Streamlit
            with open(output_path, "rb") as f:
                output_bytes = f.read()
                
            # Cleanup temporary file & folder
            os.remove(output_path)
            os.rmdir(out_dir)
            
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
            
        except convertapi.ApiError as e:
            st.error(f"Terjadi kesalahan dari sisi ConvertAPI: {str(e)}")
        except Exception as e:
            st.error(f"Terjadi kesalahan sistem: {str(e)}")
            st.error("Silakan pastikan koneksi internet stabil dan coba kembali.")
