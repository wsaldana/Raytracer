from raytracer.utils import V3, norm, dot, Intersect


class Plane:
    def __init__(self, position: V3, normal: V3, material):
        self.position = position
        self.normal = norm(normal)
        self.material = material

    def ray_intersect(self, v_origen, direction):
        d = dot(direction, self.normal)

        if abs(d) > 0.01:
            t = dot(self.normal, self.position - v_origen) / d

            if t > 0:
                hit = v_origen + (direction * t)

                return Intersect(
                    distance=t,
                    point=hit,
                    normal=self.normal
                )

        return None
