#version 330 core

out vec4 fragCol;

in vec3 txBox;

uniform  samplerCube tx_skybox; 


void main(){
    fragCol = texture(tx_skybox,txBox);
    // Calculate fog factor based on fragment's distance from the camera
    float fog_factor = exp(-0.02 * gl_FragCoord.z);

    fog_factor = clamp(fog_factor,0.0,1.0);

    // Blend the fragment color with the fog color based on the fog factor
    vec4 final_color = mix(fragCol, vec4(vec3(0.5), 0.5), fog_factor);

    fragCol = final_color;
}