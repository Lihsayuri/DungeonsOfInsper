#Código baseado no Handout da Aula 13 de Design de Software
# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import sys

pygame.init()
pygame.mixer.init()
# ----- Gera tela principal
WIDTH = 1500
HEIGHT = 600
CHAR_WIDTH = 200
CHAR_HEIGHT = 180
GRAVITY = 2
JUMP_SIZE = 30
GROUND = HEIGHT * 5 //6
# Define estados possíveis do jogador
STILL = 4
JUMPING = 5
FALLING = 6
ATTACK_char = 7

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dungeons of Insper')

# ---- Assets
def load_assets():
    assets={}
    assets["background"] = pygame.image.load('Dungeons/fundonormal.png').convert()
    assets["background"] = pygame.transform.scale(assets["background"], (WIDTH, HEIGHT))
    assets["char_img"]= pygame.image.load('Dungeons/teste_heroi_2.png').convert_alpha()
    assets["char_img"] = pygame.transform.scale(assets["char_img"], (CHAR_WIDTH, CHAR_HEIGHT))
    assets["char_atacc"] = pygame.image.load('Dungeons/teste_heroi.png').convert_alpha()
    assets["char_atacc"] = pygame.transform.scale(assets["char_atacc"], (CHAR_WIDTH, CHAR_HEIGHT))
    assets["mob_atacc"] = pygame.image.load('Dungeons/mob_certo.png').convert_alpha()
    assets["mob_atacc"] = pygame.transform.scale(assets["mob_atacc"], (CHAR_WIDTH - 25, CHAR_HEIGHT-40))
    assets["mob_normal"] = pygame.image.load('Dungeons/sprite_2_mob.png').convert_alpha()
    assets["mob_normal"] = pygame.transform.scale(assets["mob_normal"], (CHAR_WIDTH - 25, CHAR_HEIGHT-40))
    assets["boss"] = pygame.image.load('Dungeons/boss_bola_de_fogo-1 (1).png').convert_alpha()
    assets["boss"] = pygame.transform.scale(assets["boss"], (CHAR_WIDTH - 25, CHAR_HEIGHT-40))
    assets["fundo_boss"] = pygame.image.load('Dungeons/fundo_boss.png'). convert_alpha()
    assets["fundo_boss"] = pygame.transform.scale(assets["fundo_boss"], (WIDTH, HEIGHT))
    assets["fundo2"] = pygame.image.load('Dungeons/fundo2.png').convert_alpha()
    assets["fundo2"] = pygame.transform.scale(assets["fundo2"], (WIDTH, HEIGHT))
    assets["bola_de_fogo"] = pygame.image.load('Dungeons/bola_de_fogo.png').convert_alpha()
    assets["bola_de_fogo"] = pygame.transform.scale(assets["bola_de_fogo"], (CHAR_WIDTH - 25, CHAR_HEIGHT-40))
    pygame.mixer.music.load('Dungeons/videoplayback.ogg')
    pygame.mixer.music.set_volume(0.1)
    return assets

class Character(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)
        self.image = assets["char_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT//6 - 10
        self.speedx = 0
        self.groups = groups
        self.assets = assets
        self.rect.top = 0
        self.speedy = 0
        self.state = STILL
        self.lives = 3
        self.attacking = False
        

    def update(self):
        self.rect.x += self.speedx
        # Mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.speedy += GRAVITY
        self.rect.y += self.speedy
        # Atualiza o estado para caindo
        if self.speedy > 0:
            self.state = FALLING
        # Se bater no chão, para de cair
        if self.rect.bottom > GROUND:
            # Reposiciona para a posição do chão
            self.rect.bottom = GROUND
            # Para de cair
            self.speedy = 0
            self.state = STILL
        if self.attacking:
            self.image = self.assets["char_atacc"]
        else:
            self.image = self.assets["char_img"]

    def jump(self):
        # Só pode pular se ainda não estiver pulando ou caindo
        if self.state == STILL:
            self.speedy -= JUMP_SIZE
            self.state = JUMPING
            

class Mob(pygame.sprite.Sprite):
    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.image = assets["mob_normal"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT*5//6 - 10
        self.rect.x = random.randint(WIDTH // 2, WIDTH-CHAR_WIDTH)
        self.speedx = 1
        self.last_attack = pygame.time.get_ticks()
        self.atacou = False
        self.state = STILL

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
        now = pygame.time.get_ticks()
        if now - self.last_attack > 1000:
            if not self.atacou:
                self.atacou = True
                self.image = self.assets["mob_atacc"]
                self.state = ATTACK_char
            elif now - self.last_attack > 1500:
                self.atacou = False
                self.last_attack = now
                self.image = self.assets["mob_normal"]

class Boss(pygame.sprite.Sprite):
    def __init__(self, assets, groups):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.groups = groups
        self.image = assets["boss"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT*5//6 - 10
        self.rect.x = random.randint(WIDTH // 2, WIDTH-CHAR_WIDTH)
        self.speedx = 1
        self.last_attack = pygame.time.get_ticks()
        self.atacou = False
        self.state = STILL
     
    def shoot(self):
        new_bullet = Bullet(self.assets, self.rect.centerx, self.rect.centery)
        self.groups['all_sprites'].add(new_bullet)
        self.groups['all_bullets'].add(new_bullet)
        #self.assets['pew_sound'].play()

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
        now = pygame.time.get_ticks()
        if now - self.last_attack > 5000:
            if not self.atacou:
                self.atacou = True
                self.image = self.assets["boss"]
                self.state = ATTACK_char
                self.shoot()
            elif now - self.last_attack > 5500:
                self.atacou = False
                self.last_attack = now
                self.image = self.assets["boss"]

class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, centerx, centery):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['bola_de_fogo']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speedx = -10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y
        self.rect.x += self.speedx

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.right < 0:
            self.kill()


#-------Tela do jogo
SAIR = -1
TELA1 = 1
TELA2 = 2
TELA3 = 9
#----- Tela 1

def tela1(window):
    clock = pygame.time.Clock()
    assets = load_assets()
    FPS = 15

    all_sprites = pygame.sprite.Group()
    all_mobs = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_mobs'] = all_mobs
    player = Character(groups, assets)
    all_sprites.add(player)

    for i in range(1):
        mob = Mob(assets)
        all_sprites.add(mob)
        all_mobs.add(mob)

    DONE = 0
    PLAYING = 3
    state = PLAYING
    keys_down = {}
    #score = 0
    player.lives = 3
    pygame.mixer.music.play(loops=-1)
    while state != DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = DONE
                return SAIR
            if event.type == pygame.KEYDOWN:
                keys_down[event.key] = True
                if event.key == pygame.K_LEFT:
                    player.speedx -= 2
                if event.key == pygame.K_RIGHT:
                    player.speedx += 2
                if event.key == pygame.K_k:
                    player.attacking = True
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key in keys_down and keys_down[event.key]:
                    if event.key == pygame.K_LEFT:
                        player.speedx += 2
                    if event.key == pygame.K_RIGHT:
                        player.speedx -= 2
                    if event.key == pygame.K_k:
                        player.attacking = False
                keys_down[event.key] = False
        #Atualiza Jogo

        all_sprites.update()
        

        if state == PLAYING:
            hits = pygame.sprite.spritecollide(player, all_mobs, True, pygame.sprite.collide_mask)
            if player.attacking:
                for mob in hits:
                    mob.kill()
            else:
                for mob in hits:
                    player.lives -= 1
                    if player.lives == 0:
                        return SAIR
                        
            if len(all_mobs) == 0:
                return TELA2


        window.fill((0, 0, 0))  # Preenche com a cor preta
        window.blit(assets['background'], (0, 0))
        all_sprites.draw(window)

        pygame.display.update()

#----- Tela 2 

def tela2(window):
    clock = pygame.time.Clock()
    assets = load_assets()
    FPS = 15

    all_sprites = pygame.sprite.Group()
    all_mobs = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_mobs'] = all_mobs
    player = Character(groups, assets)
    all_sprites.add(player)

    for i in range(3):
        mob = Mob(assets) 
        all_sprites.add(mob)
        all_mobs.add(mob)

    DONE = 0
    PLAYING = 3
    state = PLAYING
    keys_down = {}
    
    pygame.mixer.music.play(loops=-1)
    
    while state != DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SAIR
            if state == PLAYING:    
                if event.type == pygame.KEYDOWN:
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 2
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 2
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        player.jump()
                    if event.key == pygame.K_k:
                        player.attacking = True
                if event.type == pygame.KEYUP:
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 2
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 2
                        if event.key == pygame.K_k:
                            player.attacking = False
                    keys_down[event.key] = False
        #Atualiza Jogo
        

        all_sprites.update()
        
        if state == PLAYING:
            hits = pygame.sprite.spritecollide(player, all_mobs, True, pygame.sprite.collide_mask)
            if player.attacking:
                for mob in hits:
                    mob.kill()
            else:
                for mob in hits:
                    player.lives -= 1
                    if player.lives == 0:
                        return SAIR

            if len(all_mobs) == 0:
                return TELA3
        
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['fundo2'], (0, 0))
        all_sprites.draw(window)

        pygame.display.update()

def tela3(window):
    clock = pygame.time.Clock()
    assets = load_assets()
    FPS = 15

    all_sprites = pygame.sprite.Group()
    all_bosses = pygame.sprite.Group()
    all_bullets = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_bosses'] = all_bosses
    groups['all_bullets'] = all_bullets
    player = Character(groups, assets)
    all_sprites.add(player)
    
    for i in range(2):
        boss = Boss(assets, groups) 
        all_sprites.add(boss)
        all_bosses.add(boss)

    DONE = 0
    PLAYING = 3
    state = PLAYING
    keys_down = {}
    
    pygame.mixer.music.play(loops=-1)
    
    while state != DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SAIR
            if state == PLAYING:    
                if event.type == pygame.KEYDOWN:
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 2
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 2
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        player.jump()
                    if event.key == pygame.K_k:
                        player.attacking = True
                if event.type == pygame.KEYUP:
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 2
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 2
                        if event.key == pygame.K_k:
                            player.attacking = False
                    keys_down[event.key] = False
        #Atualiza Jogo
        

        all_sprites.update()
        
        if state == PLAYING:
            hits = pygame.sprite.spritecollide(player, all_bosses, True, pygame.sprite.collide_mask)
            if player.attacking:
                for boss in hits:
                    boss.kill()
            else:
                for boss in hits:
                    player.lives -= 1
                    if player.lives == 0:
                        return SAIR

            if len(all_bosses) == 0:
                return SAIR
        
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['fundo_boss'], (0, 0))
        all_sprites.draw(window)

        pygame.display.update()

estado = TELA1
while estado != SAIR:
    if estado == TELA1:
        estado = tela1(window)
    elif estado == TELA2:
        estado = tela2(window)
    elif estado == TELA3:
        estado= tela3(window)    

pygame.quit()
sys.exit()

