#version 330 core

layout (location = 0) in vec3 in_position;

out vec3 txBox;

uniform mat4 m_proj;
uniform mat4 v_proj;
uniform mat4 model_mat;

void main(){
    vec4 x = m_proj * v_proj * model_mat * vec4(in_position,1.0);
    txBox = in_position;
    gl_Position = x.xyww;
    gl_Position.z -= 0.0001;
}