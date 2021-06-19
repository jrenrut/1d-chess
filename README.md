## Calixto-Turner Notation

A CTN record contains six fields. The separator between fields is a space. The fields are:

1. Piece placement with white starting on the left. Eeach piece is identified by a single letter; i.e., P = pawn, N = knight, B = bishop, R = rook, Q = queen, K = king. White pieces are denoted using uppercase letters and black pieces use lowercase. Empty spaces are individually noted using periods.

2. Active color. "w" means White moves next, "b" means Black moves next.

3. Castling availability. If neither side can castle, this is "-". Otherwise, this has one or two letters: "K" (White can castle), and/or "k" (Black can castle). A move that temporarily prevents castling does not negate this notation.

4. En passant target square index. If there's no en passant target square, this is "-". If a pawn has just made a two-square move, this is the position "behind" the pawn. This is recorded regardless of whether there is a pawn in position to make an en passant capture.

5. Halfmove clock: The number of halfmoves since the last capture or pawn advance, used for the fifty-move rule.

6. Fullmove number: The number of the full move. It starts at 1, and is incremented after Black's move.