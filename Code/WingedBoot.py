# Hàm xử lý khi nhân vật nhặt bình thuốc tăng tốc
def handle_speed_boost(char_rect, speed_rect, current_time, movement_speed, speed_boost_active, speed_boost_start_time, speed_boost_duration):
    # Kiểm tra nếu nhân vật nhặt được bình thuốc và chưa kích hoạt boost
    if char_rect.colliderect(speed_rect) and not speed_boost_active:
        pick_up_sound.play()  # Phát âm thanh khi nhặt bình thuốc
        speed_rect.topleft = (-1000, -1000)  # Di chuyển bình thuốc ra ngoài màn hình
        movement_speed = 10  # Tăng tốc độ di chuyển
        speed_boost_active = True  # Đánh dấu hiệu ứng tăng tốc đã kích hoạt
        speed_boost_start_time = current_time  # Lưu lại thời gian bắt đầu boost

    # Kiểm tra xem boost đã hết thời gian chưa
    if speed_boost_active and current_time - speed_boost_start_time > speed_boost_duration:
        movement_speed = 5  # Đặt lại tốc độ di chuyển về bình thường
        speed_boost_active = False  # Tắt hiệu ứng boost
    return movement_speed, speed_boost_active, speed_boost_start_time
