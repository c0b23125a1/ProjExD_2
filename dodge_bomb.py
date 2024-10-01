import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), pg.K_DOWN: (0, 5), 
         pg.K_LEFT: (-5, 0), pg.K_RIGHT: (5, 0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect)  ->  tuple[bool, bool]:  # pg.Rect型だと定義するとtop,leftなどが認識される
    """
    引数: こうかとんrct or 爆弾rct
    戻り値: 横方向と縦判定の真理値タプル
    画面内:True 画面外: False
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        yoko = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        tate = False
    return yoko, tate


def game_over(screen:pg.Surface)->None:
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(150)
    go_rct = go_img.get_rect()
    screen.blit(go_img, go_rct)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.centerx = WIDTH//2
    txt_rct.centery = HEIGHT//2
    screen.blit(txt, txt_rct)

    nakuton = pg.image.load("fig/8.png")
    screen.blit(nakuton, [350, 300])
    screen.blit(nakuton, [710, 300])
    pg.display.update()
    time.sleep(5)


# def zouka():
#     accs = [a for a in range(1, 11)]

#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)

#         avx = 

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_image = pg.Surface((20, 20))
    bb_image.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_image, (255,0,0), (10,10), 10)  # 赤、ｘ１０ｙ１０、半径１０
    bb_rct = bb_image.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なった場合
            game_over(screen)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # ヨコ方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_image, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
