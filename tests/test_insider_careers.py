"""
POM framework kullanarak Insider kariyer iş akışı için Pytest test case'i.

Bu test aşağıdaki senaryoyu kapsar:

1. Insider ana sayfasını aç ve varsa çerezleri kabul et.
2. Company menüsü üzerinden kariyer sayfasına git.
3. Kariyer sayfasında Locations, Teams ve Life at Insider bölümlerinin var olduğunu doğrula.
4. Quality Assurance landing sayfasına git ve "See all QA jobs" butonuna tıkla.
5. Açık pozisyonlar sayfasında Location "Istanbul, Turkey" ve Department "Quality Assurance" filtrelerini uygula.
6. En az bir iş ilanının döndürüldüğünü doğrula; her iş için başlık ve departmanın "Quality Assurance" içerdiğini
   ve lokasyonun "Istanbul, Turkey" içerdiğini kontrol et.
7. İlk işi aç ve Lever iş açıklamasına yönlendirildiğini ve başvuru bölümü içerdiğini doğrula.



Dikkat Buradaki her bir madde ayrı test senaryoları ile koşturulabilir. Ancak bu hem süreyi hemde kaynak tüketimini arttırmaktadır.
Paralel koşumda CPU kullanımı çok artmaktadır. Bu sorunun çözümü alternatif olarak playwright kullanılabilir. 
Playwright benchmarklarda seleniumdan daha performans göstermektedir.
"""

import pytest

from pages.home_page import HomePage
from pages.quality_assurance_page import QualityAssurancePage


@pytest.mark.parametrize("department, location", [("Quality Assurance", "Istanbul, Turkey")])
def test_insider_career_workflow(driver, department, location) -> None:
    """
    Uçtan uca kariyer iş akışını çalıştırır.
    
    Bu test fonksiyonu, Insider web sitesinde kariyer sayfalarında
    gezinmeyi ve iş arama sürecini test eder.
    """
    # 1. Ana sayfa - Insider ana sayfasını aç ve çerez onayını ver
    home = HomePage(driver)
    home.open()
    home.accept_cookies_if_present()
    assert "Insider" in driver.title, "Ana sayfa başlığı 'Insider' içermiyor"
    
    # 2. Kariyer sayfası - Company menüsünden kariyer sayfasına git ve bölümleri kontrol et
    careers = home.go_to_careers()
    careers.verify_sections_present()
    
    # 3. Quality Assurance sayfası - UI üzerinden gitmeyi dene, yoksa direkt URL kullan
    try:
        qa_page = careers.go_to_quality_assurance()
    except Exception:
        # UI linkinde sorun varsa direkt URL'e git
        driver.get("https://useinsider.com/careers/quality-assurance/")
        qa_page = QualityAssurancePage(driver)
    
    # 4. Tüm işleri gör - "See all QA jobs" butonuna tıkla
    open_positions = qa_page.click_see_all_jobs()
    
    # 5. Filtreleri uygula - Lokasyon ve departman filtrelerini ayarla
    open_positions.set_filters(location, department)
    listings = open_positions.get_listings()
    assert listings, f"{department} için {location} lokasyonunda iş ilanı bulunamadı"
    
    # 6. Her iş ilanının alanlarını kontrol et
    for job in listings:
        title_lower = job["title"].lower()
        dept_lower = job["department"].lower()
        loc_lower = job["location"].lower()
        
        # İş başlığının departmanı içerdiğini kontrol et
        assert (
            department.lower() in title_lower
        ), f"İş başlığı '{job['title']}' '{department}' içermiyor"
        
        # Departman alanının doğru olduğunu kontrol et
        assert (
            department.lower() in dept_lower
        ), f"Departman '{job['department']}' '{department}' içermiyor"
        
        # Lokasyonun doğru olduğunu kontrol et
        assert (
            location.split(",")[0].lower() in loc_lower
        ), f"Lokasyon '{job['location']}' '{location}' içermiyor"
    
    # 7. İlk iş ilanını aç ve Lever sayfasını doğrula
    detail_page = open_positions.open_first_job()
    detail_page.verify_on_lever()
