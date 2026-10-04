# Derleme

Bu işlem hazır crDroid ROM dosyalarını patch eder. Launcher'ı Android kaynak ağacından sıfırdan derlemez.

## GitHub Actions

Repo içindeki **Actions → Build module → Run workflow** yolunu kullan. Akış `build-inputs-v4` release'indeki `source-inputs-v4.zip` arşivini indirir, üç ROM dosyasının SHA-256 değerlerini `inputs.lock.json` ile karşılaştırır, OmniJawsClient sınıflarını çıkarır ve modülü paketler.

Sonuç `crDroidHome-EvoX-v4` artifact'i içinde bulunur: modül ZIP'i, checksum ve `build-report.json`. Workflow otomatik release yayımlamaz. Artifact'i indirdikten sonra içindeki modül ZIP'ini kur; artifact'in dış ZIP'i kurulum paketi değildir.

Yeni bir kaynak ROM kullanacaksan hash dosyasını güncellemek tek başına uyumluluk sağlamaz. Sınıf bağımlılıkları, imza, izinler ve cihaz davranışı yeniden incelenmelidir.

## Yerel veya Codespaces

Java 21, Python 3 ve Android SDK Build Tools 37.0.0 gerekir. SDK ve `gh` kuruluysa repo kökünde:

```bash
mkdir -p build
gh release download build-inputs-v4 --repo Berkwe/crdroid-home-evox \
  --pattern source-inputs-v4.zip --dir build
python3 scripts/unpack_inputs.py build/source-inputs-v4.zip
python3 scripts/setup_tools.py
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" 'build-tools;37.0.0'
python3 scripts/build.py --build-tools "$ANDROID_HOME/build-tools/37.0.0"
```

Codespaces'te Java veya Android SDK yoksa önce bunları kurman gerekir. Hazır ortam isteyenler için Actions daha kolay.

Girdi arşivi bilgisayarındaysa ilk indirme komutu yerine `python3 scripts/unpack_inputs.py /path/to/source-inputs-v4.zip` kullanabilirsin. Sonuçlar `dist/` altında oluşur. Girdiler, indirilen araçlar, anahtarlar ve derleme çıktıları `.gitignore` ile repo dışında tutulur.

## Kontroller

Derleme dokuz OmniJawsClient sınıfını bekler. Orijinal launcher'ın manifest, kaynak ve mevcut DEX içeriklerinin değişmediğini, yeni APK'nın aynı sertifikayla imzalandığını, ZIP bütünlüğünü ve APK hizalamasını kontrol eder. Modül içinde framework replacement olmadığını da doğrular.

APK, kaynak launcher ile eşleşen **yayımlanmış AOSP platform test anahtarı** ile imzalanır. Bu, Evolution X'in özel imza anahtarı değildir. İmza denetimini kapatan bir patch uygulanmaz.

Scriptlerin başarılı çalışması cihaz uyumluluğu testi yerine geçmez. `build-report.json` bu yüzden `device_tested: false` içerir. Paylaşılan sürümlerin gerçek cihaz testleri [PORT.md](PORT.md) içinde.

İlk [GitHub Actions derlemesi](https://github.com/Berkwe/crdroid-home-evox/actions/runs/37214921970) başarılı oldu. İndirilen APK'nın tüm 9.094 ZIP entry'sinin açılmış içeriği, telefon testindeki APK ile karşılaştırılıp aynı bulundu. İmza ve diğer modül dosyaları da doğrulandı. Sıkıştırma araçlarının sürümü APK'nın toplam hash'ini değiştirebilir; aynı dosya içerikleri her ortamda aynı arşiv baytlarını garanti etmez. v3.0 release'inde doğrudan telefonda denenmiş ZIP paylaşılmıştır. v4 derlemesi ayrıca navigasyon uyumluluk overlay’ini hedef ROM’un framework-res kaynaklarına karşı derler. Bu APK yalnızca derleme girdisidir; hedef framework’ün üzerine kurulmaz.
