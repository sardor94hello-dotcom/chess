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
        .user-info { font-size: 14px; color: #8e44ad; margin-bottom: 10px; font-weight: bold; }
        #board {
            width: 90vw;
            height: 90vw;
            max-width: 360px;
            max-height: 360px;
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            grid-template-rows: repeat(8, 1fr);
            border: 4px solid #333;
            border-radius: 6px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.8);
        }
        .square {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            cursor: pointer;
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
            padding: 10px 20px;
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

    <div id="board"></div>

    <div class="status" id="status">Sizning yurishingiz (Oqlar)</div>
    <button onclick="initBoard()">Yangi O'yin</button>

    <script>
        var tg = window.Telegram.WebApp;
        if (tg) { tg.expand(); }
        if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
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
            renderBoard();
            document.getElementById('status').innerText = 'Sizning yurishingiz (Oqlar)';
        }

        function renderBoard() {
            const boardEl = document.getElementById('board');
            boardEl.innerHTML = '';
            for (let r = 0; r < 8; r++) {
                for (let c = 0; c < 8; c++) {
                    const sq = document.createElement('div');
                    const isWhite = (r + c) % 2 === 0;
                    sq.className = `square ${isWhite ? 'white' : 'black'}`;
                    sq.dataset.row = r;
                    sq.dataset.col = c;
                    
                    const char = boardState[r][c];
                    sq.innerText = pieces[char] || '';

                    if (selectedSquare && selectedSquare.r === r && selectedSquare.col === c) {
                        sq.classList.add('selected');
                    }

                    sq.onclick = () => handleSquareClick(r, c);
                    boardEl.appendChild(sq);
                }
            }
        }

        function handleSquareClick(r, c) {
            if (selectedSquare) {
                if (selectedSquare.r === r && selectedSquare.col === c) {
                    selectedSquare = null;
                } else {
                    boardState[r][c] = boardState[selectedSquare.r][selectedSquare.col];
                    boardState[selectedSquare.r][selectedSquare.col] = '';
                    selectedSquare = nul

