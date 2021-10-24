###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################
#############################################
# RFM NEDİR?
##############################################

# RFM analizi, pazarlama çalışmalarınıza cevap vermesini beklediğiniz hedef müşteri kitlenizi belirlemek için kullanılan popüler bir analiz yöntemidir.
# Bu analiz yönteminde müşterinin geçmiş alışveriş alışkanlıklarının yanı sıra, yaptıkları alışveriş sayısına ve bu alışverişlerin harcama miktarına bağlı olarak müşterilerin muhtemel satın alma eğilimlerinin belirlenmesi amaçlanır.
# RFM analizine başlarken müşterilerimizi yenilik (R), sıklık (F) ve parasal (M) değer dağılımlarına göre gruplara ayırmaktayız.
# Bu 3 ana değişkenle birlikte yalnızca 4 müşteri bilgisiyle dahi 64 (4x4x4) farklı müşteri segmenti oluşturabilmekteyiz.

##############################################
# RFM AÇILIMI
##############################################

# Recency – Yenilik (R) – Son satım alımdan bugüne kadar geçen süredir.
# Frequency – Sıklık (F) – Toplam satın alım sayısıdır.
# Monetary – Parasallık (M) – Tüm satın alımların parasal toplamıdır.

##############################################
# RFM ANALİZİ FAYDALARI
##############################################

# Yanıt oranlarında artış,
# Dönüşüm oranlarında artış,
# Hedefleme üzerinden gerçekleştirilen dijital pazarlama çalışmalarından elde edilen gelirde artış.

##############################################
# DEĞİŞKENLER
##############################################

# InvoiceNo: Fatura numarası. Nominal. Her işleme benzersiz şe-kilde atanan 6 basamaklı bir integral numarası. Bu kod 'c' harfiy-le başlıyorsa, bir iptal olduğunu gösterir.
# StockCode: Ürün (öğe) kodu. Nominal. Her farklı ürüne benzersiz şekilde atanmış 5 basamaklı bir integral numarası.
# Description: Ürün (öğe) adı. Nominal.
# Quantity: İşlem başına her bir ürünün (kalem) miktarı. Sayısal.
# InvoiceDate: Fatura tarihi ve saati. Sayısal. Bir işlemin oluşturulduğu gün ve saat.
# UnitPrice: Birim fiyatı. Sayısal. Birim başına ürün fiyatı (£).
# CustomerID: Müşteri numarası. Nominal. Her müşteriye benzersiz şekilde atanmış 5 basamaklı bir integral numarası.
# Country: Ülke adı. Nominal. Müşterinin ikamet ettiği ülkenin adı.

###############################################################
# İş Problemi (Business Problem)
###############################################################

#Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istemektedir.

#Şirket, ortak davranışlar sergileyen müşteri segmentleri özelinde pazarlama çalışmaları yapmanın gelir artışı sağlayacağını düşünmektedir.

#Örneğin şirket için çok kazançlı olan müşterileri elde tutmak için farklı kampanyalar, yeni müşteriler için farklı kampanyalar düzenlenmek istenmektedir.


# Bu projede UCI Online Retail II DataSet kullanılmıştır. Bunun sebebi ise şirketlerin gizlilik anlayışından dolayı verilerini paylaşması mümkün olmadığından genellikle bu analizde bu veri seti kullanılır.

# Bu veri setinde, Birleşik Krallık merkezli ve tescilli, mağaza dışı bir çevrimiçi perakende için 01 / 12 / 2009 ve 09 / 12 / 2011 tarihleri arasında gerçekleşen tüm işlemleri içerir.
# Şirket esas olarak her durumda benzersiz hediyelik eşya satmaktadır. Firmanın birçok müşterisi toptancıdır.

###############################################################
# GÖREV 1: Veriyi Anlama ve Hazırlama
###############################################################

# Kütüphaneler, import komutu ile yüklenilmiştir. Import komutuundan sonra yüklenmek istenen kütüphane yazılmış, sonrasında yazılan as komutuyla ise yüklenmek istenen kütüphaneyi hangi kısaltma ile ifade edeceğimiz belirtilmiştir.
import datetime as dt
# tarih işlemleri için kullanılır
import pandas as pd
pd.set_option("display.max_columns", None)
# satırlarda maximum satırı gösterir
#pd.set_option("display.max_rows", None)
# sütunlarda maximum sütunu gösterir.
pd.set_option("display.float_format", lambda x: "%.5f" % x)

################################################################
# 1.Online Retail II excelindeki 2010-2011 verisini okuyunuz. Oluşturduğunuz dataframe’in kopyasını oluşturunuz.
################################################################

df = pd.read_excel(r"C:\Users\Hp\Desktop\Online_Retail_II\Online_Retail_II.xlsx", sheet_name="Year 2010-2011")
df_ = df.copy()
df_.head()
df_.shape

#################################################################
# 3.Veri setinde eksik gözlem var mı? Varsa hangi değişkende kaç tane eksik gözlem vardır?
#################################################################

df_.isnull().sum()
(df_.isnull().sum()).sum()

#################################################################
# 4.Eksik gözlemleri veri setinden çıkartınız. Çıkarma işleminde ‘inplace=True’ parametresini kullanınız.
#################################################################

df_.dropna(inplace=True)
df_.shape
#################################################################
# 5.Eşsiz ürün sayısı kaçtır?
#################################################################

df_["StockCode"].nunique()

#################################################################
# 6.Hangi üründen kaçar tane vardır?
#################################################################

df["StockCode"].value_counts()

#################################################################
# 7.En çok sipariş edilen 5 ürünü çoktan aza doğru sıralayınız.
#################################################################

df.groupby("StockCode").agg({"Quantity":"sum"}).sort_values(by="Quantity", ascending=False).head(5)

#################################################################
# 8.Faturalardaki ‘C’ iptal edilen işlemleri göstermektedir. İptal edilen işlemleri veri setinden çıkartınız.
#################################################################

df_ = df[df["Invoice"].str.contains("C", na=False)]
# Başında C olanları getir.
df_ = df[~df["Invoice"].str.contains("C", na=False)]
# Başında C olmayanları getirir.

#################################################################
# 9.Fatura başına elde edilen toplam kazancı ifade eden ‘TotalPrice’ adında bir değişken oluşturunuz.
#################################################################

df_["TotalPrice"] = df_["Quantity"] * df_["Price"]

###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Recency, Frequency ve Monetary tanımlarını yapınız.
# Müşteri özelinde Recency, Frequency ve Monetary metriklerini groupby, agg ve lambda ile hesaplayınız.
# Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# Oluşturduğunuz metriklerin isimlerini  recency, frequency ve monetary olarak değiştiriniz.
# Not 1: recency değeri için bugünün tarihini (2011, 12, 11) olarak kabul ediniz.
# Not 2: rfm dataframe’ini oluşturduktan sonra veri setini "monetary>0" olacak şekilde filtreleyiniz.

df_["InvoiceDate"].max()
# Veri setinin maximum tarihini verir.
# O tarih civarında bir tarihi analiz tarihi olarak kabul ederiz.
today_date =dt.datetime(2011, 12, 11)

# Recency – Yenilik (R) – Son satım alımdan bugüne kadar geçen süredir.
rfm = df_.groupby("Customer ID").agg({"InvoiceDate": lambda date: (today_date - date.max()).days})

# Frequency – Sıklık (F) – Toplam satın alım sayısıdır.
rfm = df_.groupby("Customer ID").agg({"Invoice": lambda num: num.nunique()})

# Monetary – Parasallık (M) – Tüm satın alımların parasal toplamıdır.
rfm = df_.groupby("Customer ID").agg({"TotalPrice": lambda Total: Total.sum()})

rfm = df_.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                     'Invoice': lambda num: num.nunique(),
                                     'TotalPrice': lambda Total: Total.sum()})

rfm.head()

rfm.columns = ["Recency", "Frequency", "Monetary"]
rfm.describe().T

rfm = rfm[rfm["Monetary"] > 0]

###############################################################
# GÖREV 3: RFM Skorlarının Oluşturulması ve Tek Bir Değişkene Çevrilmesi
###############################################################

# Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz.
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
# recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RFM_SCORE olarak kaydediniz.
# DİKKAT! monetary_score’u dahil etmiyoruz.

# Recency

rfm["Recency_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])

rfm["Frequency_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
# rank()işlevi, eksen boyunca sayısal veri sıralarını (1'den n'ye kadar) hesaplar. Eşit değerlere, bu değerlerin sıralarının ortalaması olan bir sıra atanır.
# Sıralama işleminden sonra farklı çeyrekliklere gidildiğinde hala aynı çeyreklik değerler gözlemleniyorsa bu bir probleme sebep olduğundan bu methodu kullanırız.

rfm["Monetary_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm["Recency_Score"].astype(str)+
                    rfm["Frequency_Score"].astype(str))

###############################################################
# GÖREV 4: RFM Skorlarının Segment Olarak Tanımlanması
###############################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlamaları yapınız.
# Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz.

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["Segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)

rfm[["Segment", "Recency", "Frequency", "Monetary"]].groupby("Segment").agg(["mean", "count"])

len(rfm[rfm["Segment"] == "hibernating"])

###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# Önemli bulduğunuz 3 segmenti seçiniz. Bu üç segmenti;
# Hem aksiyon kararları açısından,
# Hem de segmentlerin yapısı açısından (ortalama RFM değerleri) yorumlayınız.
# "Loyal Customers" sınıfına ait customer ID'leri seçerek excel çıktısını alınız.

# Champions: En yakın zamanda satın alan ve en çok harcama yapan en iyi müşterilerdir. Bu
# müşterileri ödüllendirmek gerekir. Yeni ürünleri erken benimseyenler olabilir ve markanızın tanıtımına
# yardımcı olurlar.
  # Bu grupta 659 kişi vardır.
  # Ortalama 6.08 gündür alışveriş yapmıyorlar.
  # Ortalama 14.68 kez alışveriş yapmışlar.
  # Ortalama 6552.26 birim para kazandırmışlar.
# Aksiyon: Bu segmentteki müşterilere özel ürünlerin reklamları yapılabilir.
# Yeni ürünlerin kısıtları ürünler varsa, öncelik tanınabilir.
# Satın alma davranışları olumlu olduğundan dolayı, buradaki müşterilere kişisel özelliklerine göre hediyeler verilebilir.
# Doğum gününde adrese özel hediyeler gidebilir.

# New Customers: Genel RFM puanı yüksek olan ancak sık alışveriş yapmayanlar bu grupta yer alır.
# Yakın zamanda alışveriş yapmış olup mağazayı az ziyaret eden müşterilerdir.
    # Bu grupta 42 kişi vardır.
    # Ortalama 7.23 gündür alışveriş yapmıyorlar.
    # Ortalama 1.00 kez alışveriş yapmışlar.
    # Ortalama 377.23 birim para kazandırmışlar.
# Aksiyon: “Potential Loyalists” dediğimiz gruba yakın bir gruptur.
# New Customers‘ta yer alan müşterilerin Frequency değerlerini arttırmak için aksiyonlar alınabilir.
# Toplam satın almalarını arttırmalıyız.
# Ziyaretlerini artırmak için uygun promosyonlar sunulabilir.
# Özel teklifler sağlayarak bu müşterilerle ilişkiler kurmaya başlanabilir.
# İlgilerini çekebilecek, ürün tanıtımları da yapılabilir.

# Hibernating: Bu segmentteki kullanıcılar bizden hem çok uzun zamandır alışveriş yapmamışlar hem de bizi çok iyi tanımıyorlar.
    # Bu grupta 1037 kişi vardır.
    # Ortalama 213.615 gündür alışveriş yapmıyorlar.
    # Ortalama 1.21 kez alışveriş yapmışlar.
    # Ortalama 399.95 birim para kazandırmışlar.
# Aksiyon: Bizi daha iyi tanımaları için bizim ürünlerimizi anlatan ve içerisinde kupon kodu olan bir marketing çalışması yapabiliriz.
# Bu çalışmaların yanı sıra buradaki kitleyi reklam kanallarımıza ekleyerek onlara sosyal medyada reklam gösterebiliriz.
# Bu segmente özel gösterilecek reklamların tasarımları farklı hazırlanabilir.
# Ürünlerimizi tanıtan, ya da onların sitemize gelmesini istediğimiz kelimeler kullanılarak sanki “aa tam da bana söylüyor” etkisi oluşturabiliriz.
# Mailde attığımız kupon kodlarını bu segmente reklamlarda da göstererek uykudan uyanmalarını ve yakın zamanda alışveriş yapmalarını sağlayabiliriz.
# Bu kitle hassastır çok fazla alışveriş odaklı değil de bizi tanıyın , şans verin odaklı bilinirlilik çalışmaları yapılmalıdır.

new_df = pd.DataFrame()
new_df["new_customer_id"] = rfm[rfm["Segment"] == "loyal_customers"].index
new_df.head()

new_df.to_csv("loyal_customers.csv")