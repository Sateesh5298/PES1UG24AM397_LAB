# Lab 4 submission notes

This folder starts with the ORIGINAL game.py and README.md from the supplied Q*bert source archive. The four coding tasks have not been pre-applied, so you can make one change, test it, and commit it separately.

## Required tasks

1. Fix `cube_center(row, col)` so the pyramid is symmetric. Inspect line 29 in the original source; the row offset currently uses `row // 2`.
2. Implement `cube_palette(level)` to return `TARGET + 1` RGB colours, or `None` to use `DEFAULT_PALETTE`.
3. Implement `on_cube_completed(cell)` for a brief completion flash or another visible completion effect. It is called only when a cube first reaches its target stage.
4. Implement `bonus_life_threshold()`; the README suggests `1000`. The score-threshold bookkeeping already exists.

## Suggested task commit messages

- `Fix Qbert pyramid projection`
- `Add level-based cube palettes`
- `Add cube completion feedback`
- `Set bonus life threshold`

## Evidence to add

- `videos/before.mp4`: real 10-second recording before code changes.
- `videos/after.mp4`: real 10-second recording after all changes.
- `chat_link.txt`: share link to the actual AI conversation.
- `chat_history.pdf`: complete exported/printed AI conversation.

Do not fabricate the videos or chat export. Keep the original `game.py` and `README.md` as the starting point; apply each task separately and commit it before moving to the next.
