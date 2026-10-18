// Chạy game lần đầu
renderMuseum();
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎨 Cuộc Phiêu Lưu Tại Bảo Tàng 7 Kiệt Tác</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a24;
            color: #f5f6fa;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        h1 {
            color: #f1c40f;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin-bottom: 5px;
        }

        .subtitle {
            color: #dcdde1;
            margin-bottom: 25px;
            font-style: italic;
        }

        .museum-hall {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            max-width: 1000px;
            width: 100%;
        }

        .gallery-item {
            background-color: #2f3640;
            border: 4px solid #dcdde1;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s, border-color 0.3s;
            position: relative;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }

        .gallery-item:hover {
            transform: translateY(-5px);
            border-color: #f1c40f;
        }

        .art-frame {
            height: 150px;
            background-color: #1e222b;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 40px;
            border-radius: 4px;
            margin-bottom: 10px;
        }

        .art-title {
            font-weight: bold;
            font-size: 16px;
            margin-top: 8px;
        }

        .status-badge {
            margin-top: 10px;
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }

        .locked { background-color: #e74c3c; color: white; }
        .unlocked { background-color: #2ecc71; color: white; }

        /* Modal hiển thị câu hỏi và thông tin */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0,0,0,0.8);
            justify-content: center;
            align-items: center;
            z-index: 10;
        }

        .modal-content {
            background-color: #2f3640;
            padding: 30px;
            border-radius: 12px;
            max-width: 500px;
            width: 90%;
            text-align: center;
            border: 2px solid #f1c40f;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }

        .quiz-option {
            background-color: #353b48;
            color: white;
            border: 1px solid #718093;
            padding: 10px 15px;
            margin: 8px 0;
            width: 100%;
            border-radius: 6px;
            cursor: pointer;
            font-size: 15px;
            transition: 0.2s;
        }

        .quiz-option:hover {
            background-color: #718093;
        }

        .close-btn {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 15px;
            font-weight: bold;
        }

        .victory-msg {
            margin-top: 25px;
            padding: 15px;
            background-color: #27ae60;
            border-radius: 8px;
            text-align: center;
            max-width: 400px;
            display: none;
            font-size: 18px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

    <h1>🏛️ BẢO TÀNG 7 KIỆT TÁC</h1>
    <p class="subtitle">Bấm vào từng khung tranh, trả lời câu hỏi để mở khóa khám phá tuyệt tác thế kỷ!</p>

    <div class="museum-hall" id="museumHall">
        <!-- Các bức tranh sẽ tự động render bằng Javascript ở đây -->
    </div>

    <div class="victory-msg" id="victoryMessage">
        🎉 Chúc mừng nhà thám hiểm! Bạn đã giải mã thành công toàn bộ 7 kiệt tác nghệ thuật của nhân loại!
    </div>

    <!-- Hộp thoại tương tác (Modal) -->
    <div class="modal" id="artModal">
        <div class="modal-content" id="modalContent">
            <!-- Nội dung thay đổi động -->
        </div>
    </div>

<script>
    // Dữ liệu cấu trúc trò chơi cho 7 kiệt tác
    const masterpieces = [
        {
            id: 1,
            title: "Đêm đầy sao",
            emoji: "🌌",
            unlocked: false,
            question: "Bức họa 'Đêm đầy sao' (The Starry Night) là tác phẩm của danh họa thiên tài nào?",
            options: ["Claude Monet", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci"],
            answer: "Vincent van Gogh",
            info: "Chính xác! Bức tranh vẽ lại khung cảnh từ cửa sổ phòng bệnh của Van Gogh tại Pháp, thể hiện tâm hồn đầy biến động nhưng ngập tràn khát vọng của ông thông qua các nét cọ xoáy bùng nổ."
        },
        {
            id: 2,
            title: "Cô gái và chiếc bông tai ngọc trai",
            emoji: "🧕",
            unlocked: false,
            question: "Bức họa này thường được ví von là gì của Bắc Âu?",
            options: ["Mona Lisa của Bắc Âu", "Nữ thần Tự Do", "Kiệt tác bóng đêm", "Nàng thơ Hà Lan"],
            answer: "Mona Lisa của Bắc Âu",
            info: "Tuyệt vời! Tác phẩm của Johannes Vermeer nổi tiếng với cách xử lý ánh sáng chân thực, điểm nhấn tinh tế vào chiếc bông tai ngọc trai lấp lánh phản chiếu quyến rũ."
        },
        {
            id: 3,
            title: "Cô gái và con chồn",
            emoji: "🦦",
            unlocked: false,
            question: "Ai là tác giả của bức chân dung 'Cô gái và con chồn'?",
            options: ["Michelangelo", "Raphael", "Leonardo da Vinci", "Rembrandt"],
            answer: "Leonardo da Vinci",
            info: "Đúng rồi! Đây là một trong số ít những bức chân dung phụ nữ do Leonardo da Vinci vẽ, thể hiện kỹ thuật giải phẫu động vật và người vô cùng điêu luyện."
        },
        {
            id: 4,
            title: "Bữa tối cuối cùng",
            emoji: "🍞",
            unlocked: false,
            question: "Bức tranh 'Bữa tối cuối cùng' (The Last Supper) được vẽ trực tiếp lên bề mặt kiến trúc nào?",
            options: ["Trần nhà nguyện", "Bức tường tu viện", "Mặt trống đồng", "Cánh cửa nhà thờ"],
            answer: "Bức tường tu viện",
            info: "Chính xác! Danh họa Leonardo da Vinci đã vẽ kiệt tác này trên tường phòng ăn của tu viện Santa Maria delle Grazie ở Milan, Ý."
        },
        {
            id: 5,
            title: "Tiếng thét",
            emoji: "😱",
            unlocked: false,
            question: "Bức họa 'Tiếng thét' (The Scream) phản ánh trường phái nghệ thuật nào?",
            options: ["Trường phái Ấn tượng", "Trường phái Lập thể", "Trường phái Biểu hiện", "Trường phái Hiện thực"],
            answer: "Trường phái Biểu hiện",
            info: "Chuẩn luôn! Edvard Munch đã khắc họa nỗi lo âu, cô độc tột cùng của con người hiện đại thông qua bầu trời đỏ như máu và gương mặt biến dạng vì hoảng sợ."
        },
        {
            id: 6,
            title: "Adam và Eva",
            emoji: "🍎",
            unlocked: false,
            question: "Albrecht Dürer nổi tiếng với bức tranh khắc 'Adam và Eva'. Ông là họa sĩ thuộc quốc gia nào?",
            options: ["Đức", "Ý", "Tây Ban Nha", "Pháp"],
            answer: "Đức",
            info: "Rất tốt! Albrecht Dürer là nghệ sĩ vĩ đại của thời kỳ Phục hưng phương Bắc (Đức), đưa tỷ lệ hình thể lý tưởng vào các tác phẩm đồ họa điêu luyện."
        },
        {
            id: 7,
            title: "Mona Lisa",
            emoji: "🖼️",
            unlocked: false,
            question: "Điểm đặc biệt nổi tiếng nhất khiến cả thế giới tò mò trên gương mặt của nàng Mona Lisa là gì?",
            options: ["Đôi mắt biết khóc", "Nụ cười bí ẩn", "Không có chân mày", "Vòng cổ kim cương"],
            answer: "Nụ cười bí ẩn",
            info: "Hoàn toàn chính xác! Kỹ thuật làm nhòa mờ (Sfumato) của Leonardo da Vinci tạo nên hiệu ứng thị giác kỳ lạ: nụ cười của nàng dường như thay đổi tùy thuộc vào góc nhìn của bạn!"
        }
    ];

    let currentArtIndex = null;

    // Hiển thị danh sách các bức tranh ra sảnh bảo tàng
    function renderMuseum() {
        const hall = document.getElementById("museumHall");
        hall.innerHTML = "";
        
        masterpieces.forEach((art, index) => {
            const card = document.createElement("div");
            card.className = "gallery-item";
            card.onclick = () => openArt(index);
            
            card.innerHTML = `
                <div class="art-frame">${art.unlocked ? art.emoji : "🔒"}</div>
                <div class="art-title">${art.title}</div>
                <span class="status-badge ${art.unlocked ? 'unlocked' : 'locked'}">
                    ${art.unlocked ? "Đã khám phá ✓" : "Đang bị khóa"}
                </span>
            `;
            hall.appendChild(card);
        });

        // Kiểm tra xem tất cả đã được mở khóa chưa
        const allUnlocked = masterpieces.every(art => art.unlocked);
        if (allUnlocked) {
            document.getElementById("victoryMessage").style.display = "block";
        }
    }

    // Mở hộp thoại khi click vào tranh
    function openArt(index) {
        currentArtIndex = index;
        const art = masterpieces[index];
        const modal = document.getElementById("artModal");
const content = document.getElementById("modalContent");
modal.style.display = "flex";
if (art.unlocked) {
// Nếu đã mở khóa trước đó, chỉ hiển thị thông tin kiến thức
content.innerHTML = <h2>${art.emoji} Kiệt tác: ${art.title}</h2> <p style="text-align: left; line-height: 1.6; background: #1e222b; padding: 15px; border-radius: 8px;"> ${art.info} </p> <button class="close-btn" onclick="closeModal()">Đóng cửa sổ</button>;
} else {
// Nếu chưa mở khóa, hiển thị câu đố thử thách
let optionsHTML = "";
art.options.forEach(opt => {
optionsHTML += <button class="quiz-option" onclick="submitAnswer('${opt}')">${opt}</button>;
});
content.innerHTML = <h2>🔒 Thử thách giải mã: ${art.title}</h2> <p style="font-size: 16px; margin: 15px 0; color: #f1c40f;">${art.question}</p> <div style="margin-bottom: 10px;">${optionsHTML}</div> <button class="close-btn" style="background-color:#718093;" onclick="closeModal()">Rút lui</button>;
}
}
// Kiểm tra câu trả lời của người chơi
function submitAnswer(selectedOption) {
const art = masterpieces[currentArtIndex];
const content = document.getElementById("modalContent");
if (selectedOption === art.answer) {
art.unlocked = true;
renderMuseum(); // Cập nhật lại giao diện sảnh
content.innerHTML = <h2>🎉 CHÍNH XÁC! 🎉</h2> <p style="color: #2ecc71; font-weight: bold; font-size: 18px;">Bạn đã mở khóa thành công!</p> <p style="text-align: left; line-height: 1.6; background: #1e222b; padding: 15px; border-radius: 8px;"> ${art.info} </p> <button class="close-btn" onclick="closeModal()">Tiếp tục tham quan</button>;
} else {
content.innerHTML = <h2>❌ SAI RỒI! ❌</h2> <p style="color: #e74c3c;">Bảo vệ bảo tàng đã ngăn bạn lại. Hãy thử suy luận một cách khác xem!</p> <button class="close-btn" onclick="openArt(${currentArtIndex})">Thử lại</button> <button class="close-btn" style="background-color:#718093; margin-left: 10px;" onclick="closeModal()">Quay lại sảnh</button>;
}
}
function closeModal() {
document.getElementById("artModal").style.display = "none";
}
