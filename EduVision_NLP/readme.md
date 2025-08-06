# EduVision\_NLP

**EduVision\_NLP**, sınıf ortamındaki öğrenci dikkat verilerini analiz etmek için tasarlanmış Python tabanlı bir modüldür. Ham CSV verilerini, sınıf dinamikleri, bireysel öğrenci katılımı ve iyileştirme için yapay zekâ destekli öneriler içeren ayrıntılı, yapılandırılmış raporlara dönüştürür.

---

## 📁 Klasör Yapısı

```
EduVision_NLP/
│
├── .env                     # Ortam değişkenleri (ör. API anahtarları)
├── .gitignore               # Versiyon kontrolünde yok sayılacak dosyalar
├── config.py                # Ayarlar ve API anahtarları konfigürasyonu
├── main.py                  # Ana script (CSV işle ve rapor üret)
│
├── data/                    # Girdi CSV dosyaları (lokalde oluşturulmalı)
│   ├── student_attention_log.csv
│   └── student_attention_log2.csv
│
├── logs/                    # İşlem günlükleri (lokalde oluşturulmalı)
│   └── eduvision.log
│
├── models/                  # Yapay zekâ model entegrasyonu
│   └── gemini.py
│
├── prompts/                 # Yapay zekâya yönelik prompt şablonları
│   └── report_prompt.py
│
├── reports/                 # Üretilen raporlar (lokalde oluşturulmalı)
│   ├── classroom_*.json
│   └── processing_summary_*.json
│
├── utils/                   # Yardımcı modüller
│   ├── csv_loader.py        # CSV yükleyici ve doğrulayıcı
│   └── formatter.py         # JSON rapor biçimlendirici
│
└── requirements.txt         # Proje bağımlılıkları
```

---

## ⚙️ Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/your-repository/EduVision_NLP.git
cd EduVision_NLP
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin

```bash
python -m venv venv

# Windows için:
venv\Scripts\activate

# MacOS/Linux için:
source venv/bin/activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarlayın

Proje kök dizininde `.env` adında bir dosya oluşturun ve aşağıdakini ekleyin:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Yerel Klasörleri Oluşturun

Aşağıdaki klasörler yalnızca yerel ortamda kullanılır ve manuel olarak oluşturulmalıdır:

```bash
mkdir data logs reports
```

`.env` dosyasını da elle oluşturmalısınız.

---

## 🚀 Kullanım

### 1. CSV Dosyasını Doğrulama

```bash
python main.py --csv_path "data/student_attention_log.csv" --course_name "Deneme Matematik 101" --language "tr"
```

### 2. CSV İşle ve Rapor Oluştur

```bash
python main.py --csv_path "data/student_attention_log.csv" --course_name "Matematik 101" --language "tr"
```

### 3. Logları Görüntüleme

Tüm işlem adımları `logs/eduvision.log` dosyasına kaydedilir.

---

## 📄 Çıktı

İşlem sonunda `reports/` klasörüne JSON raporları kaydedilir:

* `classroom_<ders>_<dil>_<timestamp>.json`: Ayrıntılı sınıf raporu.
* `processing_summary_<timestamp>.json`: Tüm işlenen derslerin özeti.

---

## ✨ Özellikler

### ✅ CSV Doğrulama

* Gerekli sütunların (`student_id`, `timestamp`, `attention_status`, vb.) varlığını kontrol eder.
* Eksik veya bozuk verileri loglar.

### 🤖 Yapay Zekâ Analizi

* Gemini API üzerinden sınıf etkileşimlerini analiz eder.
* Dikkat dağılımı, odak süreleri ve öğrencilerin performansı yükseltmek için öneriler sunar.

### 📊 JSON Rapor Üretimi

* Yapılandırılmış ve makine tarafından okunabilir raporlar oluşturur.
* Zaman aralıklarına göre analiz ve öğrenci bazlı özetler içerir.

### 🪵 Kapsamlı Loglama

* Tüm işlem adımları `logs/eduvision.log` dosyasına kaydedilir.

---

## 📂 Klasör Açıklamaları

| Klasör     | Açıklama                                                                        |
| ---------- | ------------------------------------------------------------------------------- |
| `data/`    | Öğrenci dikkat verilerini içeren CSV dosyaları **(lokal olarak oluşturulmalı)** |
| `logs/`    | İşlem günlüklerini içerir **(lokal olarak oluşturulmalı)**                      |
| `models/`  | Gemini AI modeli ile entegrasyon                                                |
| `prompts/` | AI'ya gönderilen prompt şablonları                                              |
| `reports/` | Üretilmiş JSON raporları **(lokal olarak oluşturulmalı)**                       |
| `utils/`   | Veri işleme ve formatlama yardımcıları                                          |

---

## 🛠️ Sorun Giderme

| Sorun                    | Çözüm                                                 |
| ------------------------ | ----------------------------------------------------- |
| **Eksik bağımlılıklar**  | `pip install -r requirements.txt` komutunu çalıştırın |
| **API anahtarı eksik**   | `.env` dosyasına `GEMINI_API_KEY` değerini ekleyin    |
| **CSV formatı hatalı**   | Gerekli sütunların mevcut olduğundan emin olun        |
| **Hata mı alıyorsunuz?** | `logs/eduvision.log` dosyasını kontrol edin           |

---

## 📌 Notlar

* **Performans:** Büyük CSV dosyalarında Gemini API’nin yanıt süresi uzayabilir.
* **Ölçeklenebilirlik:** Binlerce satır veri işleyebilir.
* **Özelleştirme:** `prompts/report_prompt.py` dosyasını değiştirerek rapor şablonlarını düzenleyebilirsiniz.
