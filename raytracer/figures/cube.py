from raytracer.utils import V3, Intersect
from raytracer.figures.plane import Plane


class Cube:
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.med = self.size / 2
        self.material = material
        self.planes = self.set_planes()

    def set_planes(self):
        planes = []

        planes.append(
            Plane(
                (self.position + V3(self.med, 0, 0)),
                V3(1, 0, 0),
                self.material
            )
        )
        planes.append(
            Plane(
                (self.position + V3(-self.med, 0, 0)),
                V3(-1, 0, 0),
                self.material
            )
        )

        planes.append(
            Plane(
                (self.position + V3(0, self.med, 0)),
                V3(0, 1, 0),
                self.material
            )
        )
        planes.append(
            Plane(
                (self.position + V3(0, -self.med, 0)),
                V3(0, -1, 0),
                self.material
            )
        )

        planes.append(
            Plane(
                (self.position + V3(0, 0, self.med)),
                V3(0, 0, 1),
                self.material
            )
        )
        planes.append(
            Plane(
                (self.position + V3(0, 0, -self.med)),
                V3(0, 0, -1),
                self.material
            )
        )

        return planes

    def ray_intersect(self, orig, direction):

        epsilon = 0.001

        minBounds = [0, 0, 0]
        maxBounds = [0, 0, 0]

        for i in range(3):
            minBounds[i] = self.position[i] - (epsilon + self.med)
            maxBounds[i] = self.position[i] + (epsilon + self.med)

        t = float('inf')
        intersect = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, direction)

            if planeInter is not None:
                if (
                    planeInter.point[0] >= minBounds[0]
                    and planeInter.point[0] <= maxBounds[0]
                ):
                    if(
                        planeInter.point[1] >= minBounds[1]
                        and planeInter.point[1] <= maxBounds[1]
                    ):
                        if(
                            planeInter.point[2] >= minBounds[2]
                            and planeInter.point[2] <= maxBounds[2]
                        ):
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

        if intersect is None:
            return None

        return Intersect(
            distance=intersect.distance,
            point=intersect.point,
            normal=intersect.normal
        )
