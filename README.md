# 3D ConnectO: Term Project for 15-112 F22

Name: Riya Bhatia
Section: C

# About the Project

3D ConnectO is a fast-paced, two-player game where player compete to connect a specified number of pieces on a 3D board. As the board is created in 2.5D, meaning that the board is an isometric projection, players can connect the number of pieces on a singular grid horizontally, vertically, or diagonally, or across multiple grids in the same fashion. The game features 3D pieces, a realistic visualization of pieces being placed on their respective boards, a 2D map to better visualize open spaces to place tokens, and an exciting twist: users can pop out any piece from the bottom grid, allowing the game to take an unexpected turn!

# How to Run

Ensure that ```main.py```, ```createObjects.py```, and ```winDetection.py``` are in the same folder. Then, run ```main.py```.

Features to be Implemented:
- 3D board with clickable and responsive cells
- Both height and grid rows & cols are adjustable
- Clicking cells generates cubes, which are stackable
- Win detection is implemented (win can occur with stackable cubes, and cubes on different levels of the 3d board)
- Blue cube is wildcard that can be implemented by either player
