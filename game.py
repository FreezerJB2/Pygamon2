import pygame
import pytmx
import pyscroll

from player import Player


class Game:

    def __init__(self):

        self.map = ['house', 'world']

        # creation de la fenêtre
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Pygamon - Aventure")

        # charger la carte
        self.map = 'world'
        tmxData = pytmx.util_pygame.load_pygame('carte.tmx')
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size())
        mapLayer.zoom = 3.5

        # generer un joueur
        playerPosition = tmxData.get_object_by_name('player')
        self.player = Player(playerPosition.x, playerPosition.y)

        # definir une liste qui va stocker les rectangles de collisions
        self.walls = []

        for obj in tmxData.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=5)
        self.group.add(self.player)

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmxData.get_object_by_name('enter_house_blue')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        enter_world = tmxData.get_object_by_name('switch_world_ouest_top')
        self.enter_world_rect = pygame.Rect(enter_world.x, enter_world.y, enter_world.width, enter_world.height)


    def handleInput(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_z]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_s]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_d]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_q]:
            self.player.move_left()
            self.player.change_animation('left')


    def charge_world(self, nameCarte, zoom, player, positionEntry, positionExit, map):

        # charger la carte
        tmxData = pytmx.util_pygame.load_pygame(nameCarte)
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size())
        mapLayer.zoom = zoom

        # definir une liste qui va stocker les rectangles de collisions
        self.walls = []

        for obj in tmxData.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # definir le rectangle de collision pour entrer dans la maison
        enter_house = tmxData.get_object_by_name(positionEntry)
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # définir le point de spawn devant la maison
        spawn_point = tmxData.get_object_by_name(positionExit)
        self.player.position[0] = spawn_point.x
        self.player.position[1] = spawn_point.y + 20

        print('Position modifié')

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=5)
        self.group.add(player)

        self.map = map

    def update(self):
        self.group.update()

        # verifier l'entrer dans la maison
        if self.map[0] == self.player.feet.colliderect(self.enter_house_rect):
            self.charge_world('house.tmx', self.player, 'exit_house_blue', 'spawn_house_blue', 'world')

        # verifier la sortie dans la maison
        if self.map[0] == self.player.feet.colliderect(self.enter_house_rect):
            self.charge_world('carte.tmx', self.player, 'enter_house_blue', 'enter_house_exit', 'house')

        if self.map[1] == self.player.feet.colliderect(self.enter_house_rect):
            self.charge_world('carte_Ouest.tmx', self.player, 'switch_world_middle_top', 'spawn_world_ouest_top', 'carte')
            print('Changez monde')

        if self.map[1] == self.player.feet.colliderect(self.enter_house_rect):
            self.charge_world('carte.tmx', self.player, 'switch_world_ouest_top', 'spawn_world_middle_ouest_top', 'carte_Ouest')


        # verification de la collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running:

            self.player.save_location()
            self.handleInput()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()

