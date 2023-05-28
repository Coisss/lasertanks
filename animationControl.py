class AnimationController(object):
    def __init__(self, animSeq: list, delaybtwFrames: int, sprite, loop: bool):
        self.delay = delaybtwFrames
        self.animSeq = animSeq
        self.startAnim = False
        self.sprite = sprite
        self.delayA = 0
        self.loop = loop
    def Update(self):
        
        if self.startAnim:
            
            for animimage in self.animSeq:
                
                if self.delayA == self.delay:
                    self.sprite.changeImage(animimage)
                    self.delayA = 0
                    if animimage == self.animSeq[len(self.animSeq) - 1]:
                        if self.loop == False:
                            self.Stop()
                else:
                    self.delayA += 1

        
    def Play(self):
        self.startAnim = True
    def Stop(self):
        self.startAnim = False