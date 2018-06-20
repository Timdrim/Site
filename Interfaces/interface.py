import ObjectOrientedMath.MathObjects as MathObjects

class IDrawableRectangle(object):

    def __init__(self,
                 center_position: MathObjects.Point,
                 size: MathObjects.Point,
                 color=None,
                 thickness=None):

        self.center_position = center_position
        self.size = size
        self.color = color
        self.thickness = thickness

