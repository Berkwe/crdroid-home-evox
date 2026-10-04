# crDroid Home for Evolution X

**English** | [Türkçe](README.tr.md)

A small systemless module that brings the crDroid launcher to Evolution X, including Quickspace and weather support.

This project is **vibe coded**. The analysis, patch, and build scripts were made with help from Codex, then tested on a real phone. The main features work, but bugs, launcher crashes, or incompatibilities after ROM updates are possible. This is an unofficial project, with no affiliation to crDroid or Evolution X.

## Compatibility

Tested on **Nothing Phone (1) / spacewar, Evolution X 11.10, Android 16**, using KernelSU/KowSU with Mountify. The source launcher comes from crDroid 12.11 / Android 16.

This release was made for that setup. It may work on other devices or ROMs, but those have not been tested and compatibility is not guaranteed. The target ROM must already include OmniJaws; the module does not install the OmniJaws app.

The Home screen, weather with Quickspace enabled, Recents, and operation after reboot were checked. Not every launcher feature or combination of settings was tested.

## What it does

The module adds the crDroid launcher as a privileged app and sets it as the Recents provider. It embeds the OmniJawsClient classes that Quickspace expects but Evolution X lacks into the launcher APK. This lets it use the ROM's existing OmniJaws app for weather.

It does not replace framework files or SystemUI. Disabling the module and rebooting removes its mounted files.

## Pixel Launcher

This module also breaks Pixel Launcher; it can crash with a “keeps stopping” message. Use the crDroid launcher as your default Home app while the module is installed. To switch back to Pixel Launcher, disable the module and reboot first.

## Installation

1. Download `crDroidHome-EvoX-v3.zip` from [Releases](https://github.com/Berkwe/crdroid-home-evox/releases/latest).
2. Back up your previous launcher module and settings. Other modules that change the launcher or Recents may conflict.
3. Install the ZIP through your root manager with Mountify installed, then reboot.
4. Select the crDroid launcher as your default Home app if needed.
5. Select **OmniJaws** as the Quickspace weather provider and enable weather in the OmniJaws settings.

Open-Meteo was used during testing because OpenWeatherMap returned HTTP 401. The ZIP does not change your provider or location preferences; you choose those yourself. On this ROM, `Auto` can select Seraphix.

If something goes wrong, disable the module through your root manager and reboot. If the launcher still opens, disabling Quickspace can also be a temporary workaround. Removing the module does not restore all app preferences to their previous values.

## Building

The **Build module** workflow in GitHub Actions produces the patched APK and module ZIP from files extracted from the source ROM. It does not build the full Android ROM or launcher from source. The APK/JAR inputs are kept in a separate `build-inputs` release instead of git history, and their hashes are checked before building.

Run the workflow manually from the Actions page and download its output artifact. For the same process on your computer or in a Codespaces terminal, see the [build notes](docs/BUILD.md) (in Turkish).

## Sources

The launcher and weather code come from crDroid, OmniROM, and AOSP. This repository contains the port scripts, module template, and Recents overlay source. The upstream commits, file hashes, and signing details are listed in [SOURCES.md](docs/SOURCES.md). The port implementation and device tests are described in [PORT.md](docs/PORT.md). These detailed notes are currently in Turkish.
