<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Đoán Số May Mắn</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74b9ff, #a29bfe);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .game-container {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 { color: #6c5ce7; margin-bottom: 10px; }
        p { color: #2d3436; font-size: 16px; }
        input[type="number"] {
            width: 80%;
            padding: 12px;
            margin: 15px 0;
            border: 2px solid #dfe6e9;
            border-radius: 8px;
            font-size: 18px;
            text-align: center;
        }
        button {
            background-color: #6c5ce7;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover { background-color: #5b4cc4; }
        .message { margin-top: 20px; font-weight: bold; font-size: 18px; }
        .turns { color: #b2bec3; margin-top: 10px; font-size: 14px; }
        .reset-btn { background-color: #00cec9; margin-top: 15px; display: none; }
        .reset-btn:hover { background-color: #00b894; }
    </style>
</head>
<body>

<div class="game-container">
    <h1>🎯 Đoán Số May Mắn</h1>
    <p>Máy tính đã nghĩ một số từ <b>1 đến 100</b>.<br>Bạn có tối đa <b>7 lượt</b> để đoán!</p>
    
    <input type="number" id="guessInput" min="1" max="100" placeholder="Nhập số từ 1-100">
    <br>
    <button onclick="checkGuess()" id="submitBtn">Đoán thử</button>
    <button onclick="initGame()" class="reset-btn" id="resetBtn">Chơi lại 🔄</button>

    <div class="message" id="message"></div>
    <div class="turns" id="turnsLeft"></div>
</div>

<script>
    let secretChallengeNumber;
    let attemptsLeft;
    const maxAttempts = 7;

    function initGame() {
        secretChallengeNumber = Math.floor(Math.random() * 100) + 1;
        attemptsLeft = maxAttempts;
        document.getElementById("message").innerText = "";
        document.getElementById("message").style.color = "#2d3436";
        document.getElementById("turnsLeft").innerText = `Bạn còn ${attemptsLeft} lượt đoán.`;
        document.getElementById("guessInput").value = "";
        document.getElementById("guessInput").disabled = false;
        document.getElementById("submitBtn").style.display = "inline-block";
        document.getElementById("resetBtn").style.display = "none";
    }

    function checkGuess() {
        const inputElement = document.getElementById("guessInput");
        const guess = parseInt(inputElement.value);
        const messageElement = document.getElementById("message");
        const turnsElement = document.getElementById("turnsLeft");

        if (isNaN(guess) || guess < 1 || guess > 100) {
            messageElement.innerText = "❌ Vui lòng nhập số hợp lệ từ 1 đến 100!";
            messageElement.style.color = "#d63031";
            return;
        }

        attemptsLeft--;

        if (guess === secretChallengeNumber) {
            messageElement.innerText = `🎉 XUẤT SẮC!!! Bạn đã đoán đúng số ${secretChallengeNumber}!`;
            messageElement.style.color = "#2ed573";
            endGame();
        } else if (attemptsLeft === 0) {
            messageElement.innerText = `💥 Thua cuộc! Số đúng là: ${secretChallengeNumber}.`;
            messageElement.style.color = "#d63031";
            endGame();
        } else {
            if (guess < secretChallengeNumber) {
                messageElement.innerText = "📉 Thấp quá! Số bí mật lớn hơn.";
                messageElement.style.color = "#e17055";
            } else {
                messageElement.innerText = "📈 Cao quá! Số bí mật nhỏ hơn.";
                messageElement.style.color = "#e17055";
            }
            turnsElement.innerText = `Bạn còn ${attemptsLeft} lượt đoán.`;
        }
        inputElement.value = "";
        inputElement.focus();
    }

    function endGame() {
        document.getElementById("guessInput").disabled = true;
        document.getElementById("submitBtn").style.display = "none";
        document.getElementById("resetBtn").style.display = "inline-block";
        document.getElementById("turnsLeft").innerText = "";
    }

    // Khởi tạo game khi tải trang
    initGame();
</script>

</body>
</html>
