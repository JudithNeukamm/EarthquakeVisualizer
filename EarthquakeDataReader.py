import vtk
import string
import math
import time


class EarthquakeDataReader(object):
    
    def __init__(self):
        self.number = 0

        # Latitude (x): from south(deg) 44.3 - north(deg) 45.5
        self.LatMax = 45.5
        self.LatMin = 44.3

        # Longitude (y): from west(deg) 10.0 - east(deg) 12
        self.LonMax = 12.0
        self.LonMin = 10.0

        self.zMin = 0.0
        self.zMax = 1.0

        # Compute the range of the data
        self.x1 = self.distance(self.LatMin, self.LonMin, self.LatMax, self.LonMin)
        self.x2 = self.distance(self.LatMin, self.LonMax, self.LatMax, self.LonMax)
        self.y1 = self.distance(self.LatMin, self.LonMin, self.LatMin, self.LonMax)
        self.y2 = self.distance(self.LatMax, self.LonMin, self.LatMax, self.LonMax)
        
    # Computes distance in Kilometers
    def distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        dLat = math.radians(lat2-lat1)
        dLon = math.radians(lon2-lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)
    
        a = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.sin(dLon/2.0) * math.sin(dLon/2.0) * math.cos(lat1) * math.cos(lat2) 
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
        d = R * c
        return d

    def get_bounds(self):
        return self.LatMin, self.LatMax, self.LonMin, self.LonMax, self.zMin, self.zMax
        #return self.x1, self.x2, self.y1, self.y2, 0, 1
    
    #Read Points
    def readPoints(self, inputfile):
        
        # all datas
        all_data = {}

        # Open the file
        infile = open(inputfile)
        
        # Read one line
        line = infile.readline()
    
        # Loop through lines
        while line:
            
            # Split the line into data
            data = line.split(';')
            # Skip the commented lines
            if data and data[0][0] != '#':
                # Convert data into float
                # print data[0], data[1], data[2], data[3], data[4].split('--')[0]
                date, x, y, z, r = data[0].rstrip(';'), float(data[1].rstrip(';')), float(data[2].rstrip(';')),  float(data[3].rstrip(';')), float(data[4].split('--')[0])
                z /= 100

                # Range selection
                # @see: http://www.zhang-liu.com/misl/map.html
                # Latitude (x): from south(deg) 44.3 - north(deg) 45.5
                # Longitude (y): from west(deg) 10.0 - east(deg) 12
                if x < self.LatMin or x > self.LatMax or y < self.LonMin or y > self.LonMax:
                    # read next line
                    line = infile.readline()
                    continue

                # create one dataset for each month
                # date string example: '2014-09-23 18:31:02.300'
                year = date[:4]
                month = date[5:7]
                   
                if not all_data.has_key(year):
                    all_data[year] = {}

                if not all_data.get(year).has_key(month):
                    all_data.get(year)[month] = {
                        'points': vtk.vtkPoints(),
                        'scalar': vtk.vtkFloatArray(),
                        'tid': vtk.vtkFloatArray()
                    }

                row = string.split(date)
                adate = row[0].split('-')
                atime = row[1].split(':')
                temp = atime[2].split('.')
                atime[2] = temp[0]

                if atime[2] == '':
                    atime[2] = '00'
                t = time.mktime([int(adate[0]), int(adate[1]), int(adate[2]), int(atime[0]), int(atime[1]), int(atime[2]), 0, 0, 0])

                # if x > LatMax:
                #     LatMax = x
                # if x < LatMin:
                #     LatMin = x
                # if y > LonMax:
                #     LonMax = y
                # if y < LonMin:
                #     LonMin = y
                if z > self.zMax:
                    self.zMax = z

                # Insert floats into the point array
                all_data.get(year)[month]['points'].InsertNextPoint(x, y, z)
                all_data.get(year)[month]['scalar'].InsertNextValue(r)
                all_data.get(year)[month]['tid'].InsertNextValue(t)
    
            # read next line
            line = infile.readline()
        #
        # for everyYear in all_data:
        #     for everyMonth in all_data[everyYear]:
        #
        #         points = all_data[everyYear][everyMonth]['points']
        #         xx = self.x1
        #         l = points.GetNumberOfPoints()
        #         i = 0
        #
        #         while i < l:
        #             x, y, z = points.GetPoint(i)
        #
        #             u = (x-self.LatMin)/(self.LatMax-self.LatMin)
        #             x = (x-self.LatMin)/(self.LatMax-self.LatMin)*xx
        #
        #             # Not perfect conversion...
        #             yy = (1-u)*self.y1 + u*self.y2
        #             y = (y-self.LonMin)/(self.LonMax-self.LonMin)*yy
        #             points.SetPoint(i, x, y, z)
        #             i += 1

        return all_data
