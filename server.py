import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_code = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grandmaster Chess</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css">
    <style>
        body {
            background-color: #121212;
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
        }
        h2 { margin: 10px 0; color: #f1c40f; text-align: center; font-size: 22px; }
        #board { width: 95vw; max-width: 400px; box-shadow: 0 8px 25px rgba(0,0,0,0.8); border-radius: 8px; }
        .status { margin-top: 15px; font-size: 15px; font-weight: bold; color: #3498db; text-align: center; }
        .controls { margin-top: 15px; display: flex; gap: 10px; }
        button {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
            cursor: pointer;
        }
        button:active { background-color: #2ecc71; }
    </style>
</head>
<body>

    <h2>♔ Grandmaster Chess ♔</h2>
    <div id="board"></div>
    <div class="status" id="status">Sizning yurishingiz (Oqlar)</div>
    <div class="controls">
        <button onclick="resetGame()">Yangi O'yin</button>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js"></script>
    <script>
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
            window.setTimeout(makeAiMove, 250);
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
