import noise
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import LinearSegmentedColormap


class Perlin:
    def __init__(self)->None:
        pass 
    
    #generate heignt map
    def generate_height_map(self,width : int, height : int , scale : int, octaves : float , persistence : float, lacunarity : int)->'Height Map':
        seed = random.randint(0, 99999)  # Generate a random seed
        height_map = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                height_map[i][j] = noise.pnoise2(i/scale, 
                                                j/scale, 
                                                octaves=octaves, 
                                                persistence=persistence, 
                                                lacunarity=lacunarity, 
                                                repeatx=1024, 
                                                repeaty=1024, 
                                                base=seed)
        return height_map
        
    #color map based on height map
    def custom_color_map(self,height_map : list)->'LinearSegmentedColormap':
        colors = [
            (36/255,41/255, 4/255),
            (58/255, 66/255, 9/255),
            (54/255, 56/255, 55/255),
            (117/255, 120/255, 118/255),
            (90/255, 92/255, 91/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (255/255, 255/255, 255/255)  # White for snow
        ]

        cmap_name = 'scenery'
        cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
        return cm(height_map)

    def generate_and_visualize_maps(self,width : int, height : int , scale : int, octaves : float , persistence : float, lacunarity : int,save_path : str):
        height_map = self.generate_height_map(width, height, scale, octaves, persistence, lacunarity)

        randint = random.randint(0,99999999)
        plt.imshow(height_map, cmap='gray', origin='lower')  # Use 'gray' colormap for grayscale
        plt.axis('off')  # Turn off axes
        plt.savefig(save_path + f"height_map_{randint}.png", bbox_inches='tight', pad_inches=0, dpi=300, transparent=False)

        color_map = self.custom_color_map(height_map)
        
        plt.imshow(color_map, origin='lower')
        plt.axis('off')
        plt.savefig(save_path + f"color_map_{randint}.png", bbox_inches='tight', pad_inches=0, dpi=300, transparent=False)  # Save color map
        plt.close()

        return randint



if __name__ == "__main__":
    Perlin().generate_and_visualize_maps(1024, 512, 100, 6, 0.5, 2,save_path="../tx/maps/")
