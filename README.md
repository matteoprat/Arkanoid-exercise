# Arkanoid-exercise
My own attempt to build a working arkanoid clone with python and pygame.

So far I managed to implement:
- ball physics;
- platform physics;
- 35 level of the game;
- working power-ups like those in the original game;
- all the graphics used is custom made;
- all the music is custom made execpt the destroy sound and the sound when you gain a life

- all logos used on screens belong to their respective owners (python and pygame)

DEPENDENCIES:
- PyGame

The game is still not perfect, known issues:
- sometimes the ball got stuck between golden blocks (unbreakable), I suppose it depends on bad collision handling
- the enemies only bounce up on corner and up / down, so they won't fall until nearby bricks are destroyed.

INSTRUCTIONS:

Screen menu:
  press S to see the high scores
  press I to see the game instructions
  press Enter to start the game

While playing:
  move with left - right arrows
  hit space to launch the ball
  press P to pause the game, Enter to unpause
  press M to mute the music, N to unmute
