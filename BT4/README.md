# Bài Tập 4: Lấy danh sách sinh viên của một khóa học

## Phần 1: Phân tích và đề xuất đa giải pháp

### 6.1 Phân tích đầu vào và đầu ra
1. **Dữ liệu nào phải được kiểm tra đầu tiên?**
   - Phải kiểm tra **Course** (khóa học) đầu tiên dựa vào `course_id`. Nếu Course không tồn tại, cần trả về lỗi `404 Not Found`.
2. **Điều kiện nào dùng để lọc Enrollment?**
   - `course_id`: Phải bằng ID khóa học được truyền vào.
   - `status`: Phải là `STUDYING` hoặc `COMPLETED`. (Loại bỏ `CANCELLED`).
3. **Điều kiện nào dùng để lọc Student?**
   - `status`: Phải là `ACTIVE`.
4. **Làm thế nào để loại bỏ sinh viên trùng?**
   - Sử dụng `DISTINCT` trong câu lệnh truy vấn cơ sở dữ liệu để loại bỏ các bản ghi trùng lặp sinh viên (trường hợp cùng 1 sinh viên đăng ký, hủy rồi đăng ký lại khiến bị duplicate dòng).
5. **Trường hợp nào trả về danh sách rỗng?**
   - Nếu Course tồn tại (qua vòng kiểm tra 1) nhưng không có sinh viên nào đăng ký thỏa mãn điều kiện `ACTIVE` và `Enrollment` không bị `CANCELLED`. Lúc này trả về status `200 OK` kèm danh sách rỗng `[]`.

### 6.2 Đề xuất tối thiểu hai giải pháp

- **Giải pháp 1: Truy vấn Enrollment rồi dùng vòng lặp (Application Level Join)**
  - B1: Lấy thông tin Course (`SELECT * FROM Course WHERE id = ?`). Nếu rỗng -> 404.
  - B2: Lấy danh sách Enrollment theo Course ID và status (`SELECT * FROM Enrollment WHERE course_id = ? AND status IN ('STUDYING', 'COMPLETED')`).
  - B3: Dùng vòng lặp trong Python lặp qua danh sách Enrollment, gom danh sách `student_id`.
  - B4: Truy vấn danh sách Student (`SELECT * FROM Student WHERE id IN (...) AND status = 'ACTIVE'`).
  - B5: Xử lý loại bỏ trùng lặp bằng cấu trúc dữ liệu `set` hoặc `dict` trong Python, rồi sắp xếp theo `full_name`.

- **Giải pháp 2: Sử dụng JOIN giữa Student và Enrollment (Database Level Join)**
  - B1: Lấy thông tin Course (`SELECT * FROM Course WHERE id = ?`). Nếu rỗng -> 404.
  - B2: Thực hiện 1 câu truy vấn có `JOIN` trực tiếp trên Database:
    ```sql
    SELECT DISTINCT s.id, s.full_name, s.email
    FROM Student s
    JOIN Enrollment e ON s.id = e.student_id
    WHERE e.course_id = ? 
      AND e.status IN ('STUDYING', 'COMPLETED')
      AND s.status = 'ACTIVE'
    ORDER BY s.full_name ASC;
    ```

## Phần 2: So sánh và lựa chọn

### 6.3 Lập bảng so sánh

| Tiêu chí | Giải pháp dùng vòng lặp | Giải pháp dùng JOIN |
| :--- | :--- | :--- |
| **Độ dễ hiểu** | Dễ hiểu cho người mới học (tư duy tuần tự từng bước). | Cần kiến thức về SQL JOIN và Relationship. |
| **Số câu truy vấn** | Nhiều (Tối thiểu 3 query: Course, Enrollment, Student). | Ít (2 query: 1 cho Course, 1 cho List Student). |
| **Tốc độ khi dữ liệu nhỏ** | Khá nhanh, khác biệt không đáng kể. | Rất nhanh. |
| **Tốc độ khi dữ liệu lớn** | Chậm, vì phải vận chuyển nhiều dữ liệu thô (Enrollment) từ DB lên RAM của Application để tự xử lý lọc, tốn Overhead rất lớn. | Nhanh, tận dụng được sức mạnh xử lý tập hợp và Indexes của Engine Database (RDBMS). |
| **Bộ nhớ sử dụng** | Tốn nhiều RAM của Server App do phải lưu array chứa hàng ngàn record Enrollment để lặp. | Tốn rất ít RAM của Server App, chỉ chứa kết quả cuối cùng đã lọc. |
| **Khả năng bảo trì** | Khó khăn khi logic lọc phức tạp hơn (VD: thêm phân trang, lọc theo điều kiện khác của Student). | Dễ dàng bảo trì, thêm sửa điều kiện chỉ bằng cách thêm vào mệnh đề `WHERE`. |
| **Khả năng mở rộng** | Rất kém, nguy cơ Memory Leak và Timeout khi có hàng chục ngàn sinh viên (N+1 Query Problem tiềm ẩn nếu không dùng WHERE IN). | Rất tốt, có thể gắn thêm Index trên DB để tăng tốc mà không sửa code App. |

**Phân tích bổ sung:**
- *Dễ hiểu với người mới?* Giải pháp vòng lặp dễ hiểu hơn vì đi theo lối tư duy truyền thống step-by-step.
- *Tạo nhiều truy vấn hơn?* Giải pháp vòng lặp.
- *Khi có 1.000 sinh viên?* Giải pháp JOIN sẽ phù hợp và hiệu suất tốt hơn nhiều.
- *Dễ thêm điều kiện lọc?* Giải pháp JOIN dễ thêm điều kiện hơn bằng các mệnh đề `AND`.
- *Nguy cơ gây chậm API?* Giải pháp vòng lặp, đặc biệt nếu lỡ dùng vòng lặp cho từng sinh viên để query DB (Lỗi N+1).

### 6.4 Lựa chọn giải pháp
- **Giải pháp được chọn:** **Giải pháp 2 (Sử dụng JOIN giữa Student và Enrollment)**.
- **Lý do lựa chọn:** Đây là cách tiếp cận "Best Practice" khi làm việc với CSDL quan hệ. Database được thiết kế để thực hiện việc lọc, nối bảng (JOIN), sắp xếp (ORDER BY), và loại bỏ trùng lặp (DISTINCT) cực kỳ nhanh chóng. Việc đẩy gánh nặng xử lý dữ liệu cho RDBMS giúp API tiết kiệm RAM, giảm thiểu số vòng kết nối mạng (I/O network) giữa App và Database, đồng thời hỗ trợ phân trang (Pagination) rất dễ dàng ở các phase sau.
- **Bối cảnh giải pháp còn lại phù hợp:** Giải pháp dùng vòng lặp chỉ phù hợp khi chúng ta lấy dữ liệu từ hai hệ thống Database khác nhau (Microservices) hoặc các CSDL không phải quan hệ (NoSQL như MongoDB).
- **Sự đánh đổi:** Yêu cầu lập trình viên phải hiểu rõ về SQLAlchemy Relationships, cách ánh xạ và setup ForeignKey để framework sinh ra câu lệnh JOIN chính xác.

## Phần 3: Thiết kế và Triển khai

Source code được đặt trong thư mục này, sử dụng `FastAPI` và `SQLAlchemy v2`. Vui lòng xem mã nguồn chi tiết.
