# Question-1

## Proje Özeti
Bu proje, kullanıcıların metinlerini girerek duygu analizini yapmalarını sağlayan bir web uygulaması sunmaktadır. Uygulama, kullanıcı yorumlarının olumlu ya da olumsuz duygu içerip içermediğini analiz eder. Uygulama, Naive Bayes makine öğrenmesi algoritması ile eğitilmiş bir model kullanarak çalışmaktadır. Uygulama, Streamlit ile geliştirilmiş, Docker ile konteynerize edilmiş ve AWS üzerinde canlıya alınmıştır.

-----

## Adım 1: Veri Kümesi ve Veri Ön İşleme
### Veri Kümesi:
Veri kümesi, her bir ürün yorumu için duygu etiketleri içeren bir CSV dosyasıdır. Veri kümesi utf-16 formatında depolanmıştır ve her bir yorumun duygu durumu ("Olumlu", "Olumsuz", "Tarafsız") etiketlenmiştir.
Bu veriye buradan erisebilirsiniz: https://www.kaggle.com/datasets/burhanbilenn/duygu-analizi-icin-urun-yorumlari

### Veri Ön İşleme:
Veri kümesindeki metin verileri, modelin doğru bir şekilde çalışabilmesi için aşağıdaki adımlarla işlenmiştir:

Her bir satırdaki veri, son virgülden önceki kısmı (yorum) ve sonrasındaki kısmı (durum) ayrılarak iki sütun olarak saklanmıştır.
"Tarafsız" etiketli veriler çıkarılmıştır.
Veri kümesi eğitim ve test verisi olarak %80 - %20 oranında ayrılmıştır.

-----

## Adım 2: Makine Öğrenmesi Modeli
Model Seçimi:
Makine öğrenmesi modelini oluşturmak için Naive Bayes algoritması seçilmiştir. Bu algoritma, metin sınıflandırma problemleri için oldukça etkili ve hızlı sonuçlar verir.

Model: Naive Bayes (MultinomialNB)
Kütüphane: sklearn
Modelin eğitimi için:

Vectorizer: CountVectorizer kullanarak metin verileri sayısal verilere dönüştürülmüştür.
Model Eğitimi: Eğitim verileriyle model eğitilmiş ve ardından kaydedilmiştir.
Modelin Kaydedilmesi:
Eğitilen model ve vectorizer dosyaları joblib kütüphanesi ile kaydedilmiştir. Kaydedilen dosyalar:

sentiment_model.pkl (Naive Bayes Modeli)
vectorizer.pkl (CountVectorizer)

-----

## Adım 3: Uygulama Geliştirme
Streamlit ile Web Uygulaması:
Web uygulaması, Streamlit kütüphanesi kullanılarak geliştirilmiştir. Kullanıcılar, ürün yorumlarını girerek uygulama üzerinden duygu analizi sonuçlarını görebilirler.

Projeyi baslatmak icin:
Conatainer'da
```bash
make rundocker
```
Sistem'de
```bash
make runlocal
```
Run local yapmadan once bir virtual environement acin ve requirements.txt'nin icindeki tum moduleleri indirin.


Model Yükleme: Eğer model dosyaları mevcutsa, model ve vectorizer yüklenir.

Modeli Eğitme: Eğer model yoksa, kullanıcı "Modeli Eğitin ve Kaydedin" butonuna tıklayarak modeli eğitebilir.

Duygu Analizi: Kullanıcı metin girerek "Duyguları Analiz Edin" butonuna tıklayarak duygu analizini alır. Sonuç olarak "Olumlu" veya "Olumsuz" olarak duygu tahmin edilir.

Görsel Gösterim: Duygu analizine göre uygun görsel (olumlu veya olumsuz) gösterilir.

Examlples:

![ScreenShot](/Assets/ok.png)

![ScreenShot](/Assets/ko.png)


Modeli Yükleme ve Eğitim:

```python
def train_and_save_model():
    df = get_data(f"{question}data/data.csv")
    test_df = df[df['Durum'] != 'Tarafsız']
    X = test_df['Gorus']
    y = test_df['Durum']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    
    nb_classifier = MultinomialNB()
    nb_classifier.fit(X_train_vec, y_train)
    
    joblib.dump(nb_classifier, f"{question}sentiment_model.pkl")
    joblib.dump(vectorizer, f"{question}vectorizer.pkl")
```

Duygu Tahmini:
```python

def predict_sentiment(text, model, vectorizer):
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    return prediction
```

-----

## Adım 4: Dockerize Etme

Docker Konteyneri:
Uygulama Docker kullanılarak konteynerize edilmiştir. Bu, uygulamanın bağımsız bir ortamda çalışmasını sağlamaktadır.

Dockerfile: Aşağıdaki Dockerfile ile gerekli bağımlılıklar kurulmuş ve uygulama çalıştırılmaya hazır hale getirilmiştir.

```dockerfile
FROM python:3.9

WORKDIR /

COPY . /Question-1/

RUN pip install uv

RUN uv pip install --system --no-cache-dir -r /Question-1/requirements.txt

RUN cd ..

EXPOSE 8501

CMD ["streamlit", "run", "/Question-1/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Burada uv modulunu ayaga kalkisi hizlandirmak icin kullaniyoruz.

-----

## Adım 5: Bulut Bilişimde Canlıya Alma
AWS ve Nginx ile Dağıtım:
Uygulama AWS üzerinde Docker konteyneri olarak çalıştırılmaya başlanmıştır. AWS EC2 instance üzerinde Docker kurularak, Nginx kullanılarak uygulamanın erişilebilirliği sağlanmıştır. Ayrıca, uygulama daha hızlı ve güvenli çalışabilmesi için Cloudflare ile yönlendirilmiştir.

AWS EC2 Kurulumu: EC2 instance üzerinde Docker kurulumları yapılmıştır.
Nginx Konfigürasyonu: Uygulamanın daha hızlı erişilmesi için Nginx reverse proxy olarak kullanılmıştır.

-----

## Adim 6: CloudFlare ile domain name linkleme
https://alpardayalman.com 'dan web uygulamasina gidebilirsiniz.

-----

## Adım 7: GitHub ve Dokümantasyon
GitHub Repo ve Dokümantasyon:
Proje kodları, gerekli açıklamalarla birlikte GitHub reposuna yüklenmiştir.
