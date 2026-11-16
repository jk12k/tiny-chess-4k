# tiny-chess-4k

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/jk12k/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/jk12k/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4 KB of Python for make.fun's tiny-chess-01 bounty: a 0x88 negamax with principal-variation search, quiescence, a transposition table, null-move pruning and late-move reductions, over a tapered PeSTO evaluation. It talks to the trial env over HTTP and searches a fixed node budget a move, never a clock, so every replay plays the same game.

`main.py` is the packed engine: an LZMA payload with its unpacker, under the 4,096-byte cap, which unpacks to the readable source of the engine.

## Run it

With the competition's env for a trial listening on a port, point the engine at it:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```

It plays the env's gauntlet end to end and prints the trial's wins, draws and losses on stderr.

## Credit

Piece-square tables and piece values: PeSTO's evaluation function by Ronald Friederich (RofChade/PeSTO), as published on the Chess Programming Wiki.

---

<sub>Entered on [make.fun](https://make.fun/?ref=f3jbp3zn&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
