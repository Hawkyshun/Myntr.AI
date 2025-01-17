# Myntr.AI - Finansal Danışmanlık Platformu

> Mynt, İskandinav dillerinde "para" ya da "madeni para" anlamına gelir.

Myntr.AI, yapay zeka destekli finansal danışmanlık ve bilgi sağlama için geliştirilen bir platformdur. Bu platform, kullanıcılara finansal kavramları açıklama, yatırım stratejileri önerme ve piyasa trendlerini analiz etme gibi konularda destek olmayı amaçlamaktadır.

## Proje Hedefleri

- 🎯 Kullanıcıların finansal hedeflerine uygun stratejiler öneren bir yapay zeka modeli oluşturmak
- 📚 Finansal terimleri açıklayarak kavramların anlaşılmasını sağlamak
- 📊 Piyasa trendleri ve finansal raporları özütleyerek kolay anlaşılır bilgiler sunmak
- 💡 Risk toleransına göre kişiselleştirilmiş yatırım tavsiyeleri vermek
- 🌐 Dünya Bankası finansal verilerini kullanarak güncel piyasa analizleri sunmak

## Proje İçeriği

### Veri Seti ve Model
Myntr.AI modeli, geniş kapsamlı finansal veri setleri ile eğitilmiştir:

- **Finansal Analizler:**
  - Temel analiz ve teknik analiz yöntemleri
  - Risk yönetimi stratejileri
  
- **Yatırım Araçları:**
  - Hisse senetleri, kripto paralar, tahviller, emtialar
  - ETF'ler ve yatırım fonları
  
- **Finansal Kavramlar:**
  - Faiz oranları, enflasyon, arbitraj gibi temel terimler
  - Portföy yönetimi ve risk analizi

### Kullanıcı Sorularına Örnekler
- "Risk toleransı düşük biri için hangi yatırım araçları uygundur?"
- "Faiz oranlarının yükselmesi piyasayı nasıl etkiler?"
- "ETF ve hisse senedi arasındaki fark nedir?"

## Teknoloji Yığını

### Frontend
- React.js
- Tailwind CSS
- Heroicons
- Axios

### Backend
- FastAPI
- PyTorch
- Transformers
- Pandas
- yfinance

### AI/ML
- Custom trained financial model (myntr-ai-v0.1)
- HuggingFace Transformers
- Turkish BERT base model

## Kurulum

### Gereksinimler
- Python 3.8+
- Node.js 16+
- npm veya yarn

### Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Kurulumu
```bash
cd frontend
npm install
```

### Model Eğitimi (Opsiyonel)
```bash
cd backend
python train_model.py
```

## Çalıştırma

### Backend Sunucusu
```bash
cd backend
uvicorn main:app --reload
```
Backend API http://localhost:8000 adresinde çalışacaktır.

### Frontend Uygulaması
```bash
cd frontend
npm run dev
```
Frontend uygulaması http://localhost:5173 adresinde çalışacaktır.

## API Endpoints

### POST /analyze
Finansal soru analizi ve tavsiye endpoint'i.

Request:
```json
{
    "question": "Yatırım tavsiyesi alabilir miyim?",
    "risk_tolerance": "medium"
}
```

Response:
```json
{
    "answer": "...",
    "recommendations": ["...", "..."],
    "additional_info": {
        "suggested_allocation": {
            "Hisse Senedi": "40%",
            "Tahvil": "30%",
            "Nakit": "30%"
        }
    }
}
```

### GET /market-data/{symbol}
Hisse senedi verisi endpoint'i.

Response:
```json
{
    "symbol": "THYAO.IS",
    "current_price": 100.50,
    "company_name": "Türk Hava Yolları",
    "market_cap": 138000000000,
    "pe_ratio": 5.2
}
```

## Web Uygulaması Özellikleri

- 🎨 **Kullanıcı Dostu Arayüz:** Basit ve etkili bir tasarım ile finansal sorularınızı kolayca sorma imkânı
- 📊 **Grafik ve Raporlama:** Piyasa analizleri ve finansal tavsiyeler için görselleştirme desteği
- ⚡ **Gerçek Zamanlı Veri:** Anlık piyasa verilerinin entegrasyonu
- 🤖 **Yapay Zeka Destekli:** Kişiselleştirilmiş finansal danışmanlık
- 💬 **Sohbet Tabanlı:** Doğal dil işleme ile kolay iletişim

## Veri Kaynakları

- [Dünya Bankası Finansal Verileri](https://datasource.kapsarc.org/explore/dataset/worldbank-global-financial-development/)
- [Türkçe Finans Dataset](https://huggingface.co/datasets/yusufbaykaloglu/turkish-finance-dataset)
- [Yahoo Finance API](https://finance.yahoo.com/)

## Katkıda Bulunma

1. Bu repo'yu fork edin
2. Feature branch'i oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## İletişim

Sorularınız ve önerileriniz için furkanerdogan2300@gmail.com üzerinden iletişime geçebilirsiniz.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

