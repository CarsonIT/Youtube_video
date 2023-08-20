# Youtube video dataset
Bộ dữ liệu này bao gồm dữ liệu trong vài tháng (và còn tiếp tục tăng) về các video thịnh hành hàng ngày trên YouTube. Dữ liệu được bao gồm cho các khu vực Hoa Kỳ, GB, DE, CA và FR (tương ứng là Hoa Kỳ, Vương quốc Anh, Đức, Canada và Pháp) và RU, MX, KR, JP và IN (tương ứng là Nga, Mexico, Hàn Quốc, Nhật Bản và Ấn Độ)  với tối đa 200 video thịnh hành được liệt kê mỗi ngày.

Dữ liệu của mỗi khu vực nằm trong một tệp riêng biệt. Dữ liệu bao gồm tiêu đề video, tiêu đề kênh, thời gian xuất bản, thẻ, lượt xem, lượt thích và không thích, mô tả và số lượng nhận xét.
Dữ liệu cũng bao gồm thể loại video khác nhau giữa các vùng. Để truy xuất thể loại đó cho một video cụ thể, hãy tìm thể loại đó trong liên kết JSON. 
# Mục tiêu
1.	Sử dụng Apache Airflow cùng ngôn ngữ lập trình Python để thực hiện quá trình trích xuất, biến đổi và nạp dữ liệu (ETL) vào cơ sở dữ liệu SQL Server.
2.	Tạo mô hình dữ liệu (data modeling) để mô tả cấu trúc và mối quan hệ giữa các thông tin trong dữ liệu.
3.	Sử dụng PowerBI để thể hiện trực quan thông tin thống kê của một số chỉ số thông qua biểu đồ và hình vẽ.
