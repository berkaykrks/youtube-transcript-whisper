import yt_dlp
import whisper
import ffmpeg
import os
import json

# 1. YouTube'dan Ses İndirme
def download_audio(video_url):
    # YDL (yt-dlp) seçenekleri
    ydl_opts = {
        'format': 'bestaudio/best',  # En iyi ses formatını seç
        'outtmpl': 'audio.%(ext)s',  # Çıktı dosyasının adı
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print("Audio downloaded successfully.")
    return 'audio.webm'  # İndirilen ses dosyasının formatı genellikle webm olabilir.

# 2. FFmpeg ile Ses Dosyasını MP3 Formatına Dönüştürme
def convert_audio(input_file, output_file):
    ffmpeg.input(input_file).output(output_file).run()
    print(f"Audio converted to {output_file}")

# 3. Whisper ile Transkript Çıkarmak
def transcribe_audio(file_path):
    model = whisper.load_model("base")  # Whisper modelini yükle
    result = model.transcribe(file_path)  # Dil parametresi belirtilmediği için otomatik dil algılaması yapılır
    return result["text"]

# 4. Transkripti JSON dosyasına kaydetme
def save_transcript_to_json(video_url, transcript, filename="transcripts.json"):
    # JSON dosyasını aç veya oluştur
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            transcripts_data = json.load(f)
    else:
        transcripts_data = {}

    # Video URL'si ve transkripti JSON verisine ekle
    transcripts_data[video_url] = transcript

    # JSON dosyasına kaydet
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(transcripts_data, f, ensure_ascii=False, indent=4)
    print(f"Transcription saved to {filename}")

# Ana İşlem Akışı
def main():
    video_url = input("YouTube video URL'sini girin (ya da boş bırakın): ")
    if not video_url:
        print("Geçerli bir video URL'si girmeniz gerekiyor!")
        return

    print("Downloading audio from YouTube...")
    audio_file = download_audio(video_url)

    # Dönüştürme işlemi gerekirse
    converted_audio_file = 'audio.mp3'
    if not os.path.exists(converted_audio_file):
        print("Converting audio to MP3 format...")
        convert_audio(audio_file, converted_audio_file)

    # Transkripti çıkarmak
    print("Transcribing audio...")
    transcript = transcribe_audio(converted_audio_file)  # Dil otomatik olarak tespit edilecek

    # Transkripti JSON dosyasına kaydet
    save_transcript_to_json(video_url, transcript)

if __name__ == "__main__":
    main()
