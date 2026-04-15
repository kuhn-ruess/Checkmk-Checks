# Notification plugin for playing sounds via API

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.4.0b1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p24-blue)
<!-- compatibility-badges:end -->

This notification plugin is used to play sounds on TVs, computers or similar devices, which can output audio.

Plugin will send an API request to backend, which will play autio files.

It was tested with XAMPP 3.3.0 on Windows 11.

## Setup
1) Install XAMPP on your host with Windows 11
2) Extract html.zip to root folder of XAMPP installation
3) Test sound with http://localhost/sounds.php
4) Intall MKP in Checkmk
5) Konfigure a notification rule
