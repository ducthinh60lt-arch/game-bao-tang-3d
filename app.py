import streamlit as st

# Cấu hình trang web Streamlit hiển thị tràn viền sắc nét
st.set_page_config(
    page_title="Hành Trình Bảo Tàng Nghệ Thuật - 7 Kiệt Tác",
    page_icon="🏛️",
    layout="wide"
)

# Khởi tạo trạng thái game (Session State)
if "game_started" not in st.session_state:
    st.session_state.game_started = False  # Trạng thái chưa bắt đầu game

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Danh sách bộ sưu tập triển lãm 7 kiệt tác độ phân giải cao
art_list = [
    {
        "title": "Đêm đầy sao (The Starry Night - Biến tấu)",
        "artist": "Vincent van Gogh",
        "meta": "Bản phối cánh đồng hoa rực rỡ sắc màu dựa trên nguyên bản 1889",
        "url": "https://unsplash.com"
    },
    {
        "title": "Mona Lisa",
        "artist": "Leonardo da Vinci",
        "meta": "Kiệt tác chân dung thời Phục Hưng kinh điển thế giới (Năm 1503)",
        "url": "https://wikimedia.org"
    },
    {
        "title": "Lady with an Ermine",
        "artist": "Leonardo da Vinci",
        "meta": "Bức chân dung vẽ nàng Cecilia Gallerani ôm con chồn trắng (Năm 1489–1490)",
        "url": "https://wikimedia.org"
    },
    {
        "title": "Skrik (The Scream - Tiếng thét)",
        "artist": "Edvard Munch",
        "meta": "Tác phẩm biểu tượng xuất sắc của trường phái biểu hiện (Năm 1893)",
        "url": "https://wikimedia.org"
    },
    {
        "title": "The Last Supper (Bữa ăn tối cuối cùng)",
        "artist": "Leonardo da Vinci",
        "meta": "Kiệt tác bích họa thâm sâu, đặt trang nghiêm ở sảnh xa nhất (Năm 1495–1498)",
        "url": "https://wikimedia.org"
    },
    {
        "title": "Girl with a Pearl Earring (Thiếu nữ đeo hoa tai ngọc trai)",
        "artist": "Johannes Vermeer",
        "meta": "Bức họa chân dung lừng danh của nền hội họa Hà Lan thế kỷ 17",
        "url": "https://wikimedia.org"
    },
    {
        "title": "Adam and Eve (Adam và Eva)",
        "artist": "Albrecht Dürer",
        "meta": "Tác phẩm tranh khắc Phục Hưng đỉnh cao cân đối hình thể (Năm 1507)",
        "url": "https://wikimedia.org"
    }
]

# --- PHẦN 1: MÀN HÌNH BẮT ĐẦU GAME (START MENU) ---
if not st.session_state.game_started:
    # Định dạng giao diện menu chào mừng sang trọng màu tối
    st.markdown(
        """
        <div style="text-align: center; margin-top: 50px; padding: 40px; background-color: #0d0d13; border-radius: 20px; border: 2px solid #d4af37; box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);">
            <h1 style="color: #d4af37; font-size: 45px; font-family: 'Georgia', serif; text-shadow: 0 0 10px rgba(212,175,55,0.5);">🏛️ VIỆN BẢO TÀNG NGHỆ THUẬT ẢO</h1>
            <p style="color: #aaa; font-size: 18px; margin-top: 10px;">Chào mừng bạn đến với chuyến hành trình khám phá 7 kiệt tác hội họa vĩ đại nhất lịch sử con người.</p>
            <p style="color: #888; font-size: 15px; font-style: italic; margin-bottom: 30px;">🎵 Nhạc nền đi kèm: Great Little Things (HauXenz - Khaen Version)</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.write("")
    st.write("")
    
    # Tạo khu vực nút bấm bắt đầu game nằm chính giữa
    col_left, col_btn, col_right = st.columns([1, 1.2, 1])
    with col_btn:
        if st.button("🏛️ BẤM VÀO ĐÂY ĐỂ BẮT ĐẦU HÀNH TRÌNH", use_container_width=True, type="primary"):
            st.session_state.game_started = True  # Đổi trạng thái để mở khóa game
            st.rerun()

# --- PHẦN 2: GIAO DIỆN CHƠI GAME CHÍNH (KHI ĐÃ BẤM NÚT START) ---
else:
    st.title("🏛️ Phòng Triển Lãm Nghệ Thuật 7 Kiệt Tác")
    st.write("Dùng các nút điều hướng bên dưới để di chuyển tham quan qua các bức tranh!")

    # TỰ ĐỘNG PHÁT NHẠC NỀN: Nhúng trình phát nhạc tự động chạy ngay khi vào game
    st.markdown(
        """
        <div style="background-color: #1a1a24; padding: 15px; border-radius: 12px; border: 1px solid #d4af37; margin-bottom: 25px;">
            <span style="color: #d4af37; font-weight: bold; font-size: 16px;">🎵 ĐANG PHÁT NHẠC NỀN: Great Little Things (HauXenz - Bản Khèn Bè lofi)</span>
            <audio src="https://catbox.moe" autoplay loop style="width: 100%; margin-top: 10px;"></audio>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Lấy dữ liệu bức tranh hiện tại dựa trên chỉ số index
    current_art = art_list[st.session_state.current_index]

    # Chia bố cục trang làm 2 cột: Cột 1 hiện tranh lớn, Cột 2 hiện thông tin giới thiệu chi tiết
    col1, col2 = st.columns([1.5, 1])

    with col1:
        # Hiển thị bức tranh căng nét, tràn viền khung hình
        st.image(current_art["url"], use_container_width=True, caption=current_art["title"])

    with col2:
        st.markdown(f"## 🖼️ {current_art['title']}")
        st.markdown(f"**Danh họa:** {current_art['artist']}")
        st.markdown(f"**Mô tả chi tiết:** {current_art['meta']}")
        
        st.divider()
        # Thêm bảng thông số danh mục triển lãm để người chơi biết đang ở bức thứ mấy
        st.metric(label="Tiến trình tham quan bảo tàng", value=f"{st.session_state.current_index + 1} / 7 Kiệt tác")
        
        # Tính năng tương tác sổ lưu niệm ghi danh người chơi
        st.markdown("✍️ **Sổ lưu niệm bảo tàng:**")
        comment = st.text_input("Để lại cảm nhận của bạn về tác phẩm này...", key=f"guest_{st.session_state.current_index}")
        if comment:
            st.success(f"Hệ thống bảo tàng đã lưu lại suy nghĩ của bạn: '{comment}'")

    st.divider()

    # Thanh nút bấm điều hướng Tiến / Lùi ở dưới cùng màn hình để người chơi bước đi tham quan
    nav_col1, nav_col2, nav_col3 = st.columns()

    with nav_col1:
        if st.button("⬅️ Quay lại bức tranh trước") and st.session_state.current_index > 0:
            st.session_state.current_index -= 1
            st.rerun()

    with nav_col3:
        if st.button("Đi tới bức tranh tiếp theo ➡️") and st.session_state.current_index < len(art_list) - 1:
            st.session_state.current_index += 1
            st.rerun()
            
    # Thêm nút bấm thoát game quay lại màn hình chính ở góc dưới
    st.write("")
    if st.button("🚪 Rời viện bảo tàng (Quay lại Menu)"):
        st.session_state.game_started = False
        st.session_state.current_index = 0
        st.rerun()
