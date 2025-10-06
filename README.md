# Insider Test Automation Project

Bu proje, Insider kariyer portalının otomatik testleri için geliştirilmiştir. Python, Selenium WebDriver ve Page Object Model (POM) design pattern kullanılarak oluşturulmuştur.

Projenin geliştirmesi Fedora Linux üzerinde yapıldığı için ve test edileceği makine bilinmediği için Webdriver-manager kullanıldı. 

##  Test Senaryosu

Bu test aşağıdaki adımları otomatik olarak gerçekleştirir:

1. **Ana Sayfa Kontrolü**: https://useinsider.com/ sayfasının açılıp açılmadığını kontrol eder
2. **Navigasyon**: "Company" menüsünden "Careers" seçer ve Career sayfasının Locations, Teams, Life at Insider bölümlerini kontrol eder
3. **QA İş İlanları**: Quality Assurance sayfasına gider, "See all QA jobs" butonuna tıklar
4. **Filtreleme**: İş ilanlarını "Istanbul, Turkey" lokasyonu ve "Quality Assurance" departmanı ile filtreler
5. **Doğrulama**: Tüm iş ilanlarının Position, Department ve Location bilgilerini kontrol eder
6. **Lever Sayfası**: "View Role" butonuna tıklayarak Lever Application form sayfasına yönlendirildiğini kontrol eder

## 🛠️ Kurulum

### Gereksinimler
- Python 3.8+
- Chrome veya Firefox browser
- Make (Makefile komutları için - opsiyonel)

### 1. Projeyi indirin
```bash
git clone https://github.com/rfatihkocademir/insider_automation_project.git
cd insider-test-automation
```

### 2. Virtual environment oluşturun
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Bağımlılıkları yükleyin
```bash
pip install -r requirements.txt
```

### 4. Environment dosyasını oluşturun
```bash
cp .env.example .env
```

### 5. Make kurulumu (Makefile komutları için - opsiyonel)

**Ubuntu/Debian:**
```bash
sudo apt-get install make
```

**CentOS/RHEL:**
```bash
sudo yum install make
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
- Git Bash kullanın veya
- MinGW/MSYS2 ile `mingw32-make` kurun

## 🚀 Testleri Çalıştırma

### Temel Kullanım

```bash
# Chrome ile test çalıştırma (varsayılan)
pytest tests/test_insider_careers.py -v

# Firefox ile test çalıştırma
pytest tests/test_insider_careers.py -v --browser=firefox

# HTML raporu ile
pytest tests/test_insider_careers.py -v --html=reports/report.html --self-contained-html
```

### Makefile ile (Make kurulu ise)

**İlk kurulum:**
```bash
# Tüm kurulumu otomatik yap
make setup

# Veya adım adım:
make install      # Bağımlılıkları yükle
make setup-env    # .env ve klasörleri oluştur
```

**Test çalıştırma:**
```bash
# Tüm testleri çalıştır
make test

# HTML raporu ile
make test-html

# Chrome ile
make test-chrome

# Firefox ile
make test-firefox

# Temizlik
make clean

# Yardım
make help
```

## 📁 Proje Yapısı

```
├── config/                 # Konfigürasyon dosyaları
├── pages/                  # Page Object sınıfları
│   ├── base_page.py        # Temel sayfa sınıfı
│   ├── home_page.py        # Ana sayfa
│   ├── careers_page.py     # Kariyer sayfası
│   ├── quality_assurance_page.py
│   ├── open_positions_page.py
│   └── job_detail_page.py
├── tests/                  # Test dosyaları
│   ├── test_data.py        # Test verileri
│   └── test_insider_careers.py  # Ana test dosyası
├── utils/                  # Yardımcı araçlar
├── screenshots/            # Hata durumunda ekran görüntüleri
├── logs/                   # Log dosyaları
├── reports/                # Test raporları
├── conftest.py            # Pytest konfigürasyonu
├── pytest.ini            # Pytest ayarları
├── requirements.txt       # Python bağımlılıkları
└── README.md
```

## 🔧 Konfigürasyon

`.env` dosyasında aşağıdaki ayarları yapabilirsiniz:

```bash
# Browser seçimi (chrome/firefox)
BROWSER=chrome

# Headless mode (true/false)
HEADLESS=false

# Timeout ayarları
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Screenshot alma (true/false)
SCREENSHOT_ON_FAILURE=true
```

## 📊 Raporlar

- **HTML Raporu**: `reports/report.html` dosyasında detaylı test sonuçları
- **Screenshot'lar**: Test başarısız olduğunda `screenshots/` klasöründe otomatik ekran görüntüsü
- **Log Dosyaları**: `logs/test.log` dosyasında detaylı log kayıtları

## 🎯 Özellikler

- ✅ **Page Object Model (POM)** design pattern
- ✅ **Cross-browser testing** (Chrome/Firefox)
- ✅ **Otomatik screenshot** alma (test başarısızlığında)
- ✅ **HTML raporlama**
- ✅ **Parametrik browser seçimi**
- ✅ **Retry mekanizması**
- ✅ **Structured logging**

Test, aşağıdaki teknolojileri kullanır:
- **Python 3.8+**
- **Selenium WebDriver 4.15.2**
- **Pytest 7.4.3**
- **Page Object Model Pattern**
- **Automatic WebDriver Management**
