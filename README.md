# SkillSwap - Yetenek Takası ve Öğrenme Ağı Platformu

SkillSwap, kullanıcıların sahip oldukları bilgi ve yetenekleri sergileyip başkalarına öğretebildikleri ve karşılığında herhangi bir para ödemeden yeni yetenekler öğrenebildikleri modern bir **"Yetenek Takası ve Öğrenme Ağı"** web platformudur.

---

## 🌟 Öne Çıkan Özellikler

1. **Çekirdek Sistem (Core App):**
   - Tailwind CSS (CDN) ile modern, duyarlı (responsive) ve şık arayüz tasarımı.
   - Tanıtıcı Hero Bölümü, platform istatistikleri ve sisteme en son eklenen 6 yetenek ilanının yer aldığı dinamik vitrin.
   - Global Navbar, kategoriler menüsü, flash mesaj kutuları ve Footer.

2. **Gelişmiş Kullanıcı Yönetimi (Users App):**
   - `AbstractUser` tabanlı `CustomUser` modeli: Biyografi (`bio`), profil görseli (`avatar`), şehir/konum (`location`).
   - Avatar yüklenmediğinde dinamik baş harf görseli sağlayan UI-Avatars entegrasyonu.
   - Kayıt Olma (Register), Giriş Yapma (Login) ve Güvenli Çıkış (Logout).
   - **Kullanıcı Paneli (Dashboard):**
     - Kullanıcı istatistikleri (Aktif ilan sayısı, gelen/giden teklifler, kabul edilen takaslar).
     - Gelen takas tekliflerini anında inceleme, kabul etme veya reddetme.
     - Kendi ilanlarını düzenleme ve silme.
     - Başkalarına gönderilen tekliflerin durumunu takip etme.

3. **Yetenek İlanları (Listings App):**
   - **Kategori Sistemi (Category):** Otomatik slug üretimi ve kategoriye göre gruplandırma.
   - **Yetenek İlanı (SkillListing):** Başlık, detaylı açıklama, kategori, ilan sahibi, zorluk seviyesi (Başlangıç, Orta, İleri) ve tarih bilgileri.
   - Filtreleme ve Arama: Metin araması, kategoriye ve zorluk seviyesine göre canlı filtreleme.
   - Sayfalama (Pagination): Sayfa geçişlerinde arama ve filtre parametrelerini koruyan sayfalama yapısı.
   - İlan Detay Sayfası: Eğitmen kartı, benzer kategori ilanları ve interaktif takas formu.

4. **Takas Sistemi (Swaps App):**
   - **Takas Talebi (SwapRequest):** Kullanıcıların ilgilendikleri ilana özel takas mesajı ve sunabilecekleri yeteneği ilettikleri model.
   - Durum Yönetimi: `Pending` (Beklemede), `Accepted` (Kabul Edildi), `Rejected` (Reddedildi).
   - İlan sahibi profiline girerek gelen teklifleri tek tıkla **Kabul** veya **Reddet** yapabilir.
   - Teklif kabul edildiğinde tarafların e-posta adresleri karşılıklı olarak görünür hale gelir.

5. **Django Admin Paneli:**
   - `CustomUser`, `Category`, `SkillListing`, ve `SwapRequest` modelleri için özelleştirilmiş `list_display`, `search_fields`, `list_filter` ve `date_hierarchy` yapılandırmaları.

---

## 📁 Proje Dosya Yapısı

```
SkillSwap/
├── manage.py
├── requirements.txt
├── README.md
├── skillswap/                     # Proje Ana Ayar Paketi
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                          # Çekirdek Uygulama (Home & Base)
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── users/                         # Kullanıcı Yönetimi & Dashboard
│   ├── apps.py
│   ├── models.py                  # CustomUser
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   └── admin.py
├── listings/                      # Yetenek İlanları & Kategoriler
│   ├── apps.py
│   ├── models.py                  # Category & SkillListing
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   ├── admin.py
│   ├── context_processors.py
│   └── management/
│       └── commands/
│           └── seed_data.py       # Örnek Veri Yükleme Komutu
├── swaps/                         # Takas & Teklif Mekanizması
│   ├── apps.py
│   ├── models.py                  # SwapRequest
│   ├── forms.py
│   ├── urls.py
│   ├── views.py
│   └── admin.py
├── templates/                     # Tailwind CSS HTML Şablonları
│   ├── base.html                  # Global Layout
│   ├── core/
│   │   └── home.html
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html           # Kullanıcı Dashboard
│   │   └── profile_edit.html
│   └── listings/
│       ├── listing_list.html
│       ├── listing_detail.html
│       ├── listing_form.html
│       └── listing_confirm_delete.html
└── static/
    └── css/
        └── styles.css
```

---

## 🚀 Kurulum ve Çalıştırma Adımları

### 1. Sanal Ortam Oluşturma ve Aktifleştirme
Terminal veya PowerShell üzerinden proje klasörüne gidin:

```bash
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktifleştirin:
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# macOS / Linux:
source venv/bin/activate
```

### 2. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 3. Veritabanı Migrasyonlarını Çalıştırma
```bash
python manage.py makemigrations users listings swaps core
python manage.py migrate
```

### 4. Örnek Verileri (Seed Data) Yükleme
Platformun hemen dolu ve test edilebilir gelmesi için hazır komutu çalıştırın:
```bash
python manage.py seed_data
```
Bu komut sisteminize:
- **Admin Kullanıcısı:** `admin` / `admin123`
- **Demo Eğitmenler & Öğrenciler:** `ahmet_dev`, `ayse_design`, `mehmet_guitar`, `elif_english` (Şifreleri: `password123`)
- **6 Popüler Kategori** (Yazılım, Yabancı Dil, Tasarım, Müzik, Dijital Pazarlama, Fotoğrafçılık)
- **6 Zengin Yetenek İlanı**
- **Örnek Takas Teklifleri** (Bekleyen ve Kabul edilen)
otomatik olarak ekler.

### 5. Geliştirme Sunucusunu Başlatma
```bash
python manage.py runserver
```

Tarayıcınızda açın:
- **Web Sitesi:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Paneli:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
