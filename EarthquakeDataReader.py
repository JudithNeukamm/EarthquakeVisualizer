import vtk
import string
import time


class EarthquakeDataReader(object):

    # Filter Latitude (x)
    LatMax = 45.5  # from south(deg) 44.3
    LatMin = 44.3  # to north(deg) 45.5

    # Filter Longitude (y)
    LonMax = 12.0  # from west(deg) 10.0
    LonMin = 10.0  # to east(deg) 12

    # Filter depth (z)
    zMin = 0.0
    zMax = 1.0

    # Filter strength of earthquake
    StrengthMin = 0
    StrengthMax = 10

    def set_strength_filter(self, min_strength, max_strength):
        self.StrengthMin = min_strength
        self.StrengthMax = max_strength

    def get_strength_range(self):
        return self.StrengthMin, self.StrengthMax

    def get_bounds(self):
        return self.LatMin, self.LatMax, self.LonMin, self.LonMax, self.zMin, self.zMax
    
    # Read data points
    def read_points(self, inputfile):
        
        # all data
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

                # Filter location range
                # @see: http://www.zhang-liu.com/misl/map.html
                # Latitude (x): from south(deg) 44.3 - north(deg) 45.5
                # Longitude (y): from west(deg) 10.0 - east(deg) 12
                if x < self.LatMin or x > self.LatMax or y < self.LonMin or y > self.LonMax:
                    # read next line
                    line = infile.readline()
                    continue

                # Filter strength of earthquake
                if r < self.StrengthMin or r > self.StrengthMax:
                    # read next line
                    line = infile.readline()
                    continue

                # create one dataset for each month
                # date string example: '2014-09-23 18:31:02.300'
                year = date[:4]
                month = date[5:7]

                # create a containers for every month of a given year
                if not all_data.has_key(year):
                    all_data[year] = {}

                    for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
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

                if z > self.zMax:
                    self.zMax = z

                # Insert floats into the point array
                all_data.get(year)[month]['points'].InsertNextPoint(x, y, z)
                all_data.get(year)[month]['scalar'].InsertNextValue(r)
                all_data.get(year)[month]['tid'].InsertNextValue(t)
    
            # read next line
            line = infile.readline()

        return all_data
