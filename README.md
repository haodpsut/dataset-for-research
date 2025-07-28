# dataset-for-research

## 1. Dataset mà mình hay làm về network: 
Edge-IIoTset: A New Comprehensive Realistic Cyber Security Dataset of IoT and IIoT Applications: Centralized and Federated Learning

https://ieee-dataport.org/documents/edge-iiotset-new-comprehensive-realistic-cyber-security-dataset-iot-and-iiot-applications

Paper kết quả baseline đã có:
https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9751703

## 2. Global Web Cache Latency Measurement Dataset (Spache‑WWW’25)
Khoảng 2 triệu phép đo RTT ping tới 50 website phổ biến, thu thập bằng probe RIPE Atlas dùng kết nối LEO (Starlink hoặc các mạng LEO khác), trải khắp 5 châu lục trong 24 giờ 

Global Web Cache Latency Measurement for Low-Earth Orbit Satellite Networks: A Dataset
https://zenodo.org/records/14835444

Phù hợp: nghiên cứu caching web trên vệ tinh, mô phỏng chiến lược routing, học dự đoán RTT để tối ưu QoS hoặc điều phối server cache.


## 3. WetLinks – Starlink Dataset kèm dữ liệu thời tiết
Gồm khoảng 140.000 phép đo từ 2 vị trí ở Châu Âu trong 6 tháng. Có RTT, throughput, traceroute và dữ liệu thời tiết từ trạm thời tiết gần thiết bị Starlink 
Phù hợp: nghiên cứu ảnh hưởng của thời tiết (mưa, sương, độ ẩm...) đến latency và throughput, xây dựng mô hình latency phụ thuộc điều kiện môi trường.

https://github.com/sys-uos/WetLinks
https://arxiv.org/pdf/2402.16448


## 4. LEO Satellite Channel – Channel Coefficients Dataset
Mô phỏng kênh tín hiệu từ LEO satellite với Massive MIMO, gồm dữ liệu channel vectors cho 1000 người dùng ngẫu nhiên với thông tin vị trí, antena UPA 20×20… 

tên dataset: Dataset Description: Channel coefficients of multiple users connected to a LEO satellite equipped with massive MIMO antenna.

paper: CVaR-based Robust Beamforming Framework for Massive MIMO LEO Satellite Communications

https://fnr-smartspace-project.uni.lu/leo-satellite-channel/?utm_source=chatgpt.com
Phù hợp: thiết kế beamforming, nghiên cứu scheduling/kênh cho giảm delay trong mạng vệ tinh trong môi trường vật lý.

5. Radio KPI & Latency Measurement for Satellite + 5G (Danimarca)
Dataset từ dự án COMMECT của Aalborg University, gồm các KPI đo latency, throughput từ cả kết nối 5G NSA và kết nối vệ tinh, trong môi trường thực địa phục vụ giám sát vận chuyển gia súc tại vùng nông thôn Đan Mạch 

Radio KPI & Latency Measurement of Cellular and Satellite Networks for Evaluating Multi-Connectivity Solutions in Livestock Transport Monitoring in Rural Areas

https://zenodo.org/records/14620779?utm_source=chatgpt.com

Phù hợp: so sánh performance giữa hai loại kết nối, tối ưu chuyển đổi (handover), multi‑connectivity để giảm độ trễ hệ thống.

Updated: 28.07.2025
