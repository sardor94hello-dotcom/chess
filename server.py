import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_code = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Grandmaster Chess</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
    <style>
        body {
            background-color: #1a1a1a;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
        .header {
            text-align: center;
            margin-bottom: 15px;
        }
        h2 { margin: 5px 0; color: #f1c40f; font-size: 22px; }
        .user-info { font-size: 14px; color: #bdc3c7; }
        #board {
            width: 90vw;
            max-width: 380px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            border-radius: 6px;
            overflow: hidden;
        }
        .status {
            margin-top: 15px;
            font-size: 15px;
            font-weight: 600;
            color: #2ecc71;
            text-align: center;
            min-height: 22px;
        }
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        button {
            background-color: #e67e22;
            color: white;
            border: none;
            padding: 10px 18px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
        }
        button:active { transform: scale(0.96); }
    </style>
</head>
<body>

    <div class="header">
        <h2>♔ Grandmaster Chess ♔</h2>
        <div class="user-info" id="user-name">O'yinchi: Shaxmatchi</div>
    </div>

    <div id="board"></div>

    <div class="status" id="status">Sizning yurishingiz (Oqlar)</div>

    <div class="controls">
        <button onclick="resetGame()">Yangi O'yin</button>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>
    <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
    <script>
        var tg = window.Telegram.WebApp;
        tg.expand();

        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('user-name').innerText = 'O\'yinchi: ' + tg.initDataUnsafe.user.first_name;
        }

        var board = null;
        var game = new Chess();

        function makeAiMove() {
            var moves = game.moves();
            if (moves.length === 0) return;
            var randomMove = moves[Math.floor(Math.random() * moves.length)];
            game.move(randomMove);
            board.position(game.fen());
            updateStatus();
        }

        function onDragStart (source, piece, position, orientation) {
            if (game.game_over()) return false;
            if (piece.search(/^b/) !== -1) return false;
        }

        function onDrop (source, target) {
            var move = game.move({
                from: source,
                to: target,
                promotion: 'q'
            });

            if (move === null) return 'snapback';
            updateStatus();
            window.setTimeout(makeAiMove, 300);
        }

        function onSnapEnd () {
            board.position(game.fen());
        }

        function updateStatus () {
            var status = '';
            var moveColor = 'Oqlar';
            if (game.turn() === 'b') { moveColor = 'Qoralar (AI)'; }

            if (game.in_checkmate()) {
                status = 'O\'yin tugadi, ' + moveColor + ' mot bo\'ldi.';
            } else if (game.in_draw()) {
                status = 'O\'yin durang bilan tugadi.';
            } else {
                status = moveColor + ' yurishi';
                if (game.in_check()) { status += ', SHAX!'; }
            }
            $('#status').html(status);
        }

        function resetGame() {
            game.reset();
            board.start();
            updateStatus();
        }

        var config = {
            draggable: true,
            position: 'start',
            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png',
            onDragStart: onDragStart,
            onDrop: onDrop,
            onSnapEnd: onSnapEnd
        };
        board = Chessboard('board', config);
        updateStatus();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_code

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
