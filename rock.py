import pygame
import random
import sys
import math

pygame.init()

################################ Temel Ayarlar ###########################################
width, height = 1080, 920
obj_size = 20
game_speed = 45
obj_num = 120
##########################################################################################
font = pygame.font.SysFont(None, 96)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Taş-Kağıt-Makas")

object_type = ["rock", "paper", "scissors"]

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

objects = []
obj_counter = 0

# Obje resimleri import etme

rockImg = pygame.image.load("rock.png")
paperImg = pygame.image.load("paper.png")
scissorsImg = pygame.image.load("scissors.png")

rockImg = pygame.transform.scale(rockImg, (obj_size, obj_size))
paperImg = pygame.transform.scale(paperImg, (obj_size, obj_size))
scissorsImg = pygame.transform.scale(scissorsImg, (obj_size, obj_size))

# Oyun sonu obje sayıları

rock = 0
paper = 0
scissors = 0


# Oyun kodları

class GameObject:
    def __int__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = random.randint(1, 5)  # obje hızı
        self.angle = random.uniform(0, 360)  # objenin açısı
        self.type = random.choice(object_type)

        # Obje türüne göre resim atama
        if self.type == "rock":
            self.image = rockImg
        elif self.type == "paper":
            self.image = paperImg
        elif self.type == "scissors":
            self.image = scissorsImg

        # resim boyutunu ayarlama
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))

    # Hareket fonksiyonu
    def move(self):
        # obje hareket vektörünü hesaplama
        dx = self.speed * math.cos(math.radians(self.angle))
        dy = self.speed * math.sin(math.radians(self.angle))

        # obje hareket vektörünü uygula
        self.rect.x += dx
        self.rect.y += dy

        # Obje duvarlardan sekerse hareket yönünü tersine çevir
        if self.rect.left <= 0 or self.rect.right >= width:
            self.angle = 180 - self.angle
        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.angle = -self.angle

        # Duvara yapışmasın önlemek için objeyi düzenle
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height

    # Objeyi ekrana çizdirme
    def draw(self):
        if self.image:
            if self.type == "rock":
                screen.blit(rockImg, self.rect)
            elif self.type == "paper":
                screen.blit(paperImg, self.rect)
            elif self.type == "scissors":
                screen.blit(scissorsImg, self.rect)

        # resim olmama durumunda renk ata
        else:
            if self.type == "rock":
                pygame.draw.rect(screen, red, self.rect)
            elif self.type == "paper":
                pygame.draw.rect(screen, blue, self.rect)
            elif self.type == "scissors":
                pygame.draw.rect(screen, green, self.rect)


# Rast gele obje oluşturma

def create_random_object():
    return GameObject(
        random.randint(10, width - 100),
        random.randint(10, height - 100),
        obj_size,
        obj_size
    )

# Objelerin çarpışmasını kontrol etme
def check_collision(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect)


def handle_collision(obj1, obj2):
    overlap = obj1.rect.clip(obj2.rect).width
    if overlap > 0:
        angle = math.atan2(obj2.rect.centery - obj1.rect.centery, obj2.rect.centerx - obj1.rect.centerx)
        offset_x = int(overlap / 2 * math.cos(angle))
        offset_y = int(overlap / 2 * math.sin(angle))
        obj1.rect.x -= offset_x
        obj1.rect.y -= offset_y
        obj2.rect.x += offset_x
        obj2.rect.y += offset_y


# Nesnelerin çarpışmaya göre dönüşmesi
def object_changing(obj1, obj2):
    check = obj1.rect.colliderect(obj2.rect.inflate(20, 20))

    # işi garantiye almak için bütün kombinasyonları yazmalyız
    if check:
        if obj1.type == "rock" and obj2.type == "paper":
            obj1.type = "paper"
        elif obj1.type == "rock" and obj2.type == "scissors":
            obj2.type = "rock"
        elif obj1.type == "paper" and obj2.type == "scissors":
            obj1.type = "scissors"
        elif obj1.type == "paper" and obj2.type == "rock":
            obj2.type = "paper"
        elif obj1.type == "scissors" and obj2.type == "paper":
            obj2.type = "scissors"
        elif obj1.type == "scissors" and obj2.type == "rock":
            obj1.type = "rock"


# Oyun Döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    while obj_counter < obj_num:
        obj = create_random_object()
        objects.append(obj)
        obj_counter += 1

    screen.fill(white)

    for obj in objects:
        obj.move()
        obj.draw()

    for i in range(len(objects)):
        if objects[i].type == "rock":
            rock += 1
        elif objects[i].type == "paper":
            paper += 1
        elif objects[i].type == "scissors":
            scissors += 1

        # Obje çarpışma ve değişme fonksiyonlarını uygulanması
        for j in range(len(objects)):
            if check_collision(objects[i], objects[j]):
                handle_collision(objects[i], objects[j])
            object_changing(objects[i], objects[j])

    # Oyun içindeki nesnlerinin sayısına göre kazananın belirlenilmesi
    if (rock == 0) and (paper == 0) and (scissors > 0):
        end_text = font.render("Makas Kazandı", True, black)
        text_rect = end_text.get_rect(center=(width // 2, height // 2))
        screen.blit(end_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(5000)  # 5 saniye duraksama
        pygame.quit()
        sys.exit()
    elif (rock == 0) and (paper > 0) and (scissors == 0):
        end_text = font.render("Kağıt Kazandı", True, black)
        text_rect = end_text.get_rect(center=(width // 2, height // 2))
        screen.blit(end_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(5000)  # 5 saniye duraksama
        pygame.quit()
        sys.exit()
    elif (rock > 0) and (paper == 0) and (scissors == 0):
        end_text = font.render("Taş Kazandı", True, black)
        text_rect = end_text.get_rect(center=(width // 2, height // 2))
        screen.blit(end_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(5000)  # 5 saniye duraksama
        pygame.quit()
        sys.exit()

    # Her döngüden sonra nesne sayacını sıfırla
    rock = 0
    paper = 0
    scissors = 0

    pygame.display.flip()
    pygame.time.Clock().tick(game_speed)
