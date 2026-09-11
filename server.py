import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_code = """<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Grandmaster Chess</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 10px;
            box-sizing: border-box;
            user-select: none;
        }
        h2 { margin: 5px 0; color: #f1c40f; font-size: 22px; text-align: center; }
        .user-info { font-size: 14px; color: #8e44ad; margin-bottom: 12px; font-weight: bold; }
        #board-wrapper {
            width: 320px;
            height: 320px;
            border: 4px solid #333;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.8);
            background-color: #769656;
        }
        table {
            width: 100%;
            height: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        td {
            width: 40px;
            height: 40px;
            text-align: center;
            vertical-align: middle;
            font-size: 28px;
            cursor: pointer;
            line-height: 1;
        }
        .white { background-color: #eeeed2; color: #000; }
        .black { background-color: #769656; color: #000; }
        .selected { background-color: #f6f669 !important; }
        .status { margin-top: 15px; font-size: 16px; font-weight: bold; color: #2ecc71; text-align: center; }
        button {
            margin-top: 15px;
            background-color: #e67e22;
            color: white;
            border: none;
            padding: 10px 22px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <h2>♔ Grandmaster Chess ♔</h2>
    <div class="user-info" id="user-name">O'yinchi: Shaxmatchi</div>

    <div id="board-wrapper">
        <table id="board"></table>
    </div>

    <div class="status" id="status">Sizning yurishingiz (Oqlar)</div>
    <button onclick="initBoard()">Yangi O'yin</button>

    <script>
        var tg = window.Telegram ? window.Telegram.WebApp : null;
        if (tg) { tg.expand(); }
        if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('user-name').innerText = 'O\'yinchi: ' + tg.initDataUnsafe.user.first_name;
        }

        const pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        };

        let initialBoard = [
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
            document.getElementById('status').innerText = 'Sizning yurishingiz (Oqlar)';
        }

        function renderBoard() {
            const boardEl = document.getElementById('board');
            boardEl.innerHTML = '';
            for (let r = 0; r < 8; r++) {
                const tr = document.createElement('tr');
                for (let c = 0; c < 8; c++) {
                    const td = document.createElement('td');
                    const isWhite = (r + c) % 2 === 0;
                    td.className = isWhite ? 'white' : 'black';
                    
                    const char = boardState[r][c];
                    td.innerText = pieces[char] || '';

                    if (selectedSquare && selectedSquare.r === r && selectedSquare.col === c) {
                        td.classList.add('selected');
                    }

                    td.onclick = () => handleSquareClick(r, c);
                    tr.appendChild(td);
                }
                boardEl.appendChild(tr);
            }
        }

        function handleSquareClick(r, c) {
            if (selectedSquare) {
                if (selectedSquare.r === r && selectedSquare.col === c) {
                    selectedSquare = null;
                } else {
                    boardState[r][c] = boardState[selectedSquare.r][selectedSquare.col];
                    boardState[selectedSquare.r][selectedSquare.col] = '';
                    selectedSquare = null;
                    renderBoard();
                    setTimeout(makeAiMove, 300);
                    return;
                }
            } else {
                if (boardState[r][c] && boardState[r][c] === boardState[r][c].toUpperCase()) {
                    selectedSquare = { r: r, col: c };
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
