import psp2d, pspos
import time


def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


CLEAR_COLOR = psp2d.Color(0,0,0,255)

pspos.setclocks(333,166)
psp_scr  = psp2d.Screen()
psp_font = psp2d.Font('font.png')
n = 0


def update_result(valor, calculate=None):
    global n
    n += valor
    psp_scr.clear(CLEAR_COLOR)
    psp_font.drawText(psp_scr, 200, 0, "..: Fibonacci :..")
    psp_font.drawText(psp_scr, 100, 15, "Press O to get out")
    psp_font.drawText(psp_scr, 100, 30, "Press X to calculate")
    psp_font.drawText(psp_scr, 100, 45, "Press <triangle> to restart")
    psp_font.drawText(psp_scr, 100, 60, "Use R and L to add or subtract the number")
    psp_font.drawText(psp_scr, 100, 80, "Fibonacii of %d" % n)
    if calculate:
        psp_font.drawText(psp_scr, 200, 200, "Result: %d" % fib(n))
    psp_scr.swap()


def main():
    update_result(0)
    while True:
        pad = psp2d.Controller()
        time.sleep(0.07) # pra evitar apertar uma vez e entender como varias
        if pad.circle:
            return
        elif pad.triangle:
            update_result(-n)
        elif pad.cross:
            update_result(0, True)
        elif pad.l:
            update_result(-1)
        elif pad.r:
            update_result(+1)


if __name__ == '__main__':
    main()
