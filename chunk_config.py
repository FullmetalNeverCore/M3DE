chunk_size = 32
half_chunk = chunk_size // 2
chunk_area = chunk_size * chunk_size
chunk_vol = chunk_area * chunk_size


world_wid,world_hei = 2,1
world_dim = world_wid 
world_area = world_wid * world_dim
center_xz = world_wid * 16
center_y = world_hei * 16
world_v = world_area * world_hei

seed = 16