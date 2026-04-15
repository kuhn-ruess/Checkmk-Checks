# CMDB Syncer Monitoring

<!-- compatibility-badges:start -->
![Checkmk min](https://img.shields.io/badge/Checkmk%20min-2.3.0p1-2f4f4f) ![Checkmk max](https://img.shields.io/badge/Checkmk%20max-current-informational) ![packaged](https://img.shields.io/badge/packaged-2.4.0p8-blue)
<!-- compatibility-badges:end -->
You can monitor every Service you have running in the Syncer. Just check for his Source name in the Syncer log:

<img width="1386" alt="grafik" src="https://github.com/user-attachments/assets/9573c4ab-58ec-46e6-80db-e030a9090494">

This name you can configure then for the Special Agent:

<img width="711" alt="grafik" src="https://github.com/user-attachments/assets/47fe27bf-7e7d-41b2-b3ae-c2b22e1486f8">

For Every Source you Specify as a Service, a Checkmk Service will be created.
