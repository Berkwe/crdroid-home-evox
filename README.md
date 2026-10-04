# crDroid Home for Evolution X

crDroid launcher'ını Evolution X üzerinde kullanmak için küçük bir systemless modül. Quickspace ve hava durumu desteğini de çalıştırıyor.

Bu proje açıkça **vibe coded**. Analiz, patch ve derleme scriptleri Codex yardımıyla hazırlandı, ardından gerçek telefonda denendi. Genel hatlarıyla çalışıyor ama hata, launcher çökmesi veya ROM güncellemesinden sonra uyumsuzluk çıkabilir. Resmî bir crDroid ya da Evolution X projesi değil.

## Uyumluluk

Test edilen ortam **Nothing Phone (1) / spacewar, Evolution X 11.10, Android 16**. Root tarafında KernelSU/KowSU ve Mountify kullanıldı. Kaynak launcher crDroid 12.11 / Android 16'dan alındı.

Bu sürüm o kurulum için hazırlandı. Diğer cihazlarda veya ROM'larda da çalışabilir, fakat denenmedi ve kesin uyumluluk sözü veremem. Hedef ROM'da OmniJaws bulunması gerekiyor; modül OmniJaws uygulamasını ayrıca kurmuyor.

Home ekranı, Quickspace açıkken hava durumu, Recents ve yeniden başlatma sonrası çalışma kontrol edildi. Tüm launcher özellikleri ve ayar kombinasyonları test edilmedi.

## Ne yapıyor?

crDroid launcher'ını privileged app olarak ekliyor ve Recents sağlayıcısını bu launcher'a yönlendiriyor. Quickspace'in beklediği, Evolution X'te eksik olan OmniJawsClient sınıflarını launcher APK'sının içine koyuyor. Böylece hava durumu için ROM'daki OmniJaws uygulamasını kullanabiliyor.

Framework dosyalarını veya SystemUI'yi değiştirmiyor. Modülü kapatıp yeniden başlatarak mount edilen dosyaları geri alabiliyorsun.

## Kurulum

1. [Releases](https://github.com/Berkwe/crdroid-home-evox/releases/latest) sayfasından `crDroidHome-EvoX-v3.zip` dosyasını indir.
2. Önceki launcher modülünü ve ayarlarını yedekle. Aynı işi yapan başka modüller varsa çakışabilir.
3. Mountify kurulu root yöneticisinden ZIP'i yükle ve telefonu yeniden başlat.
4. Gerekirse varsayılan Home uygulaması olarak crDroid launcher'ını seç.
5. Quickspace hava durumu sağlayıcısını **OmniJaws** seç ve OmniJaws ayarlarından hava durumunu aç.

Testte OpenWeatherMap HTTP 401 döndürdüğü için Open-Meteo kullanıldı. ZIP sağlayıcı veya konum tercihini değiştirmiyor; bunları kendin seçiyorsun. `Auto` seçeneği bu ROM'da Seraphix'i seçebiliyor.

Sorun çıkarsa root yöneticisinden modülü kapatıp yeniden başlat. Launcher açılabiliyorsa Quickspace'i kapatmak da geçici çözüm olabilir. Modülü kaldırmak uygulama tercihlerinin tamamını eski hâline getirmez.

## Derleme

GitHub Actions'taki **Build module** akışı kaynak ROM'dan çıkarılmış dosyalarla patched APK ve modül ZIP'ini üretir. Android ROM'unu veya launcher'ı kaynak koddan tamamen derlemez. APK/JAR girdileri git geçmişi yerine ayrı `build-inputs` release'inde tutulur; hash'leri derlemeden önce kontrol edilir.

Actions sayfasından akışı elle çalıştırıp sonuçtaki artifact'i indirebilirsin. Aynı işlemi bilgisayarında veya Codespaces terminalinde yapmak için [derleme notlarına](docs/BUILD.md) bak.

## Kaynaklar

Launcher ve hava durumu kodu crDroid, OmniROM ve AOSP çalışmalarına dayanıyor. Bu repo port scriptlerini, modül şablonunu ve Recents overlay kaynağını içeriyor. Kullanılan upstream commit'leri, dosya hash'leri ve imza bilgisi [SOURCES.md](docs/SOURCES.md) içinde. Portun nasıl çalıştığı ve cihaz testleri [PORT.md](docs/PORT.md) içinde.
