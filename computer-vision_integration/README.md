# Bilgisayarla Görü Entegrasyonu

## Genel Bakış

Bu modül **çoklu kişi gerçek zamanlı dikkat takibi** uygular:  
- **MediaPipe** ile yüz ağı tespiti  
- **EasyOCR** ile öğrenci adlarının kimlik kartı/rozetlerden okunması  
- **OpenCV** ile görüntü işleme ve kafa poz tahmini  
- **Özel mantık** ile bakış yönü tespiti, dikkat puanlama ve oturum metriklerinin kaydı  

Sistem:  
1. Karelerdeki yüzleri (video dosyası veya webcam) algılar  
2. Her kişiye benzersiz bir **Öğrenci ID’si** atar  
3. **Öğrenci adını** OCR ile okur (yalnızca ilk göründüğünde)  
4. **Bakış yönünü** ve **kafa pozunu** takip eder  
5. **Dikkatli / dikkatsiz** durumunu belirler  
6. Tüm sonuçları **CSV dosyasına** kaydeder (backend işlemeye hazır)  

## Klasör Yapısı
```
computer_vision_integration/
│
├── frame_processor.py    # Kare işleme ana yöneticisi
├── face_utils.py         # Yüz algılama, kırpma, ID atama
├── metrics.py            # Bakış yönü ve kafa poz tahmini
├── csv_logger.py         # Metrik hesaplama ve CSV yazma
├── ocr_photo.py          # OCR ile isim çıkarma
├── id_manager.py         # ID ile çıkarılan isim/foto eşleşmelerini yönetir
├── main.py               # Giriş noktası; modülleri başlatır ve takip hattını çalıştırır
├── requirements.txt      # Python bağımlılıkları
└── README.md             # Bu dosya
```

## Kurulum

**1. Depoyu klonlayın**
```bash
git clone https://github.com/muhammederbay10/BTK-HACKATHON-2025-EduVision.git
cd computer_vision_integration
```
**2. Sanal ortam oluşturun ve etkinleştirin**
```
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```
**3. Bağımlılıkları yükleyin**
```
pip install -r requirements.txt
```

## Kullanım
Video dosyası ile çalıştırma:
```
python frame_processor.py --video_path test-data/test_video.mp4 --output_csv output.csv
```

Canlı webcam ile çalıştırma:
```
python frame_processor.py --video_path "" --output_csv live_log.csv
```
Komut satırı argümanları:

```--video_path```:	Giriş video dosyasının yolu. Webcam için boş string ("").
```--output_csv```:	Çıkış CSV log dosyasının yolu.

## Çıktı
Her çalıştırma, şu sütunlara sahip bir CSV log üretir:
---
| Sütun Adı                 | Açıklama                                                  |
|---------------------------|-----------------------------------------------------------|
| `student_id`              | Her yüz için benzersiz ID                                 |
| `timestamp`               | ISO formatlı zaman damgası                                |
| `frame_idx`               | Kare numarası                                             |
| `attention_status`        | Dikkatli / Dikkatsiz                                      |
| `gaze`                    | Sol / Orta / Sağ / Bilinmiyor                             |
| `yaw_angle_deg`           | Kafa yaw açısı (derece)                                   |
| `attention_score`         | Bu kareye kadar dikkatli geçirilen zaman yüzdesi          |
| `distraction_events`      | Dikkat kaybı olay sayısı                                  |
| `yawning_count`           | (Yer tutucu) — henüz uygulanmadı                          |
| `eye_closure_duration_sec`| (Yer tutucu) — henüz uygulanmadı                          |
| `focus_quality`           | (Yer tutucu) — henüz uygulanmadı                          |
| `session_duration_minutes`| Öğrencinin ilk karesinden itibaren geçen süre (dakika)    |
---

Ayrıca, kırpılmış öğrenci yüz görüntüleri ```photo_id/``` klasörüne kaydedilir ve ID–isim eşleşmeleri ```photo_id/id_name_mapping.json``` dosyasında tutulur.

## Backend Entegrasyonu

Backend sunucusu, CSV’yi periyodik olarak okuyarak gerçek zamanlı dikkat metriklerini toplayabilir, ID/foto eşleşmelerini JSON dosyasından alabilir ve toplu skorlarla raporlar veya uyarılar üretebilir. Bu tasarım, sistemin diğer eğitim, analiz veya izleme platformlarına sorunsuz entegrasyonunu sağlar.

## Notlar

- **Performans:** EasyOCR CPU açısından yoğundur. Donanımınız destekliyorsa ```ocr_photo.py``` içinde ```gpu=True``` yaparak GPU modunu etkinleştirebilirsiniz.
- **Ölçeklenebilirlik:** Varsayılan MediaPipe ayarlarıyla gerçek zamanlı olarak 15 yüze kadar takip yapılabilir (face_utils.py içinde değiştirilebilir).
- **Aydınlatma:** Kafa poz tahmini, iyi aydınlatılmış sahnelerde en güvenilirdir.

## Sorun Giderme
Sorun yaşarsanız:
- Tüm bağımlılıkların yüklü olduğundan emin olun (```requirements.txt```)
- Mediapipe desteği için Python 3.10 veya 3.11 kullanıldığını doğrulayın
- Problem devam ederse, depoda bir issue açın ve net tekrar adımları, tam hata mesajını ve kısa bir ortam açıklamasını ekleyin.
