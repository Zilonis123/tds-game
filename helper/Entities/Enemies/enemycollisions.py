

# self is gonna be the enemy

def check_collisions(self, render):
    # enemies
    for e in render.enemies:
        if e == self:
            continue
        
        if e.rect.colliderect(self.rect):
            handlecollision(self, e.rect)
            self.targetTurret = None

    # turrets
    for t in render.turrets:
        # if it isnt our target
        if t.rect.colliderect(self.rect) and t.uid != self.targetTurret:
            handlecollision(self, t.rect)


def handlecollision(self, rect2):
    rect1 = self.rect.copy()

    overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
    overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)

    if overlap_x > 0 and overlap_y > 0:
        if overlap_x < overlap_y:
            if rect1.centerx < rect2.centerx:
                rect1.right = rect2.left
            else:
                rect1.left = rect2.right
        else:
            if rect1.centery < rect2.centery:
                rect1.bottom = rect2.top
            else:
                rect1.top = rect2.bottom
    self.rect = rect1