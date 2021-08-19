import pygame


# definir une classe qui va s'occupe des animations
class AnimateSprite(pygame.sprite.Sprite):

    # definir les choses à faire à la création de l'entité
    def __init__(self, spriteName):
        super().__init__()
        self.image = pygame.image.load(f'{spriteName}.png')
        self.current_image = 0
        self.images = animations.get(spriteName)

    # definir une méthode pour animer le sprite
    def animate(self):
        # passer à l'image suivante
        self.current_image += 1

        # verifier si l'on a atteint la fin de l'animation
        if self.current_image >= len(self.images):
            # remmettre l'animation au départ
            self.current_image = 0

        # modifier l'image prededente par la suivante
        self.image = self.images[self.current_image]


# definir une fonction pour charger les images d'un sprite
def load_animation_images(spriteName):
    # chargement des images
    images = []
    # récupérer le chemin du dossier pour se sprite
    path = (spriteName)

    # boucler sur chaque image dans se dossier
    for num in range(1, 3):
        image_path = path + '.png'
        images.append(pygame.image.load(image_path))

    # renvoyer le contenu de la liste
    return images


# definir un dictionnaire qui va contenir les images chargées de chaque sprite
animations = {
    'player': load_animation_images('player')
}

