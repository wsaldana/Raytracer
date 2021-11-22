from raytracer.utils import dot, Intersect, norm


class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, origin, direction):
        L = self.center - origin
        tca = dot(L, direction)
        len_l = L.length()
        d2 = (len_l**2) - (tca**2)

        if d2 > self.radius**2:
            return None

        thc = (self.radius**2 - d2)**(1/2)

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        hit = direction * t0 + origin
        normal = norm(hit - self.center)

        return Intersect(
            distance=t0,
            normal=normal,
            point=hit
        )
