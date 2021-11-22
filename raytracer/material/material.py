from raytracer.utils import Color
from raytracer.texture.texture import Texture


class Material:
    def __init__(
            self,
            diffuse: Color,
            albedo: list,
            spec: int,
            refractive_index: int = 0,
            texture: Texture = None
    ):
        self.albedo = albedo
        self.diffuse = diffuse
        self.spec = spec
        self.refractive_index = refractive_index
        self.texture = texture


WOOD = Material(
    diffuse=Color(200, 165, 125),
    albedo=[0.3, 0.3, 0.1, 0],
    spec=0
)
GOLD = Material(
    diffuse=Color(85, 50, 0),
    albedo=[0.8, 1, 10, 5],
    spec=200
)
METAL = Material(
    diffuse=Color(60, 60, 80),
    albedo=[0.1, 5, 6, 3],
    spec=100
)
BRICK = Material(
    diffuse=Color(200, 100, 60),
    albedo=[0.3, 0.3, 0.1, 0],
    spec=0
)
MIRROR = Material(
    diffuse=Color(255, 255, 255),
    albedo=[0, 10, 0.8, 0],
    spec=1500
)
EMERALD = Material(
    diffuse=Color(0, 160, 100),
    albedo=[0, 1, 10, 10],
    spec=500,
    refractive_index=1.57
)
DIRTH = Material(
    diffuse=Color(85, 45, 65),
    albedo=[0.6, 0.3, 0.1, 0],
    spec=50,
    texture=Texture('./models/grass_block_tex.bmp')
)
