#version 330 core

layout (location=0) in uint data;

int x,y,z;
int amb;
int dirid;

uniform mat4 m_proj;
uniform mat4 v_proj;
uniform mat4 model_mat;

flat out int vox_id;
flat out int face_id;
out float shader;
out vec3 fragPos;

const float shading[6] = float[6](
    1.0,0.5,
    0.5,0.8,
    0.5,0.8
);

out vec3 vox_color;

out vec2 tx;

const float amb_shading[4] = float[4](0.1,0.25,0.5,1.0); //for each face

const vec2 tx_coords[4] = vec2[4](
    vec2(0,0),vec2(0,1),
    vec2(1,0),vec2(1,1)
);

//basically every face of voxel down here
const int tx_ind[24] = int[24](
    1,0,2,1,2,3,
    3,0,2,3,1,0,
    3,1,0,3,0,2,
    1,2,3,1,0,2
);

void unpacking_data(uint data){
    //hard code bits numbers
    uint bbit = 6u,cbit = 6u,dbit = 8u,ebit = 3u,fbit = 2u,gbit = 1u;
    uint bmask = 63u,cmask = 63u,dmask = 255u,emask = 7u,fmask = 3u,gmask = 1u;

    uint fgbit = fbit + gbit;
    uint efgbit = ebit + fgbit;
    uint defgbit = dbit + efgbit;
    uint cdefgbit = cbit + defgbit;
    uint bcdefgbit = bbit + cdefgbit;

    x = int(data >> bcdefgbit);
    y = int((data >> cdefgbit) & bmask);
    z = int((data >> defgbit) & cmask);

    vox_id = int((data >> efgbit)&dmask);
    face_id = int((data >> fgbit)&emask);
    amb = int((data >> gbit)&fmask);
    dirid = int(data & gmask);
};

void main(){
    unpacking_data(data);
    vec3 in_position = vec3(x,y,z);
    fragPos = vec3(model_mat * vec4(in_position,1.0));
    int tx_index = gl_VertexID % 6 + ((face_id & 1)+dirid*2) * 6;
    tx = tx_coords[tx_ind[tx_index]];
    shader = shading[face_id]*amb_shading[amb];
    gl_Position = m_proj * v_proj * model_mat * vec4(in_position,1.0);
}