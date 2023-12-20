# LeetCode-Gacha
Python program to use LeetCode completed question as roulette currency.

This program will be using the Python LeetCode client API https://github.com/fspv/python-leetcode. <br>
The purpose of this program is to encourage users to complete more questions via custom set prizes for the gacha roulette wheel.

To use:
1) Update the config.ini with your LeetCode session cookies
2) Update rates.ini to change your roulette rates and values
3) Run main.py from the console or main.exe from release download
4) Press the circle button in the middle of the wheel to start
![start](https://github.com/TomWu370/LeetCode-Gacha/assets/75613334/0eae6e79-2ff3-42a2-be87-88301aed3979)




Project Structure:
![Gacha](https://github.com/TomWu370/LeetCode-Gacha/assets/75613334/710e7258-a50c-4b26-9c1d-bc2683adfc45)



To build an executable yourself: <br>
1)Install pyinstaller with pip install pyinstaller <br>
2)run command in home directory, pyinstaller ./main.py --onefile --windowed

Further Improvement:
When the spinner rotates, it reflects a ghost image of itself by 180 degrees, the cause is unknown, but likely due to pygame layers
