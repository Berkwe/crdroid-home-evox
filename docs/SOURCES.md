# Kaynaklar ve dosya kökeni

Girdiler `crDroidAndroid-16.0-20260811-Spacewar-v12.11` ROM'undan çıkarıldı. Kaynak commit'leri ROM'un `product/etc/build-manifest.xml` dosyasından alındı. Bu bağlantılar kodun kökenini gösterir; ROM APK/JAR dosyalarını yalnızca bu commit'lerden birebir yeniden üretme iddiası yoktur.

| Parça | Kaynak |
|---|---|
| Launcher3 | [crDroid Launcher3, e19eb92](https://github.com/crdroidandroid/android_packages_apps_Launcher3/tree/e19eb92f2e8d863e6ee9f041d768496bc16151f5) |
| Framework / OmniJawsClient | [crDroid frameworks/base, 708e793](https://github.com/crdroidandroid/android_frameworks_base/tree/708e793e39322960e8f61edf2028aa30b07901fe) |
| İlgili sınıfın kaynağı | [OmniJawsClient.java](https://github.com/crdroidandroid/android_frameworks_base/blob/708e793e39322960e8f61edf2028aa30b07901fe/core/java/com/android/internal/util/crdroid/OmniJawsClient.java) |
| OmniJaws uygulaması | [crDroid OmniJaws, 11276aa](https://github.com/crdroidandroid/android_packages_services_OmniJaws/tree/11276aa1d68bad38ad29d8fad9d01be3dca1b436) |
| OmniJaws'ın kökeni | [OmniROM OmniJaws](https://github.com/omnirom/android_packages_services_OmniJaws) |
| Android altyapısı | [Android Open Source Project](https://source.android.com/) |
| DEX araçları | [JADX 1.5.6](https://github.com/skylot/jadx/releases/tag/v1.5.6), içindeki dexlib2/smali sınıfları |
| Test imza dosyaları | [AOSP platform test certificate](https://android.googlesource.com/platform/build/+/refs/heads/main/target/product/security/platform.x509.pem), [test key](https://android.googlesource.com/platform/build/+/refs/heads/main/target/product/security/platform.pk8) |

## ROM girdileri

`build-inputs` release'indeki arşiv yalnızca bu iki dosyayı içerir. Hash'leri `inputs.lock.json` içinde kilitlidir.

| Arşivdeki isim | ROM içindeki yol | SHA-256 |
|---|---|---|
| `framework.jar` | `system/system/framework/framework.jar` | `fcc4989e81a739dba53cda6a6c201bf49ac09a1b1ab084a39a105ac50ed10d6d` |
| `Launcher3QuickStep.apk` | `system_ext/priv-app/Launcher3QuickStep/Launcher3QuickStep.apk` | `6e51e0d5b643b4dea0037f19e1c3e9d617e4fee837f605e4847339eb7dca0519` |

Framework JAR yalnızca derleme girdisidir. Son modüle eklenmez ve cihaz framework'ünün üzerine mount edilmez.

Permission XML'leri kaynak ROM'un `system_ext/etc/permissions` dizininden alındı. Recents RRO bu port için yazıldı; kaynak XML'leri `overlay/` dizininde. Küçük, cihazda denenmiş compiled RRO `module/system/product/overlay/` altında korunuyor. RRO'nun SHA-256 değeri `5a066310fe30b2be3146e3e8aaebbcb4a11d937b3c6a0f84a9fe15cdd71f3ee3`.

## Lisans

Port scriptleri ve bu repo için yazılan overlay Apache-2.0 lisansı altında. Upstream kod, ROM dosyaları ve içerdikleri üçüncü taraf bileşenler kendi lisanslarını korur. OmniJawsClient kaynak başlığı OmniROM ve crDroid teliflerini içerir. Bu repo launcher'ın, OmniJaws'ın veya Evolution X'in sahipliğini iddia etmez.
