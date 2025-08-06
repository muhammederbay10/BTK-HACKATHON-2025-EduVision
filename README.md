# EduVision - Dikkat Takip Platformu

EduVision, öğretmenlerle birebir görüşmeler sonucunda özellikle online eğitimde dikkat takibinin ciddi bir sorun olduğunu gözlemleyen İskenderiye AI takımı tarafından geliştirilmiştir. Online derslerde öğretmenle, fiziksel sınıfta olduğu gibi öğrencilerin dikkat durumunu doğrudan gözlemleyemekte zorluk çekiyor ve sınıf içi etkileşimi kaybetmektedir. Bu nedenle dikkat kaybı anlarının tespiti kritik hâle gelmektedir. Projede, öğrencilerin eğitim videoları izlerken ne kadar dikkatli olduklarını anlık olarak analiz eden ve öğretmenlere kapsamlı geri bildirim ve özet rapor sağlayan bir GEMINI API (LLM) kullandık.

Temel amacımız; öğretmenlerin, hangi zaman aralıklarında ve neden öğrencilerin dikkatini kaybettiğini görebilmesi ve buna göre içeriklerini veya sunum yöntemlerini optimize edebilmesini sağlamaktır.

Eğitim videolarında öğrenci dikkatini ve katılımını analiz eden yapay zekâ destekli bir platform. Dört ana bileşenden oluşur:

* **Computer Vision Modülü**: Gerçek zamanlı dikkat takibi (MediaPipe, OpenCV, EasyOCR)
* **NLP Modülü (Gemini API)**: Yapay zekâ destekli sınıf analiz raporlama
* **Backend (FastAPI)**: API sunucusu
* **Frontend (Next.js)**: Kullanıcı arayüzü

## 📺[DEMO VİDEOSU İZLE (TIKLA).](https://drive.google.com/file/d/1dR9UlkWI5hdUMXJixfUeWgZC3cf_gshc/view?usp=sharing)

## [CANLI DEMO (TIKLA).](https://btk-hackathon-2025-edu-vision.vercel.app/)

---

## 📁 Proje Yapısı

```
BTK-HACKATHON-2025-EduVision/
├── computer-vision_integration/  # Gerçek zamanlı dikkat takibi (MediaPipe, OpenCV, EasyOCR)
├── EduVision_NLP/                # Gemini tabanlı NLP raporlama modülü
├── backend/                      # FastAPI backend sunucusu
├── Webapp/                       # Next.js frontend uygulaması (daha önce 'app' idi)
├── Dockerfile                    # Docker yapılandırma dosyası
├── schema.sql                    # Veritabanı şema tanımı
├── schema-diagram.png            # Veritabanı şeması diyagramı
├── README.md                     # Ana proje dökümantasyonu
└── .env, .gitignore, .dockerignore vb. dosyalar
```

---

## 🔧 Gereksinimler

* **Node.js** (sürüm 18 veya üstü)
* **Python** (sürüm 3.8 veya üstü)
* **npm** veya **yarn**
* **pip**

---

## ⚙️ Kurulum

### 1. Computer Vision Modülü

```bash
cd computer_vision_integration
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. NLP Modülü (Gemini API)

```bash
cd EduVision_NLP
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

`.env`, `data/`, `logs/` ve `reports/` klasörlerini oluşturmayı unutmayın:

```bash
mkdir data logs reports
```

`.env` içine aşağıdakini ekleyin:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Frontend (Next.js)

```bash
cd Webapp
npm install
```

---

## ▶️ Uygulamayı Çalıştırma

### 1. Computer Vision Takibi

**Video ile çalıştır:**

```bash
python frame_processor.py --video_path test-data/test_video.mp4 --output_csv output.csv
```

**Webcam ile çalıştır:**

```bash
python frame_processor.py --video_path "" --output_csv live_log.csv
```

### 2. NLP Modülü ile CSV İşleme ve Raporlama

```bash
cd EduVision_NLP
python main.py --csv_path data/student_attention_log.csv --course_name "Matematik 101" --language "tr"
```

### 3. Backend

```bash
cd backend
source venv/bin/activate
python app/main.py
```

* API URL: `${NEXT_PUBLIC_API_URL}`
* Dökümantasyon: `${NEXT_PUBLIC_API_URL}/docs`

### 4. Frontend

```bash
cd Webapp
npm run dev
```

Uygulama açılacak: `http://localhost:3000`

---

## 🚀 Özellikler

* 🎥 Video yükleme ve analiz
* 👁 Gaze takibi ve baş pozu tahmini
* 🧠 Yapay zekâ ile dikkat değerlendirmesi (Gemini)
* 📈 JSON & CSV rapor üretimi
* 🔄 Gerçek zamanlı analiz güncellemeleri
* 🗃 Önceki analiz geçmişi ve eşleşen yüz-foto verisi

---

## 📄 CV Modülü Çıktıları

Her çalışma sonunda CSV raporu üretilir:

| Sütun                  | Açıklama                        |
| ---------------------- | ------------------------------- |
| student\_id            | Yüz için benzersiz kimlik       |
| timestamp              | ISO formatında zaman damgası    |
| frame\_idx             | Video karesi numarası           |
| attention\_status      | Dikkatli / Dikkatsiz            |
| gaze                   | Sol / Orta / Sağ / Bilinmiyor   |
| yaw\_angle\_deg        | Başın sağa/sola dönüş açısı     |
| attention\_score       | Toplam dikkat yüzdesi           |
| distraction\_events    | Dikkat kaybı sayısı             |
| yawning\_count         | (YAKINDA) Esneme tespiti        |
| eye\_closure\_duration | (YAKINDA) Göz kapanma süresi    |
| focus\_quality         | (GELİŞECEK) Odak kalitesi       |
| session\_duration\_min | İlk kareden itibaren geçen süre |

Ek olarak, `photo_id/` klasörüne yüz görselleri ve `id_name_mapping.json` dosyasına kimlik-ad eşlemeleri kaydedilir.

---

## 🧱 Teknoloji Yığını

**Computer Vision**:

* OpenCV
* MediaPipe
* EasyOCR
* NumPy, math, custom gaze algoritmaları

**NLP Modülü**:

* Gemini API (sınıf raporu üretimi)
* Prompt yönetimi
* CSV/JSON dönüştürme ve formatlama

**Backend**:

* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic

**Frontend**:

* Next.js 13
* TypeScript
* Tailwind CSS
* Radix UI
* Framer Motion

---

## 🔌 API Uç Noktaları

* `GET /` – Sağlık kontrolü
* `POST /api/upload` – Video yüklemesi
* `GET /api/report/{report_id}` – Rapor görüntüleme
* `GET /api/reports` – Rapor listesi
* `GET /api/processing/{report_id}` – İşlenme durumu

---

## 🛠️ Sorun Giderme

* **Python sürümü**: MediaPipe için 3.10 veya 3.11 kullanın
* **OCR yavaşsa**: `ocr_photo.py` içinde `gpu=True` yaparak GPU'yu etkinleştirin
* **CORS hataları**: `backend/app/main.py` dosyasındaki izinleri kontrol edin
* **Yüz tanıma eksikse**: Işıklandırmayı artırın veya çözünürlük ayarlarını kontrol edin

---

## 🤝 Katkıda Bulunma

1. Repositoriesi forkladıktan sonra
2. Yeni bir branch oluşturun
3. Değişikliklerinizi yapın
4. Test edip pull request gönderin

---

## 👥 Katkıda Bulunanlar

* **Muhammed Erbay**
* **Enes Halit**
* **Osama Elbagory**

----

## 📄 Lisans

Bu proje **MIT Lisansı** ile lisanslanmıştır.
