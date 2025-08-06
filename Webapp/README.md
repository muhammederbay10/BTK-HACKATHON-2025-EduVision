# EduVision - Dikkat Takip Platformu

Eğitim videolarında öğrenci dikkatini ve katılımını analiz eden yapay zekâ destekli bir platform.

---

## 📁 Proje Yapısı

```
project/
├── app/            # Next.js frontend uygulaması
├── backend/        # FastAPI backend sunucusu
├── components/     # React bileşenleri
├── lib/            # Yardımcı fonksiyonlar
└── hooks/          # Özel React hook'ları
```

---

## 🔧 Gereksinimler

* **Node.js** (sürüm 18 veya üstü)
* **Python** (sürüm 3.8 veya üstü)
* **npm** veya **yarn**

---

## ⚙️ Kurulum ve Başlatma

### 1. Frontend Kurulumu (Next.js)

Proje kök dizinine gidip bağımlılıkları yükleyin:

```bash
cd /path/to/project
npm install
```

### 2. Backend Kurulumu (Python/FastAPI)

Backend klasörüne geçip sanal ortam oluşturun:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Python bağımlılıklarını yükleyin:

```bash
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy python-multipart pydantic
```

---

## ▶️ Uygulamayı Çalıştırma

### 1. Backend Sunucusunu Başlatın

`backend` klasöründen (sanal ortam aktifken):

```bash
cd backend
source venv/bin/activate
python app/main.py
```
The backend API will be available at: `${NEXT_PUBLIC_API_URL}`
- API documentation: `${NEXT_PUBLIC_API_URL}/docs`

### 2. Frontend Sunucusunu Başlatın

Proje kök dizininden:

```bash
npm run dev
```

* Frontend: `http://localhost:3000`

---

## 🚀 Özellikler

* 🎥 **Video Yükleme**: Eğitim videolarını yükleyin
* 👁 **Dikkat Takibi**: Öğrenci dikkatini yapay zekâ ile analiz eder
* 🔄 **Gerçek Zamanlı İşleme**: Canlı ilerleme takibi
* 📊 **Detaylı Raporlar**: Kapsamlı analizler ve öneriler
* 🗂 **Geçmiş Yönetimi**: Önceki analizlere erişim

---

## 📡 API Uç Noktaları

* `GET /` – Sağlık kontrolü
* `POST /api/upload` – Video yüklemesi
* `GET /api/report/{report_id}` – Raporu görüntüle
* `GET /api/reports` – Tüm raporları listele
* `GET /api/processing/{report_id}` – İşlenme durumu

---

## 🧑‍💻 Geliştirme

### Frontend Geliştirme

```bash
npm run dev     # Geliştirme sunucusunu başlat
npm run build   # Üretim için derle
npm run start   # Üretim sunucusunu başlat
npm run lint    # ESLint çalıştır
```

### Backend Geliştirme

```bash
# Sanal ortam aktifken
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧱 Teknoloji Yığını

### Frontend

* **Next.js 13** – React framework
* **TypeScript** – Tür güvenliği
* **Tailwind CSS** – Stil düzeni
* **Radix UI** – Bileşen kütüphanesi
* **Framer Motion** – Animasyonlar

### Backend

* **FastAPI** – Python web framework
* **Uvicorn** – ASGI sunucusu
* **Pydantic** – Veri doğrulama
* **SQLAlchemy** – Veritabanı ORM

---

## 🛠️ Sorun Giderme

### Yaygın Sorunlar

1. **Port çakışması**: 3000 veya 8000 portları doluysa:

   * Frontend: `PORT=3001` ortam değişkeniyle çalıştırın
   * Backend: `app/main.py` içindeki portu değiştirin

2. **Python sanal ortamı**: Backend komutlarını çalıştırmadan önce sanal ortamı aktifleştirin:

   ```bash
   source backend/venv/bin/activate
   ```

3. **CORS issues**: The backend is configured to allow requests from `http://localhost:3000`. Update CORS settings in `backend/app/main.py` if using different ports.

## Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
