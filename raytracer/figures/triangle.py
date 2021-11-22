from raytracer.utils import dot, barycentric, Intersect, norm, cross


class Triangle:
    def __init__(self, vertices, material):
        self.vertices = vertices
        self.material = material

    def ray_intersect(self, origin, direction):
        e = 0.001
        v0, v1, v2 = self.vertices
        normal = cross(
            (v1 - v0),
            (v2 - v0)
        )
        determinant = dot(normal, direction)

        if abs(determinant) < e:
            return None

        distance = dot(normal, v0)
        t = (dot(normal, origin) + distance) / determinant
        if t < 0:
            return None

        point = direction * t + origin
        u, v, w = barycentric(v0, v1, v2, point)

        if w < 0 or v < 0 or u < 0:
            return None

        return Intersect(
            distance=distance,
            point=point,
            normal=norm(normal)
        )
