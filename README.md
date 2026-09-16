# 🏦 Bank Churn Risk Dashboard

Bu proje, banka müşterilerinin bankayı terk etme (churn) riskini tahmin eden uçtan uca (end-to-end) bir makine öğrenmesi sistemidir. Klasik monolitik (tek dosya) yapıların aksine; proje **Docker** kullanılarak **FastAPI** (Arka Uç) ve **Streamlit** (Ön Uç) olmak üzere tam bağımsız mikroservisler (microservices) halinde tasarlanmıştır.

## 🚀 Mimari ve Öne Çıkan Özellikler

* **🐳 Dockerize Edilmiş Yapı:** Uygulama, `docker-compose` ile platform bağımsız olarak tek bir komutla ayağa kalkacak şekilde izole edilmiştir.
* **⚙️ FastAPI Backend:** Makine öğrenmesi modeli ve ağır **SHAP** (Açıklanabilir Yapay Zeka) hesaplamaları, arayüzü yormamak adına bağımsız bir API sunucusunda asenkron olarak çalışır.
* **🎨 Streamlit Frontend:** REST API ile haberleşen, hafifletilmiş ve kullanıcı dostu etkileşimli yönetim paneli.
* **🤖 Otonom AI Agent:** API'den dönen müşteri risk seviyesi ve bakiyesine göre otonom pazarlama aksiyonları (VIP elde tutma, SMS kampanyası, çapraz satış) üreten kural tabanlı asistan.
* **🧪 What-If Simulator & Batch Analysis:** Tekil müşteri senaryolarını simüle etme ve toplu müşteri CSV'lerini işleyerek finansal kayıp riskine göre sıralama yeteneği.

## 🛠️ Kullanılan Teknolojiler

* **Arka Uç (Backend):** FastAPI, Uvicorn, Pydantic
* **Ön Uç (Frontend):** Streamlit, Plotly
* **Makine Öğrenmesi & XAI:** XGBoost, Scikit-Learn, SHAP, Pandas, NumPy
* **Orkestrasyon (DevOps):** Docker, Docker Compose

## 🔌 API Endpoint'leri (FastAPI)

Backend servisi `http://localhost:8000` portunda çalışır ve aşağıdaki endpoint'leri sunar:

* `POST /predict`: JSON formatında müşteri verilerini alır; churn tahminini, olasılık yüzdesini ve özellik bazlı SHAP değerlerini döndürür.
* `GET /model_info`: Arayüzdeki Sürücü Analizi (Driver Analysis) grafiği için modelin genel özellik önem (feature importance) katsayılarını döndürür.

## 💻 Kurulum ve Çalıştırma (Docker ile)

Projeyi kendi bilgisayarınızda çalıştırmak için bilgisayarınızda **Docker** ve **Docker Desktop**'ın kurulu ve açık olması yeterlidir.

**Adım 1: Yönetici Şifrelerini Ayarlayın**
Frontend servisinin giriş ekranını geçebilmek için `frontend` klasörünün içine `.streamlit` adında yeni bir klasör açın. İçine `secrets.toml` adında bir dosya oluşturup şu kodları yapıştırın:
```toml
[auth]
username = "admin"
password = "123"
```
**Adım 2: Sistemi Ayağa Kaldırın**
Terminalinizi projenin ana dizininde `(docker-compose.yml dosyasının olduğu yerde)` açın ve şu komutu çalıştırın:
```docker-compose up --build```

**Adım 3: Uygulamaya Erişin**
Konteynerler başarıyla oluştuktan sonra tarayıcınızdan aşağıdaki adreslere gidebilirsiniz:
* 🖥️ Yönetici Paneli (Streamlit): http://localhost:8501
* ⚙️ API Dokümantasyonu (Swagger UI): http://localhost:8000/docs