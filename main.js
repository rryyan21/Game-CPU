
      let board = Array(4)
        .fill()
        .map(() => Array(4).fill(""));
      let gameActive = true;

      // Create the board
      const boardDiv = document.getElementById("board");
      for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
          const cell = document.createElement("div");
          cell.className = "cell";
          cell.onclick = () => makeMove(i, j);
          boardDiv.appendChild(cell);
        }
      }

      function makeMove(row, col) {
        if (!gameActive || board[row][col]) return;

        // Player move
        board[row][col] = "O";
        updateBoard();

        if (checkWinner()) {
          document.getElementById("status").textContent = "You won!";
          gameActive = false;
          return;
        }

        if (isBoardFull()) {
          document.getElementById("status").textContent = "It's a tie!";
          gameActive = false;
          return;
        }

        // AI move
        document.getElementById("status").textContent = "AI is thinking...";

        setTimeout(() => {
          makeAIMove();
          updateBoard();

          if (checkWinner()) {
            document.getElementById("status").textContent = "AI wins!";
            gameActive = false;
          } else if (isBoardFull()) {
            document.getElementById("status").textContent = "It's a tie!";
            gameActive = false;
          } else {
            document.getElementById("status").textContent =
              "Your turn (You are O)";
          }
        }, 100);
      }

      function makeAIMove() {
        // Check if AI can win
        let move = findWinningMove("X");
        if (move) {
          board[move.row][move.col] = "X";
          return;
        }

        // Block player's winning move
        move = findWinningMove("O");
        if (move) {
          board[move.row][move.col] = "X";
          return;
        }

        // Try to create a line of three
        move = findBestStrategicMove();
        if (move) {
          board[move.row][move.col] = "X";
          return;
        }

        // Take center if available
        if (!board[1][1]) {
          board[1][1] = "X";
          return;
        } else if (!board[1][2]) {
          board[1][2] = "X";
          return;
        } else if (!board[2][1]) {
          board[2][1] = "X";
          return;
        } else if (!board[2][2]) {
          board[2][2] = "X";
          return;
        }

        // Take any available corner
        const corners = [
          [0, 0],
          [0, 3],
          [3, 0],
          [3, 3],
        ];
        for (let [row, col] of corners) {
          if (!board[row][col]) {
            board[row][col] = "X";
            return;
          }
        }

        // Take any available space
        for (let i = 0; i < 4; i++) {
          for (let j = 0; j < 4; j++) {
            if (!board[i][j]) {
              board[i][j] = "X";
              return;
            }
          }
        }
      }

      function findWinningMove(player) {
        // Check each empty cell for a winning move
        for (let i = 0; i < 4; i++) {
          for (let j = 0; j < 4; j++) {
            if (!board[i][j]) {
              board[i][j] = player;
              if (checkWinner()) {
                board[i][j] = ""; // Reset the test
                return { row: i, col: j };
              }
              board[i][j] = ""; // Reset the test
            }
          }
        }
        return null;
      }

      function findBestStrategicMove() {
        let bestScore = -Infinity;
        let bestMove = null;

        for (let i = 0; i < 4; i++) {
          for (let j = 0; j < 4; j++) {
            if (!board[i][j]) {
              let score = evaluatePosition(i, j);
              if (score > bestScore) {
                bestScore = score;
                bestMove = { row: i, col: j };
              }
            }
          }
        }
        return bestMove;
      }

      function evaluatePosition(row, col) {
        let score = 0;

        // Check row potential
        let rowCount = board[row].filter((cell) => cell === "X").length;
        score += rowCount * 2;

        // Check column potential
        let colCount = board
          .map((r) => r[col])
          .filter((cell) => cell === "X").length;
        score += colCount * 2;

        // Check diagonals
        if (row === col || row + col === 3) {
          let diag1 = [board[0][0], board[1][1], board[2][2], board[3][3]];
          let diag2 = [board[0][3], board[1][2], board[2][1], board[3][0]];
          let diagCount1 = diag1.filter((cell) => cell === "X").length;
          let diagCount2 = diag2.filter((cell) => cell === "X").length;
          score += Math.max(diagCount1, diagCount2) * 3;
        }

        return score;
      }

      function updateBoard() {
        const cells = document.getElementsByClassName("cell");
        for (let i = 0; i < 4; i++) {
          for (let j = 0; j < 4; j++) {
            const cell = cells[i * 4 + j];
            cell.textContent = board[i][j];
            cell.className = "cell " + board[i][j];
          }
        }
      }

      function checkWinner() {
        // Check rows and columns
        for (let i = 0; i < 4; i++) {
          if (
            board[i].every((cell) => cell === "O") ||
            board[i].every((cell) => cell === "X")
          )
            return true;

          let col = board.map((row) => row[i]);
          if (
            col.every((cell) => cell === "O") ||
            col.every((cell) => cell === "X")
          )
            return true;
        }

        // Check diagonals
        let diag1 = [board[0][0], board[1][1], board[2][2], board[3][3]];
        let diag2 = [board[0][3], board[1][2], board[2][1], board[3][0]];
        if (
          diag1.every((cell) => cell === "O") ||
          diag1.every((cell) => cell === "X")
        )
          return true;
        if (
          diag2.every((cell) => cell === "O") ||
          diag2.every((cell) => cell === "X")
        )
          return true;

        return false;
      }

      function isBoardFull() {
        return board.every((row) => row.every((cell) => cell !== ""));
      }

      function resetGame() {
        board = Array(4)
          .fill()
          .map(() => Array(4).fill(""));
        gameActive = true;
        updateBoard();
        document.getElementById("status").textContent = "Your turn (You are O)";
      }