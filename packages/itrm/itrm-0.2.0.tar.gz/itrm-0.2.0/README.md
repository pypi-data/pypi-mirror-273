# Interactive Terminal Utilities

```python
import itrm
```

This library provides several functions for nicely printing data to the
terminal. MatPlotLib is a very nice library, but it can be a bit tedious at
times when all you want is something quick and dirty.

-   Every separate plot needs to be introduced with a `plt.figure()` statement.
-   Large sets of data can be slow to render.
-   If you are working in full screen on the terminal, plots can pull you to
    another window which can be obnoxious.
-   The entire python program and the terminal is locked up after any
    `plt.show()` command until you close all figure windows.
-   Unless you save the figures to individual files, there is no buffer to show
    plots from past runs.
-   Sometimes it it not available, such as when running code on a server through
    SSH.

These are all excuses to use this library. But, the biggest reason to use this
library is that the terminal is cool, and the more you can do your work in the
terminal the better!

As a warning, the terminal emulator built into Neovim does seem to struggle to
correctly handle string buffering of Unicode characters. Consequently, with
`itrm.config.uni` set to `True` (the default) the plots can have garbled
characters and not display correctly. Setting the `uni` property to `False` will
remove that problem. Other terminal emulators tested do not have this problem.

## Defaults

While `itrm` does not use dotfiles, you can set some "defaults" with the
`config` class. For example, by default Unicode characters are used throughout,
but you can change this by setting `itrm.config.uni` to `False` before any other
call to `itrm`. The following table lists the configuration options:

| Setting       | Default       | Description                       |
| ---------     | :-----------: | --------------------------------- |
| `uni`         | `True`        | flag to use Unicode characters    |
| `cols`        | `60`          | default column width              |
| `rows`        | `20`          | default row height                |
| `ar`          | `0.48`        | aspect ratio of characters        |

There is also a method for changing the color map: `itrm.config.cmap()`. It
takes a string: `"colors"`, `"grays"`, `"reds"`, `"greens"`, or `"blues"`.

## Interactive Plots

```python
itrm.iplot(x, y=None, label=None, rows=1, cols=1,
        lg=None, overlay=False):
```

The `iplot` function will render all the data points defined by `x` and `y` to
the terminal. The inputs `x` and `y` can be vectors or matrices. If they are
matrices, each **row** is treated as a separate curve. Note, this is different
from MatPlotLib, in which each *column* is treated as a separate row. (This
difference is intentional, as in the author's opinion varying time along columns
means each column in a matrix can be treated as a vector. This arrangement works
very well with in linear algebra, especially matrix multiplication with a "set"
of vectors over time.)

The shapes of `x` and `y` do not have to be the same, but they must be
compatible. So, `x` could be a vector and `y` could be a matrix as long as the
length of `x` equals the number of columns of `y`.

If only `x` is given, it will be interpreted as the `y` values, and the `x`
values will be the array of indices.

When the plot is printed, the graph is rendered within a box and the ranges of
`x` and `y` are listed in the bottom left corner. So,

```
(0:99, -1.5:1.5)
```

means that `x` ranges from `0` to `99` and `y` ranges from `-1.5` to `1.5`.

If a `label` is given, this will be printed in the bottom right of the plot box.

The `rows` and `cols` parameters let you specify the number of terminal text
rows and columns to use for the plot, respectively. For each of these, if the
value is less than or equal to 1, it represents a portion of the available space
to use. For example, if `rows` is `0.5`, then half the number of rows of the
current terminal window will be used for the plot. If the value is greater than
1, it represents the absolute number of rows or columns to use. Also, if the
size of the current terminal cannot be obtained, the available space will
default to `20` rows and `60` columns. These defaults can be redefined by
changing `itrm.config.rows` and `itrm.config.cols`, respectively.

By default, this library will use Unicode symbols (specifically braille) for
plotting. A recommended font is JuliaMono. However, if your font does not
support the necessary Unicode symbols, you can tell the library to not use them
by setting `itrm.config.uni` to `False` before calling the `itrm.plot` function.
In that case, only ASCII characters will be used.

To distinguish multiple curves from each other, colors will be used. The color
map is blue, green, yellow, orange, magenta, and purple. If you have more than 6
curves (This is just a terminal-based plot; why would you do that?), then the
colors will recycle.

You can set the x or y axes to logarithmic scaling by setting the `lg` parameter
to one of `"x"`, `"y"`, or `"xy"`. Note that the values reported for the view
and the cursor will also be logarithmic.

To prevent your terminal history from extending each time a new plot is
rendered, you can print a new plot over a previous plot by setting the `overlay`
parameter to `True`. This can be especially useful when there a multiple plots
to render but you do not want your terminal history to fill up quickly.

The `iplot` function provides interactivity through a vertical cursor. You can
move the cursor left and right, at normal speed or fast speed. You can zoom in
and out. And, you can cycle through which rows of the `x` and `y` data to focus
on. Note, `iplot` is designed for monotonically-increasing `x` values, and,
consequently, does not support equal axis scaling.

![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_iplot.png)

The following table details the shortcut keys:

| Keys               | Function                 |   | Keys           | Function                 |
| :----------------: | ------------------------ | - | :------------: | ------------------------ |
| `q`, `x`, `⌫`, `↵` | exit interactive plot    |   | `j`, `s`, `↓`  | zoom in                  |
| `h`, `a`, `←`      | move cursor left         |   | `k`, `w`, `↑`  | zoom out                 |
| `l`, `d`, `→`      | move cursor right        |   | `J`, `S`, `⇧↓` | zoom in fast             |
| `H`, `A`, `⇧←`     | move cursor left fast    |   | `K`, `W`, `⇧↑` | zoom out fast            |
| `L`, `D`, `⇧→`     | move cursor right fast   |   | `n`            | next data row            |
| `g`                | move cursor to start     |   | `p`            | previous data row        |
| `G`                | move cursor to end       |   | `i`            | toggle individual view   |
| `c`, `z`           | center view on cursor    |   | `r`            | redraw the whole plot    |

## Plots

```python
itrm.plot(x, y=None, label=None, rows=1, cols=1,
        equal_axes=0, lg=None, overlay=False):
```

The `plot` function is a non-interactive version of the `iplot` function.

The `plot` function will render all the data points defined by `x` and `y` to
the terminal. The inputs `x` and `y` can be vectors or matrices. If they are
matrices, each **row** is treated as a separate curve. Note, this is different
from MatPlotLib, in which each *column* is treated as a separate row. (This
difference is intentional, as in the author's opinion varying time along columns
means each column in a matrix can be treated as a vector. This arrangement works
very well with in linear algebra, especially matrix multiplication with a "set"
of vectors over time.)

The shapes of `x` and `y` do not have to be the same, but they must be
compatible. So, `x` could be a vector and `y` could be a matrix as long as the
length of `x` equals the number of columns of `y`.

If only `x` is given, it will be interpreted as the `y` values, and the `x`
values will be the array of indices.

When the plot is printed, the graph is rendered within a box and the ranges of
`x` and `y` are listed in the bottom left corner. So,

```
(0:99, -1.5:1.5)
```

means that `x` ranges from `0` to `99` and `y` ranges from `-1.5` to `1.5`.

If a `label` is given, this will be printed in the bottom right of the plot box.

The `rows` and `cols` parameters let you specify the number of terminal text
rows and columns to use for the plot, respectively. For each of these, if the
value is less than or equal to 1, it represents a portion of the available space
to use. For example, if `rows` is `0.5`, then half the number of rows of the
current terminal window will be used for the plot. If the value is greater than
1, it represents the absolute number of rows or columns to use. Also, if the
size of the current terminal cannot be obtained, the available space will
default to `20` rows and `60` columns. These defaults can be redefined by
changing `itrm.config.rows` and `itrm.config.cols`, respectively.

By default, this library will use Unicode symbols (specifically braille) for
plotting. A recommended font is JuliaMono. However, if your font does not
support the necessary Unicode symbols, you can tell the library to not use them
by setting `itrm.config.uni` to `False` before calling the `itrm.plot` function.
In that case, only ASCII characters will be used.

To distinguish multiple curves from each other, colors will be used. The color
map is blue, green, yellow, orange, magenta, and purple. If you have more than 6
curves (This is just a terminal-based plot; why would you do that?), then the
colors will recycle.

If you want equal axis scaling, set `equal_axes` to `True`. However, since
terminal fonts are not always the same aspect ratio and because the line spacing
in your terminal might be adjustable, you can adjust the understood character
aspect ratio with `itrm.config.ar`. The default value is `0.48`. This means the
width of a character is understood to be about 0.48 of the height of a
character. Making this value larger means the characters are interpreted to be
wider, making the plot narrower horizontally. This is a feature the `iplot`
function does not share. Because the `plot` supports equal axis scaling, it does
not require that the `x` axis data monotonically increase.

You can set the x or y axes to logarithmic scaling by setting the `lg` parameter
to one of `"x"`, `"y"`, or `"xy"`. Note that the values reported for the view
will also be logarithmic.

To prevent your terminal history from extending each time a new plot is
rendered, you can print a new plot over a previous plot by setting the `overlay`
parameter to `True`. This can be especially useful when creating a live
animation.

| Single curve    | Multiple curves |
| --------------- | --------------- |
| ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_plot_1.png) | ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_plot_6.png) |

## Bars

```python
itrm.bars(x, labels=None, cols=1, fat=False)
```

It can be convenient to plot a simple bar graph. The `x` input is the vector of
values. The `labels` input is a list of strings corresponding to the labels to
print before the bar of each value in `x`. If the `cols` input is greater than
1, it is the total width of characters including the labels. If it is less than
or equal to 1, it is the portion of the terminal window width which will be used
for the graph. If the `fat` input is set to `True`, the bars will be thick.

```
 apples |=========                                         |
oranges |=========================================         |
bananas |==================================================|
  pears |====================                              |
 grapes |============================                      |
```

## Heat maps

```python
itrm.heat(matrix)
```

The `heat` function will generate a heat map of the `matrix` input using 24
shades of gray. Black is used for the lowest value and white for the highest
value. If `itrm.config.uni` is `True`, half-block characters from the Unicode
table will be used. If it is `False`, two spaces per element of the matrix will
be used.

| With Unicode      | Without Unicode     |
| ----------------- | ------------------- |
| ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_heat_uni.png) | ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_heat_ascii.png) |

## Tables

```python
itrm.table(matrix, head=None, left=None, width=10, sep='  ')
```

You can print a nicely spaced table of the `matrix` data. The `head` and `left`
inputs are lists of header and left-most column labels, respectively, to print
around the `matrix`.

```
           |      Set 1       Set 2       Set 3
---------- | ----------  ----------  ----------
    apples | 0.65802165  0.20015677  0.51074794
   bananas | 0.42184098  0.46774988  0.39589918
     pears | 0.79159879  0.89324181  0.57347394
   oranges | 0.25932644  0.29973433  0.90646047
    grapes |  0.2751687  0.40117769  0.58233234
```

## Sparsity

```python
itrm.sparsity(matrix, label='')
```

If all you want to see is the sparsity of a matrix, use this function. The
`label` input will be placed in the bottom-right corner of the render.

| With Unicode          | Without Unicode         |
| --------------------- | ----------------------- |
| ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_sparsity_uni.png) | ![](https://gitlab.com/davidwoodburn/itrm/-/raw/main/figures/fig_sparsity_ascii.png) |

## Progress bars

```python
itrm.progress(k, K, t_init=None, cols=1, fat=False)
```

There are many progress bar libraries available for Python. But, many of them
seem to be extremely over-complicated. TQDM, for example, includes over 20
source files. This library's implementation of a progress bar is a single,
one-page function. The `k` input is the counter of whatever for loop the
progress bar is reporting on. The `K` input is one greater than the largest
possible value of `k`, as in `for k in range(K):`. If `t_init` is provided, the
estimated time remaining to complete the process based on the initial time
stored in `t_init` will be displayed. When the process is completed, the total
elapsed time since `t_init` will be displayed. If `cols` is not provided, the
full width of the current terminal window will be used. If the `fat` input is
set to `True`, the bars will be thick.

```
 44% ======================----------------------------- -00:00:02.1
```
