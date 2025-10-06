"""
Insider kariyer testleri için test verileri.

Bu modül test senaryolarında kullanılacak tüm test verilerini,
arama kriterlerini, URL'leri ve konfigürasyonları içerir.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class JobSearchCriteria:
    """
    İş arama kriterleri için veri sınıfı.
    
    Bu sınıf iş arama testlerinde kullanılacak departman,
    lokasyon ve beklenen anahtar kelimeleri tutar.
    """

    department: str  # Aranacak departman (örn: "Quality Assurance")
    location: str    # Aranacak lokasyon (örn: "Istanbul, Turkey")
    expected_keywords: List[str]  # Beklenen anahtar kelimeler


@dataclass
class TestUser:
    """
    Test kullanıcı bilgileri için veri sınıfı.
    
    Form doldurma testlerinde kullanılacak kullanıcı
    bilgilerini tutar.
    """

    name: str   # Kullanıcı adı
    email: str  # E-posta adresi
    phone: str  # Telefon numarası


class TestData:
    """
    Tüm test verileri için konteyner sınıfı.
    
    Bu sınıf projedeki tüm test verilerini merkezi olarak
    yönetir ve test sınıflarına kolay erişim sağlar.
    """

    # ==================== İŞ ARAMA TEST VERİLERİ ====================
    
    # İstanbul QA işleri için arama kriterleri
    QA_JOBS_ISTANBUL = JobSearchCriteria(
        department="Quality Assurance",
        location="Istanbul, Turkey",
        expected_keywords=["quality", "assurance", "qa", "test"],
    )

    # Ankara QA işleri için arama kriterleri
    QA_JOBS_ANKARA = JobSearchCriteria(
        department="Quality Assurance",
        location="Ankara, Turkey",
        expected_keywords=["quality", "assurance", "qa", "test"],
    )

    # ==================== URL'LER ====================
    
    # Test edilecek sayfaların URL'leri
    URLS = {
        "home": "https://useinsider.com/",
        "careers": "https://useinsider.com/careers/",
        "qa_careers": "https://useinsider.com/careers/quality-assurance/",
        "open_positions": "https://useinsider.com/careers/open-positions/",
    }

    # ==================== BEKLENEN SAYFA ELEMENTLERİ ====================
    
    # Kariyer sayfasında bulunması gereken bölümler
    EXPECTED_CAREER_SECTIONS = ["locations", "teams", "life at insider"]

    # ==================== TEST KULLANICILARI ====================
    
    # Test kullanıcı verileri (placeholder data)
    TEST_USERS = {
        "default": TestUser(
            name="Test Kullanıcısı", 
            email="test@example.com", 
            phone="+90 555 123 4567"
        )
    }

    # ==================== BROWSER KONFİGÜRASYONLARI ====================
    
    # Parametrize edilmiş testler için browser seçenekleri
    BROWSERS = ["chrome", "firefox"]

    # ==================== TIMEOUT KONFİGÜRASYONLARI ====================
    
    # Farklı bekleme süreleri için timeout değerleri
    TIMEOUTS = {
        "short": 5,    # Kısa bekleme (5 saniye)
        "medium": 10,  # Orta bekleme (10 saniye)
        "long": 30     # Uzun bekleme (30 saniye)
    }
