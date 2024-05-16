def getList(l1, index):
    newList = []
    for i in l1:
        newList.append(i[index])
    return newList
def getminX(x, l1):
    m = 0
    for i in l1:
        if i <= x:
            m = max(i, m)
    h = 99999
    for i in l1:
        if i > x:
            h = min(i, h)
    return m, h
def getCloseX(x, l1):
    h = l1[min(range(len(l1)), key = lambda i: l1[i]-x)]
    u = l1[min(range(len(l1)), key = lambda i: -(l1[i]-x))]
    return h, u
class G:
    def __init__(self, colors):
        self.colors = colors
        self.rValues = getList(colors, 0)
        self.gValues = getList(colors, 1)
        self.bValues = getList(colors, 2)



    def getX(self, x, l1):
        low, high = l1[0], l1[1]
        y = low + (high-low)*(x)
        return y

    def getRGBfromX(self, x):
        r = self.getX(x, self.rValues)
        g = self.getX(x, self.gValues)
        b = self.getX(x, self.bValues)
        return int(r), int(g), int(b)
class Gradient:
    def __init__(self, colors):
        self.gradients = []
        try:
            self.rValues = getList(colors, 0)
            self.gValues = getList(colors, 1)
            self.bValues = getList(colors, 2)
        except:
            raise IndexError("Invalid color code in \"colors\"")
        try:
            self.xValues = getList(colors, 3)
        except:
            raise IndexError("No position value found in \"colors\"")
        for r in self.rValues:
            if r > 255 or r < 0:
                raise ValueError("Invalide color code in \"colors\" (color code cannot have a value over 255 or under 0)")
        for g in self.gValues:
            if g > 255 or g < 0:
                raise ValueError("Invalide color code in \"colors\" (color code cannot have a value over 255 or under 0)")
        for b in self.bValues:
            if b > 255 or b < 0:
                raise ValueError("Invalide color code in \"colors\" (color code cannot have a value over 255 or under 0)")
        for x in self.xValues:
            if x > 1 or x < 0:
                raise ValueError("Invalide position in \"colors\" (position value cannot exceed 1 or fall below 0)")
        for i in range(len(colors)-1):
            g = G([colors[i], colors[i+1]])
            self.gradients.append(g)

    def getRGBfromX(self,x):
        lowx, high = getminX(x, self.xValues)
        low = self.xValues.index(lowx)
        if high == 0:
            return self.gradients[low].getRGBfromX(high)
        elif high-lowx == 0:
            return self.gradients[low].getRGBfromX(high)
        else:
            return self.gradients[low].getRGBfromX((x-lowx)/(high-lowx))

