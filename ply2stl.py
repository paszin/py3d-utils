import os
from stlwriter import STLWriter
import tempfile

class Ply2Stl:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.lines = []
        self.f = tempfile.NamedTemporaryFile()
        self.stlwriter = STLWriter(filename=self.f.name)
        self.stlwriter.start()

    @staticmethod
    def parseVertexLine(line):
        '''e.g. '-0.0604006 0.0282632 0.421265 112 124 138'''
        return map(float, line.split(' ')[:3])

    @staticmethod
    def parseFaceLine(line):
        '''e.g.3 1 7 2'''
        return map(int, line.split(' ')[1:4])
        
        

    def load(self, filename):
        self.verticesCount = 0
        self.facesCount = 0
        self.end_header_line = None
        with open(filename) as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                self.lines.append(line)
                if line == "end_header":
                    self.end_header_line = i
                    continue
                if line.startswith("element vertex"):
                    self.verticesCount = int(line.replace("element vertex", "").strip())
                    continue
                if line.startswith("element face"):
                    self.facesCount = int(line.replace("element face", "").strip())
                    continue
                #print i,
                if self.end_header_line and i <= self.verticesCount + self.end_header_line:
                    self.vertices.append(Ply2Stl.parseVertexLine(line))
                if self.end_header_line and i > self.verticesCount + self.end_header_line:
                    self.faces.append(Ply2Stl.parseFaceLine(line))
                    

    def addToStl(self, filename):
        self.vertices = []
        self.faces = []
        self.load(filename)
        self.writeStl(False)

    def finishStl(self, filename=None):
        code = self.stlwriter.finish()
        with open(filename, 'w') as f:
            f.write(code)
            return
        return self.f.name

    def writeStl(self, end=True):

        for face in self.faces:
            self.stlwriter.addFacet(self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]])
        if end:
            self.stlwriter.finish()
                


