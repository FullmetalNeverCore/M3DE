class Benchmark:
    _instance = None 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self)->None:
        self.lowest = 33 
        self.fps_count = []


    def avarage_fps(self) -> float:
        return sum(self.fps_count)/len(self.fps_count)

    def count_points(self) -> int:
        return int(self.lowest*self.avarage_fps())