#version 330 core

layout (location = 0) in vec2 in_txcoord;
layout (location = 1) in vec3 in_norm;
layout (location = 2) in vec3 in_position;

out vec2 rtc_0;
out vec3 norm;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 v_proj;
uniform mat4 model_mat;

void main(){
    rtc_0 = in_txcoord;
    fragPos = vec3(model_mat * vec4(in_position,1.0));
    //inverse and transpose for correct lightning
    norm = mat3(transpose(inverse(model_mat))) * normalize(in_norm);
    gl_Position = m_proj * v_proj * model_mat * vec4(in_position.xy,in_position.z - 4.5 ,1.0);
}