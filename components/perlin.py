import noise
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.colors import LinearSegmentedColormap


class Perlin:
    def __init__(self)->None:
        pass 
    def generate_height_map(self,width, height, scale, octaves, persistence, lacunarity):
        seed = random.randint(0, 1000)  # Generate a random seed
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
        
    def custom_color_map(self,height_map):
        colors = [
            (58/255,66/255,9/255),
            (72/255, 82/255, 11/255),
            (103/255, 100/255, 105/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (172/255, 180/255, 196/255),
            (103/255, 100/255, 105/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (154/255, 156/255, 154/255),
            (103/255, 100/255, 105/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (172/255, 180/255, 196/255),
            (103/255, 100/255, 105/255),
            (154/255, 156/255, 154/255),
            (172/255, 180/255, 196/255),
            (230/255, 235/255, 237/255)
        ]


        n_bins = [100] * len(colors)  # Number of bins for each color
        cmap_name = 'scenery'
        cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
        return cm(height_map)
    def generate_and_visualize_maps(self,width, height, scale, octaves, persistence, lacunarity,save_path):
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
