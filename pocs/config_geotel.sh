#!/bin/bash

ADB_PATH=/home/gescande/Téléchargements/platform-tools/

TRAPTA_APK_URL=http://www.trapta.eu/bin/trapta.apk
ADB_Download_URL=https://dl.google.com/android/repository/platform-tools-latest-linux.zip

read -p "Passer le telephone en mode developpeur -> Settings -> About phone -> 5 clic sur Build number "
read -p "Activer le debuggage USB -> Settings -> Developer options -> USB debugging "


$ADB_PATH/adb shell settings put system accelerometer_rotation 1
$ADB_PATH/adb shell settings put system screen_brightness_mode 1
$ADB_PATH/adb shell settings put system system_locales fr-FR

$ADB_PATH/adb shell dumpsys iphonesubinfo

$ADB_PATH/adb install trapta.apk 

$ADB_PATH/adb shell pm uninstall -k --user 0 com.android.

$ADB_PATH/adb shell reboot
