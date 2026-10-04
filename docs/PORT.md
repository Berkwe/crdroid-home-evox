# Port notları

Quickspace açılınca launcher, `com.android.internal.util.crdroid.OmniJawsClient$OmniJawsObserver` bulunamadığı için çöküyordu. Quickspace kapalıyken launcher ve Recents çalışıyordu.

Çözüm, kaynak framework'teki OmniJawsClient ve sekiz iç/sentetik sınıfını aynı package adıyla launcher içine `classes3.dex` olarak eklemek oldu. Çıkarılan DEX 15.504 bayt. Mevcut iki launcher DEX'i ve kaynakları korunuyor.

## Bağımlılıklar

OmniJawsClient'ın çalıştırdığı API'ler Android Context, ContentResolver, Cursor, PackageManager, Resources ve broadcast API'leri ile standart Java sınıfları. Başka crDroid yardımcı sınıfı gerekmiyor. JADX çıktısındaki bazı internal API isimleri inline edilmiş sabitlerin yeniden adlandırılmasından geliyor; DEX'te bu sınıflara runtime çağrısı bulunmuyor.

Hava verisi `org.omnirom.omnijaws.provider` üzerinden `weather`, `settings` ve `hourly` yollarından okunuyor. `WEATHER_UPDATE` ve `WEATHER_ERROR` broadcast'leri dinleniyor. Launcher'ın `org.omnirom.omnijaws.READ_WEATHER` izni gerekiyor; test cihazında zaten verilmişti. Özel bir crDroid Binder servisi veya framework shim gerekmiyor.

Evolution X'in mevcut OmniJaws uygulaması bu sözleşmeyi sağlıyor. Bu yüzden crDroid OmniJaws APK'sı, kaynak OmniJaws RRO'su veya yeni konum permission XML'i modüle eklenmedi. Bu karar, mevcut OmniJaws'ın kurulu ve izinlerinin verilmiş olduğu test cihazına dayanıyor.

## Test

4 Ekim 2026'da Nothing Phone (1), Evolution X 11.10 / Android 16 üzerinde:

- Launcher Home ekranı çizildi.
- `pref_quickspace=true` ile launcher açıldı.
- OmniJaws seçiliyken Open-Meteo verisi ve hava ikonu Quickspace'te gösterildi.
- Recents ekranı açıldı ve Recents component'i crDroid launcher olarak kaldı.
- İki reboot yapıldı; ikinci reboot sonrası Quickspace ve hava verisi tekrar görüldü.
- Test loglarında launcher crash'i veya OmniJawsClient ClassNotFoundException görülmedi.
- MANAGE_ACTIVITY_TASKS, READ_FRAME_BUFFER ve READ_WEATHER izinleri korunmuştu.

APK imzası ve ZIP bütünlüğü doğrulandı. Mevcut launcher'ın 8.826 META-INF dışı entry'si aynı kaldı; Recents RRO ve permission XML'leri önceki modülle birebir aynıydı.

Test edilen patched APK SHA-256:

```text
8891afe77b47b9cbd47d0e0d37eb82460d3fc5b4df7bbf055ebf9418601f82da
```

Bu sonuçlar yalnızca belirtilen kurulum ve test süresi için geçerli. Diğer ROM'lar, farklı imzalı launcher sürümleri, uzun süreli hava güncellemeleri ve tüm ayar kombinasyonları doğrulanmadı. Derleme çıktısının APK hash'i bu değerle eşleşmiyorsa yeni çıktı ayrıca cihazda denenmelidir.
