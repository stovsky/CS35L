import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
    return (
        <button className="square" onClick={props.onClick}>
            {props.value}
        </button>
    );
}

class Board extends React.Component {
    renderSquare(i) {
        return (
            <Square
                value={this.props.squares[i]}
                onClick={() => this.props.onClick(i)}
            />
        );
    }

    render() {
        return (
            <div>
                <div className="board-row">
                    {this.renderSquare(0)}
                    {this.renderSquare(1)}
                    {this.renderSquare(2)}
                </div>
                <div className="board-row">
                    {this.renderSquare(3)}
                    {this.renderSquare(4)}
                    {this.renderSquare(5)}
                </div>
                <div className="board-row">
                    {this.renderSquare(6)}
                    {this.renderSquare(7)}
                    {this.renderSquare(8)}
                </div>
            </div>
        );
    }
}

class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            history: [
                {
                    squares: Array(9).fill(null)
                }
            ],
            stepNumber: 0,
            xIsNext: true,
            prev_index: -1
        };
    }

    handleClick(i) {
        const history = this.state.history.slice(0, this.state.stepNumber + 1);
        const current = history[history.length - 1];
        const squares = current.squares.slice();

        const prev_index = this.state.prev_index;
        
        var set_state = (same_turn) => {
            if (same_turn) {
                this.setState({
                    history: history.concat([
                        {
                            squares: squares
                        }
                    ]),
                    stepNumber: history.length,
                    xIsNext: this.state.xIsNext,
                    prev_index: i
                });
            }
            else {
                this.setState({
                    history: history.concat([
                        {
                            squares: squares
                        }
                    ]),
                    stepNumber: history.length,
                    xIsNext: !this.state.xIsNext,
                    prev_index: i
                });
            }
            return;
        }

        if (calculateWinner(squares)) {
            return;
        }

        if (this.state.stepNumber >= 6) {
            // Test that checks if a square clicked is the same as who's turn it is
            var is_same = (x) => squares[x] === (this.state.xIsNext ? "X" : "O");
            
            // Player is deciding which piece they want to move
            if (squares[prev_index]) {
                if (!is_same(i) || !squares[i]) {
                    return;
                }

                // If a valid piece is clicked, remove it but keep the same turn so it can be moved somewhere else
                squares[i] = null;
                set_state(true);
                
            // A piece has been clicked that we want to move, now we need to move it
            } else {
                
                // If the same square is clicked, just put it back and don't switch turns
                if (i === prev_index) {
                    squares[i] = this.state.xIsNext ? "X" : "O";
                    set_state(true);
                    return;
                }
                
                // If the square clicked isn't adjacent or it's occupied, it's invalid
                if (!is_adjacent(i, prev_index) || squares[i]) {
                    return;
                }
                
                // If the middle square is the same as the player's turn
                if (is_same(4)) {
                    
                    // If the spot the player clicked doesn't win, then it's invalid and can't be placed
                    squares[i] = this.state.xIsNext ? "X" : "O";
                    if (!calculateWinner(squares)) {
                        squares[i] = null;
                        return;
                    }
                }
                
                // Finally, place the piece and switch turns
                squares[i] = this.state.xIsNext ? "X" : "O";
                set_state(false);
            }
        } 
        
        // If there isn't 6 or more pieces on the board, it's just regular tic-tac-toe
        else {
            if (squares[i]) {
                return;
            }
            squares[i] = this.state.xIsNext ? "X" : "O";
            set_state(false);
        }
    }

    jumpTo(step) {
        this.setState({
            stepNumber: step,
            xIsNext: step % 2 === 0
        });
    }

    render() {
        const history = this.state.history;
        const current = history[this.state.stepNumber];
        const winner = calculateWinner(current.squares);


        let status;
        if (winner) {
            status = "Winner: " + winner;
        } else {
            status = "Next player: " + (this.state.xIsNext ? "X" : "O");
        }

        return (
            <div className="game">
                <div className="game-board">
                    <Board
                        squares={current.squares}
                        onClick={(i) => this.handleClick(i)}
                    />
                </div>
                <div className="game-info">
                    <div>{status}</div>
                </div>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));

function calculateWinner(squares) {
    const lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];
    for (let i = 0; i < lines.length; i++) {
        const [a, b, c] = lines[i];
        if (
            squares[a] &&
            squares[a] === squares[b] &&
            squares[a] === squares[c]
        ) {
            return squares[a];
        }
    }
    return null;
}

function is_adjacent(curr_i, last_i) {

    switch (curr_i) {
        case 0:
            return last_i === 1 || last_i === 3 || last_i === 4;
        case 1:
            return last_i === 0 || last_i === 2 || last_i === 4 || last_i === 3 || last_i === 5;
        case 2:
            return last_i === 1 || last_i === 4 || last_i === 5;
        case 3:
            return last_i === 0 || last_i === 1 || last_i === 4 || last_i === 6 || last_i === 7;
        case 4:
            return true;
        case 5:
            return last_i === 1 || last_i === 2 || last_i === 4 || last_i === 7 || last_i === 8;
        case 6:
            return last_i === 3 || last_i === 4 || last_i === 7;
        case 7:
            return last_i === 3 || last_i === 4 || last_i === 5 || last_i === 6 || last_i === 8;
        case 8:
            return last_i === 4 || last_i === 5 || last_i === 7;
        default:
            return;
    }

}
