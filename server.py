import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_code = """<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Global Chess Arena</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background: linear-gradient(135deg, #0f0c20 0%, #15102a 100%);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 100vh;
            padding: 12px;
            user-select: none;
        }
        .top-bar {
            width: 100%;
            max-width: 380px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .player-card { display: flex; align-items: center; gap: 8px; }
        .avatar { width: 36px; height: 36px; border-radius: 50%; background: #6c5ce7; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px; border: 2px solid #a29bfe; }
        .player-info h4 { font-size: 14px; color: #fff; }
        .player-info p { font-size: 11px; color: #00b894; font-weight: bold; }
        .prize-pool { text-align: right; }
        .prize-pool span { font-size: 10px; color: #b2bec3; text-transform: uppercase; }
        .prize-pool h3 { font-size: 15px; color: #fdcb6e; font-weight: 800; }

        .board-container {
            width: 100%;
            max-width: 360px;
            aspect-ratio: 1 / 1;
            margin: 10px 0;
            background: #2d3436;
            border-radius: 12px;
            padding: 6px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            border: 2px solid #6c5ce7;
        }
        .grid-board {
            width: 100%;
            height: 100%;
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            border-radius: 8px;
            overflow: hidden;
        }
        .cell {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 34px;
            cursor: pointer;
            transition: background 0.15s;
        }
        .cell.light { background-color: #dee3e6; color: #2d3436; }
        .cell.dark { background-color: #8c9eb2; color: #1e272e; }
        .cell.selected { background-color: #fdcb6e !important; }
        .cell.last-move { background-color: #ffeaa7 !important; }

        .status-panel {
            width: 100%;
            max-width: 380px;
            text-align: center;
            font-size: 14px;
            font-weight: 700;
            padding: 8px;
            border-radius: 8px;
            background: rgba(0, 184, 148, 0.15);
            color: #55efc4;
            border: 1px solid rgba(0, 184, 148, 0.3);
        }

        .action-buttons {
            width: 100%;
            max-width: 380px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 8px;
        }
        .btn {
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .btn-primary { background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; }
        .btn-gold { background: linear-gradient(135deg, #fdcb6e, #e17055); color: white; }
        .btn:active { transform: scale(0.96); }
    </style>
</head>
<body>

    <div class="top-bar">
        <div class="player-card">
            <div class="avatar" id="user-avatar">🏆</div>
            <div class="player-info">
                <h4 id="user-name">Shaxmatchi</h4>
                <p>Balans: $120.00</p>
            </div>
        </div>
        <div class="prize-pool">
            <span>Turnir Jamg'armasi</span>
            <h3>$5,000</h3>
        </div>
    </div>

    <div class="board-container">
        <div class="grid-board" id="board"></div>
    </div>

    <div class="status-panel" id="status-text">
        ⚡ Sizning yurishingiz (Oqlar)
    </div>

    <div class="action-buttons">
        <button class="btn btn-primary" onclick="initBoard()">🔄 Yangi O'yin</button>
        <button class="btn btn-gold" onclick="startTournament()">🏆 Turnirga Kirish</button>
    </div>

    <script>
        var tg = window.Telegram ? window.Telegram.WebApp : null;
        if (tg) {
            tg.expand();
            if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
                const user = tg.initDataUnsafe.user;
                document.getElementById('user-name').innerText = user.first_name;
                document.getElementById('user-avatar').innerText = user.first_name.charAt(0).toUpperCase();
            }
        }

        const pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        };

        const initialBoard = [
            ['r','n','b','q','k','b','n','r'],
            ['p','p','p','p','p','p','p','p'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['P','P','P','P','P','P','P','P'],
            ['R','N','B','Q','K','B','N','R']
        ];

        let boardState = [];
        let selectedSquare = null;

        function initBoard() {
            boardState = JSON.parse(JSON.stringify(initialBoard));
            selectedSquare = null;
            renderBoard();
            document.getElementById('status-text').innerText = "⚡ Sizning yurishingiz (Oqlar)";
        }

        function renderBoard() {
            const boardEl = document.getElementById('board');
            boardEl.innerHTML = '';
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const cell = document.createElement('div');
                    const isLight = (r + c) % 2 === 0;
                    cell.className = `cell ${isLight ? 'light' : 'dark'}`;
                    
                    const p = boardState[r][c];
                    cell.innerText = pieces[p] || '';

                    if (selectedSquare && selectedSquare.r === r && selectedSquare.c === c) {
                        cell.classList.add('selected');
                    }

                    cell.onclick = () => handleCellClick(r, c);
                    boardEl.appendChild(cell);
                }
            }
        }

        function handleCellClick(r, c) {
            if (selectedSquare) {
                if (selectedSquare.r === r && selectedSquare.c === c) {
                    selectedSquare = null;
                } else {
                    boardState[r][c] = boardState[selectedSquare.r][selectedSquare.c];
                    boardState[selectedSquare.r][selectedSquare.c] = '';
                    selectedSquare = null;
                    renderBoard();
                    document.getElementById('status-text').innerText = "🤖 Sun'iy Intellekt o'ylamoqda...";
                    setTimeout(makeAiMove, 400);
                    return;
                }
            } else {
                if (boardState[r][c] && boardState[r][c] === boardState[r][c].toUpperCase()) {
                    selectedSquare = { r: r, c: c };
                }
            }
            renderBoard();
        }

        function makeAiMove() {
            let moves = [];
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    if (boardState[r][c] && boardState[r][c] === boardState[r][c].toLowerCase()) {
                        moves.push({ r: r, c: c });
                    }
                }
            }
            if (moves.length === 0) return;
            let p = moves[Math.floor(Math.random() * moves.length)];
            let emptySquare = { r: 5, c: Math.floor(Math.random() * 8) };
            boardState[emptySquare.r][emptySquare.c] = boardState[p.r][p.c];
            boardState[p.r][p.c] = '';
            renderBoard();
            document.getElementById('status-text').innerText = "⚡ Sizning yurishingiz (Oqlar)";
        }

        function startTournament() {
            if (tg) {
                tg.showAlert("🏆 $5,000 mukofot jamg'armasiga ega haftalik turnirga xush kelibsiz! Har bir g'alaba uchun $10 mukofot beriladi.");
            } else {
                alert("Turnir rejimi ishga tushdi!");
            }
        }

        initBoard();
    </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_code

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
