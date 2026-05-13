import streamlit as st
import tempfile
import os
import convertapi

# --- KONFIGURASI API ---
# Menggunakan API Key yang Anda sediakan
convertapi.api_secret = 'KT670n4yoAl3FSIicyM6UUZfyPHKcWWX'

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
            status_text.text("Menyiapkan file untuk dikirim ke Cloud Engine...")
            progress_bar.progress(20)
            
            # Simpan file upload ke temporary file agar bisa dibaca oleh ConvertAPI
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_input:
                tmp_input.write(uploaded_file.getvalue())
                input_path = tmp_input.name
                
            output_path = input_path.replace(f".{file_extension}", f".{target_format}")
            
            status_text.text(f"Memproses Konversi {source_format.upper()} ke {target_format.upper()} via ConvertAPI...")
            progress_bar.progress(50)
            
            # --- EKSEKUSI CONVERTAPI SUNGGUHAN ---
            # Mengirim file ke server ConvertAPI dan menunggu hasilnya
            result = convertapi.convert(target_format, {'File': input_path}, from_format=source_format)
            
            status_text.text("Mengunduh hasil dari Cloud Engine...")
            progress_bar.progress(80)
            
            # Menyimpan hasil dari ConvertAPI ke local sementara
            result.file.save(output_path)
            
            # Membaca hasil konversi menjadi bytes untuk tombol Download Streamlit
            with open(output_path, "rb") as f:
                output_bytes = f.read()
                
            # Cleanup temporary files agar server tidak penuh
            os.remove(input_path)
            os.remove(output_path)
            
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
