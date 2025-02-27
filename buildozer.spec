# Buildozer.spec file for building Kivy app APK

[app]
title = Calculator Vault
package.name = calculatorvault
package.domain = com.example
source.include_exts = py,png,jpg,kv,atlas

requirements = python3, kivy

android.arch = armeabi-v7a
android.ndk_api = 23
android.api = 31
android.minapi = 21
android.package = org.example.calculatorvault
android.p4a_whitelist =
android.p4a_blacklist =
android.p4a_bootstrap = sdl2
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
