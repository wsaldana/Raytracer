from random import random
from math import pi, tan

from raytracer.utils import char, dword, word
from raytracer.utils import V3, Color, norm, dot, reflect, refract, transform
from raytracer.obj.obj import Obj


# RUN PARAMETERS
RAND_VAL = 0
MAX_RECURSION_DEPTH = 4

# CONSTANTS
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)


class Raytracer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg_color = BLACK
        self.light = None
        self.clear()

    def clear(self):
        self.pixels = [
                [
                    BLACK
                    for _
                    in range(self.width)
                ]
                for _ in range(self.height)
            ]

    def write(self, filename):
        with open(filename, 'bw') as f:
            # File header
            f.write(char('B'))
            f.write(char('M'))
            f.write(dword(14 + 40 + 3*(self.width * self.height)))
            f.write(dword(0))
            f.write(dword(14 + 40))
            # Info Header
            f.write(dword(40))
            f.write(dword(self.width))
            f.write(dword(self.height))
            f.write(word(1))
            f.write(word(24))
            f.write(dword(0))
            f.write(dword((self.width * self.height) * 3))
            f.write(dword(0))
            f.write(dword(0))
            f.write(dword(0))
            f.write(dword(0))

            for y in range(self.height):
                for x in range(self.width):
                    try:
                        f.write(self.pixels[y][x].toBytes())
                    except:
                        pass

            f.close()

    def point(self, x, y, col):
        self.pixels[y][x] = col

    def cast_ray(self, origin, direction, recursion=0):
        material, intersect = self.scene_intersect(origin, direction)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            return self.bg_color

        light_dir = norm(self.light.position - intersect.point)

        offset_normal = intersect.normal * 0.1
        shadow_orig = (
            intersect.point + offset_normal
            if dot(light_dir, intersect.normal) >= 0
            else intersect.point - offset_normal
        )

        shadow_material, shadow_intersect = self.scene_intersect(
            shadow_orig, light_dir
        )

        if shadow_material is None:
            shadow_intensity = 0
        else:
            shadow_intensity = 0.9

        if material.albedo[2] > 0:
            reverse_direction = direction * -1
            reflect_direction = reflect(reverse_direction, intersect.normal)
            reflect_orig = (
                intersect.point + offset_normal
                if dot(reflect_direction, intersect.normal) >= 0
                else intersect.point - offset_normal
            )

            reflect_color = self.cast_ray(
                reflect_orig, reflect_direction,
                recursion + 1
            )

        else:
            reflect_color = Color(0, 0, 0)

        if material.albedo[3] > 0:
            refract_direction = refract(
                direction,
                intersect.normal,
                material.refractive_index
            )

            if refract_direction is not None:
                refract_orig = (
                    intersect.point + offset_normal
                    if dot(reflect_direction, intersect.normal) >= 0
                    else intersect.point - offset_normal
                )
                refract_color = self.cast_ray(
                    refract_orig,
                    refract_direction,
                    recursion + 1
                )
            else:
                refract_color = Color(0, 0, 0)

        else:
            refract_color = Color(0, 0, 0)

        diffuse_intensity = (
            self.light.intensity
            * max(0, dot(light_dir, intersect.normal))
            * (1 - shadow_intensity)
        )

        if shadow_intensity > 0:
            specular_intensity = 0
        else:
            specular_reflection = reflect(light_dir, intersect.normal)
            specular_intensity = (
                self.light.intensity
                * (
                    max(0, dot(specular_reflection, direction))
                    ** material.spec
                )
            )

        diffuse = material.diffuse * diffuse_intensity * material.albedo[0]
        specular = self.light.color * specular_intensity * material.albedo[1]
        reflection = reflect_color * material.albedo[2]

        refraction = refract_color * material.albedo[3]

        if material.texture and intersect.text_coords:
            text_color = material.texture.get_color(
                intersect.text_coords[0],
                intersect.text_coords[1]
            )
            diffuse = text_color * 255

        c = diffuse + specular + reflection + refraction

        return c

    def scene_intersect(self, origin, direction):
        zbuffer = float('inf')
        material = None
        intersect = None

        for obj in self.scene:
            r_intersect = obj.ray_intersect(origin, direction)

            if r_intersect and r_intersect.distance < zbuffer:
                zbuffer = r_intersect.distance
                material = obj.material
                intersect = r_intersect

        return material, intersect

    def render(self):
        fov = pi/2
        aspect_ratio = self.width/self.height

        for y in range(self.height):
            for x in range(self.width):
                if random() > RAND_VAL:
                    i = (
                        (2 * ((x + 0.5)/self.width) - 1)
                        * aspect_ratio * tan(fov/2)
                    )
                    j = 1 - 2 * ((y + 0.5)/self.height) * tan(fov/2)

                    direction = norm(V3(i, j, -1))
                    col = self.cast_ray(V3(0, 0, 0), direction)
                    self.point(x, y, col)

    def load(self, filename, translate, scale):
        model = Obj(filename)
        triangles_vertex = []

        for face in model.faces:
            f1 = face[0][0] - 1
            f2 = face[1][0] - 1
            f3 = face[2][0] - 1

            A = transform(model.vertices[f1], translate, scale)
            B = transform(model.vertices[f2], translate, scale)
            C = transform(model.vertices[f3], translate, scale)
            triangles_vertex.append([A, B, C])

        return triangles_vertex
