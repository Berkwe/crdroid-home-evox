# v4 navigasyon düzeltmesi

v3 yüklendikten sonra hareket çubuğu kaybolabiliyor veya koyu zeminde görünmüyordu. Klavye altında da gereğinden büyük bir alan oluşuyordu. Sorun reboot ile düzelmiyordu.

Neden, crDroid ile Evolution X'in private framework resource ID'lerinin farklı olmasıydı. Launcher'ın kendi dimension kaynakları, crDroid'de derlenmiş ID'ler üzerinden yanlış Evolution X kaynaklarını okuyordu.

| Launcher kaynağı | Beklenen Android kaynağı | Evolution X'te yanlış okunan kaynak |
|---|---|---|
| `taskbar_phone_size` | `navigation_bar_frame_height` | `min_window_blur_radius` (`1px`) |
| `taskbar_stashed_size` | `taskbar_stashed_size` | `task_height_of_minimized_mode` (`80dp`) |
| `taskbar_size` | `taskbar_frame_height` | `system_gestures_start_threshold` |
| `taskbar_phone_rounded_corner_content_margin` | `rounded_corner_content_padding` | `restricted_icon_size_material` |
| `persistent_taskbar_corner_radius` | `rounded_corner_radius` | `round_scrollbar_width` |

v4, `com.android.launcher3` paketini hedefleyen `com.berkwe.crdroidnavcompat` static RRO'sunu `/product/overlay/CrDroidNavigationCompat.apk` yoluna systemless olarak ekler. Beş dimension, test edilen Evolution X framework-res APK'sına karşı kaynak adıyla yeniden bağlanır. Kaynak XML'leri `overlay-navigation/` içinde; overlay derleme scriptiyle üretilir.

Launcher APK'sı ve eski Recents RRO değiştirilmez. Framework ve SystemUI değiştirilmez. Bu düzeltme ölçüleri doğru kaynağa bağlar; çubuğu her zeminde zorla aynı renge boyamaz.

Cihazda ilk overlay testi sonrası navigasyon inset'i 230 pikselden 69 piksele indi. Hareket çubuğu Home'da ve klavye açıkken tekrar görüldü; fazla klavye alt boşluğu düzeldi. Kullanıcı da düzelmeyi doğruladı. Ardından overlay systemless modüle taşındı; reboot sonrası `/product/overlay/` yolundan etkin yüklendiği ve `taskbar_stashed_size=24dp` olduğu kontrol edildi.

Bu private kaynaklar başka ROM sürümlerinde tekrar değişebilir. v4 yine yalnızca README'de belirtilen Evolution X kurulumu için test edilmiştir.
