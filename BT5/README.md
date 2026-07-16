# Bài Tập 5: Xây dựng hệ thống đăng ký workshop cho sinh viên

## Phần 1: Thiết kế kiến trúc

### 7.1 Phân tích nhu cầu

1. **Khách hàng đang gặp vấn đề gì?**
   - Đăng ký trùng lặp: Sinh viên điền nhiều lần cùng 1 form.
   - Vượt quá số lượng: Workshop đầy vẫn nhận đăng ký vì Google Form khó limit động.
   - Quản lý thời gian mở/đóng: Sinh viên vẫn đăng ký được khi workshop đã kết thúc.
   - Khó tra cứu chéo: Nhân viên mệt mỏi trong việc gom file Excel để xem "Sinh viên A học những workshop nào" hay "Workshop B gồm những ai".

2. **Người dùng chính của hệ thống là ai?**
   - **Sinh viên:** Đăng ký / Hủy đăng ký workshop, xem danh sách workshop của mình.
   - **Quản trị viên (Nhân viên trung tâm):** Tạo, quản lý workshop, xem danh sách sinh viên.

3. **Hệ thống cần giải quyết những chức năng nào?**
   - Quản lý dữ liệu sinh viên (CRUD cơ bản).
   - Quản lý dữ liệu workshop (CRUD cơ bản, cập nhật trạng thái/số lượng).
   - Xử lý luồng đăng ký (Kiểm tra điều kiện: Workshop tồn tại, chưa bị đầy, đang mở, Sinh viên tồn tại, chưa đăng ký).
   - Xử lý luồng hủy đăng ký (Cập nhật trạng thái Soft-delete thay vì xóa hẳn dòng).
   - Truy xuất và thống kê (Lấy danh sách chéo).

4. **Chức năng quan trọng nhất là gì?**
   - Chức năng **Đăng ký workshop** là quan trọng nhất vì nó liên quan trực tiếp đến nghiệp vụ cốt lõi, đòi hỏi phải Validation dữ liệu cực kỳ chặt chẽ (đảm bảo tính vẹn toàn dữ liệu - Data Integrity) để giải quyết các pain-points ban đầu.

### 7.2 Thiết kế cơ sở dữ liệu

**Các Bảng & Khóa**
1. **Bảng `students`**
   - `id` (Integer): Primary Key.
   - `student_code` (String): Unique. (Nên dùng mã SV là duy nhất, Email có thể thay đổi hoặc có người dùng 2 email, tuy nhiên ta sẽ Unique cả 2).
   - `email` (String): Unique.
   - `full_name` (String)
   - `status` (String): Trạng thái (ACTIVE, INACTIVE).

2. **Bảng `workshops`**
   - `id` (Integer): Primary Key.
   - `title` (String)
   - `description` (String)
   - `maximum_participants` (Integer)
   - `status` (String): (OPEN, CLOSED, CANCELLED).
   - `start_time` (DateTime)

3. **Bảng `registrations` (Bảng trung gian)**
   - `id` (Integer): Primary Key.
   - `student_id` (Integer): Foreign Key -> `students.id`.
   - `workshop_id` (Integer): Foreign Key -> `workshops.id`.
   - `registered_at` (DateTime): Thời gian đăng ký.
   - `status` (String): Trạng thái (REGISTERED, CANCELLED). Hủy đăng ký chỉ update status, không Hard-Delete.

**Loại Quan Hệ**
- Quan hệ Many-to-Many giữa `students` và `workshops` được tách thành 2 quan hệ One-to-Many thông qua bảng trung gian `registrations`.
- Một Student có nhiều Registration, Một Workshop có nhiều Registration.

### 7.3 Quyết định thiết kế (Trả lời các câu hỏi nghiệp vụ)
1. **Workshop có những trạng thái nào?** `OPEN` (Đang nhận), `CLOSED` (Đã đủ người/Đóng form), `CANCELLED` (Bị hủy).
2. **Sinh viên có những trạng thái nào?** `ACTIVE` (Bình thường), `INACTIVE` (Đã nghỉ học/Cấm thi).
3. **Khi sinh viên hủy đăng ký thì xóa dữ liệu hay đổi trạng thái?** Đổi trạng thái (`status = CANCELLED`) để lưu lại Audit Log phục vụ thống kê (sinh viên nào hay bùng kèo).
4. **Có cho phép sinh viên không hoạt động đăng ký không?** Không, chỉ cấp quyền cho `ACTIVE`.
5. **Khi workshop đã bắt đầu thì có được đăng ký không?** Không, hệ thống có thể so sánh thời gian hiện tại với `start_time` để từ chối nếu bị trễ.
6. **Khi workshop bị hủy thì các đăng ký được xử lý thế nào?** Không cần cập nhật tất cả đăng ký, chỉ cần API kiểm tra nếu Workshop bị Cancelled thì không cho đăng ký mới, có thể bắn notification (Nằm ngoài phạm vi yêu cầu hiện tại).
7. **Email hay mã sinh viên cần duy nhất?** Cả 2 đều nên duy nhất, nhưng mã sinh viên làm định danh nghiệp vụ tốt hơn.
8. **API nên trả về dữ liệu phẳng hay lồng nhau?** Trả về lồng nhau (Nested) sẽ tiện cho Frontend hơn. Ví dụ API lấy chi tiết Workshop sẽ trả kèm List Students bên trong thay vì Frontend phải gọi 2 API.
9. **Những chức năng nào cần tách thành service?** Việc kiểm tra logic điều kiện (kiểm tra tồn tại, đếm số lượng slot trống) được tách vào lớp CRUD (hoặc Repositories) để Controller (Router) gọn gàng.

## Phần 2: Sản phẩm hoàn chỉnh
Mã nguồn nằm trong thư mục này.
Khởi động MySQL bằng `docker-compose up -d`.
Chạy ứng dụng bằng `uvicorn main:app --reload`.
Truy cập tài liệu API tại `http://localhost:8000/docs`.
