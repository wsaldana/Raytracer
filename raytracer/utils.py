import struct


class Intersect:
    def __init__(self, distance, point, normal, text_coords=None):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.text_coords = text_coords


class Light:
    def __init__(self, position, intensity, color):
        self.position = position
        self.intensity = intensity
        self.color = color


class V3:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, other):
        try:
            return V3(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z,
            )
        except AttributeError:
            return V3(
                self.x * other,
                self.y * other,
                self.z * other,
            )

    def __len__(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def length(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class V2:
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def __add__(self, other):
        return V2(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        return V2(
            self.x - other.x,
            self.y - other.y
        )

    def __len__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y

    def __str__(self):
        return f'({self.x}, {self.y})'


def ccolor(v):
    return max(0, min(255, int(v)))


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)

        return f'Color({r}, {g}, {b})'

    def toBytes(self):
        b = ccolor(self.b)
        g = ccolor(self.g)
        r = ccolor(self.r)

        return bytes([b, g, r])

    def __add__(self, other):
        r = ccolor(self.r + other.r)
        g = ccolor(self.g + other.g)
        b = ccolor(self.b + other.b)

        return Color(r, g, b)

    def __mul__(self, k):
        r = ccolor(self.r * k)
        g = ccolor(self.g * k)
        b = ccolor(self.b * k)

        return Color(r, g, b)


def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    return round(xs[0]), round(xs[-1]), round(ys[0]), round(ys[-1])


def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(dw):
    return struct.pack('=l', dw)


def cross(v0, v1):
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)


def barycentric(A, B, C, P):
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary.z) < 1:
        return -1, -1, -1

    return (
        1 - (bary.x + bary.y) / bary.z,
        bary.y / bary.z,
        bary.x / bary.z
    )


def norm(v0: V3) -> V3:
    vector_l = v0.length()

    if vector_l == 0:
        return V3(0, 0, 0)

    return V3(
        v0.x / vector_l,
        v0.y / vector_l,
        v0.z / vector_l
    )


def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z


def matrix_multiply(M1, M2):
    result = [
        [
            sum(a * b for a, b in zip(X_row, Y_col))
            for Y_col in zip(*M2)
        ]
        for X_row in M1
    ]
    return result


def reflect(I, N):
    return norm(
        I - (N * (2 * dot(I, N)))
    )


def refract(I, N, refraction_index):
    cosi = -max(-1, min(1, dot(I, N)))
    etai = 1
    etat = refraction_index

    if cosi < 0:
        cosi = -cosi
        etai, etat = etat, etai
        N = N * -1

    try:
        eta = etai/etat
    except ZeroDivisionError:
        etai, etat = etat, etai
        eta = etai/etat

    k = 1 - eta**2 * (1 - cosi**2)
    if k < 0:
        return None

    return norm(
        (I * eta) + (N * ((eta * cosi) + k**0.5))
    )


def transform(vertex, translate=(0, 0, 0), scale=(1, 1, 1)):
    return V3(
        (vertex[0] * scale[0]) + translate[0],
        (vertex[1] * scale[1]) + translate[1],
        (vertex[2] * scale[2]) + translate[2]
    )
