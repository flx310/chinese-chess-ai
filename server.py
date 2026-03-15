#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 导入 Elephantfish
from Elephantfish import Position, Searcher, parse, render, initial, A0, A9

searcher = Searcher()


def to_ef_string(board):
    """将前端棋盘转换为 Elephantfish 格式
    
    前端棋盘 (10x9):
    - board[0]: 黑方底线 (車馬象士將...)
    - board[9]: 红方底线 (車馬相仕帥...)
    
    Elephantfish 棋盘 (16x16):
    - 行 3: 黑方底线
    - 行 12: 红方底线
    
    注意：Elephantfish 默认红方（大写）走棋。
    我们需要翻转棋盘并交换大小写，让AI认为它在走红方（实际是黑方）
    """
    unicode_to_ascii = {
        '車': 'r', '馬': 'n', '相': 'b', '象': 'b', '仕': 'a', '士': 'a',
        '帥': 'k', '將': 'k', '炮': 'c', '兵': 'p', '卒': 'p'
    }
    
    # 构建 16 行，并翻转棋盘（让黑方在下，红方在上）
    # 同时交换大小写（让AI认为它在走红方）
    lines = []
    for ef_row in range(16):
        if ef_row < 3 or ef_row > 12:
            lines.append('               ')
        else:
            # EF 行 3-12 对应前端行 9-0（翻转）
            board_row = 12 - ef_row  # 翻转：EF行3->前端行9，EF行12->前端行0
            line = '   '
            for col in range(9):
                p = board[board_row][col]
                if p is None:
                    line += '.'
                else:
                    char = unicode_to_ascii.get(p['p'], '.')
                    # 交换大小写：黑方变红方，红方变黑方
                    # 这样AI会认为它在走红方（实际是黑方）
                    line += char.lower() if p['c'] else char.upper()
            line += '   '
            lines.append(line)
    
    return '\n'.join(lines) + '\n'


def ef_move_to_coords(move):
    """将 Elephantfish 走法转换为前端坐标
    
    注意：我们在 to_ef_string 中翻转了棋盘并交换了大小写。
    所以AI认为它在走红方（实际是黑方）。
    返回的坐标需要再次翻转回来。
    """
    if not move or len(move) != 2:
        return None
    
    from_idx, to_idx = move
    
    # EF 棋盘是 16x16，索引 = row * 16 + col
    from_row = from_idx // 16
    from_col = from_idx % 16
    to_row = to_idx // 16
    to_col = to_idx % 16
    
    # 转换为前端坐标 (0-9 行，0-8 列)
    # 减去左边的空白 (3列)
    from_col = from_col - 3
    to_col = to_col - 3
    
    # 减去上方的空白 (3行)
    from_row = from_row - 3
    to_row = to_row - 3
    
    # 翻转行（因为我们在 to_ef_string 中翻转了棋盘）
    # AI认为的行0实际是行9，行9实际是行0
    from_row = 9 - from_row
    to_row = 9 - to_row
    
    if 0 <= from_row < 10 and 0 <= from_col < 9 and 0 <= to_row < 10 and 0 <= to_col < 9:
        return {
            'fromRow': from_row,
            'fromCol': from_col,
            'toRow': to_row,
            'toCol': to_col
        }
    return None


@app.route('/api/move', methods=['POST', 'OPTIONS'])
def get_move():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        board = data.get('board', [])
        depth = data.get('depth', 3)
        
        if not board or len(board) != 10:
            return jsonify({'error': 'Invalid board'}), 400
        
        # 转换棋盘
        ef_board = to_ef_string(board)
        print("EF Board:")
        print(ef_board)
        print()
        
        pos = Position(ef_board, 0)
        
        # 获取所有合法走法
        moves = list(pos.gen_moves())
        print(f"Found {len(moves)} legal moves")
        
        if not moves:
            return jsonify({'error': 'No legal moves'}), 400
        
        # 使用 Elephantfish 搜索 - 增强版
        best_move = None
        max_depth = 0
        best_score = 0
        
        # 根据难度设置搜索深度
        search_depth = {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8}.get(depth, 5)
        
        for d, move, score in searcher.search(pos):
            print(f"Depth {d}: move={move}, score={score}")
            if move:
                best_move = move
                max_depth = d
                best_score = score
            if d >= search_depth:
                break
        
        # 如果搜索没找到，使用第一个合法走法
        if not best_move:
            best_move = moves[0]
            print(f"Using first legal move: {best_move}")
        
        result = ef_move_to_coords(best_move)
        print(f"Converted coords: {result}")
        
        if result:
            return jsonify({
                'move': result,
                'depth': max_depth,
                'score': 0
            })
        
        return jsonify({'error': 'Coordinate conversion failed'}), 400
        
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    return '<h1>Elephantfish Chess AI Server</h1><p>POST /api/move with JSON board</p>'


@app.route('/api/reset', methods=['POST', 'OPTIONS'])
def reset():
    global searcher
    searcher = Searcher()
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("Elephantfish AI Server")
    print(f"A0 = {A0}, A9 = {A9}")
    app.run(host='0.0.0.0', port=5000, debug=False)
