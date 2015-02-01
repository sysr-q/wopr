WOPR - War Operation Plan Response
==================================

Cute little terminal widgets, backed by [drawille](https://github.com/asciimoo/drawille/).
Based on [node-blessed-contrib](https://github.com/yaronn/blessed-contrib), but
I prefer Python, and sort of thought it was silly to include the window
manager/layout stuff in that project, rather than leaving it to screen/tmux.

## Testing currently implemented widgets

```
$ python -mwopr.test.sparkline
[ displays a beautiful sinewave ]
$ python -mwopr.test.TODO
```
