#version 330 core

out vec4 fragCol;

in vec3 txBox;

uniform  samplerCube tx_skybox; 


void main(){
    fragCol = texture(tx_skybox,txBox);
}