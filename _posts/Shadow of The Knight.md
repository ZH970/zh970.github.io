[Solutions for the exercise "Shadows of the Knight - Episode 1"](https://www.codingame.com/training/medium/shadows-of-the-knight-episode-1/solution)

Tags: Binary search Intervals

通过if分支实现二分查找，一开始简化方向导致方案不对：先竖向查找再横向，实际根据反馈再判断八个方向二分逼近，斜向比直角更快，通过逻辑复杂度换取时间复杂度。