from raytracer.raytracing import Raytracer
from raytracer.utils import V3, Color, Light
from raytracer.figures.triangle import Triangle
from raytracer.figures.sphere import Sphere
from raytracer.figures.plane import Plane
from raytracer.figures.cube import Cube
from raytracer.material.material import EMERALD, BRICK, WOOD, GOLD, METAL


def main():
    render = Raytracer(500, 500)

    render.light = Light(
        position=V3(20, -10, 20),
        intensity=1,
        color=Color(255, 255, 255)
    )

    render.scene = [
        Plane(
            V3(0, -400, 0),
            V3(0, 1, 0),
            WOOD
        ),
        Plane(
            V3(0, 0, -400),
            V3(0, 0, 1),
            BRICK
        ),
        Cube(
            V3(20, 20, -30),
            5,
            GOLD
        ),
        Sphere(
            V3(0, 0, -50),
            20,
            EMERALD
        ),
        Triangle(
            (V3(0, -50, -100), V3(-30, -30, -100), V3(30, -30, -100)),
            GOLD
        )
    ]

    obj_model = render.load('./models/rombo.obj', (0, 0, -5), (0.3, 0.3, 0.2))

    render.scene += [
        Triangle(triangle, METAL)
        for triangle
        in obj_model
    ]

    render.render()
    render.write('render.bmp')


if __name__ == "__main__":
    main()
