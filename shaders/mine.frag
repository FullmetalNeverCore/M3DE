#version 330 core 

layout (location=0) out vec4 fragColor;

in vec3 vox_color;
in vec3 fragPos;


uniform sampler2DArray tx_0;
uniform vec3 camP;
uniform int rendist; 


in vec2 tx;
in float shader;
flat in int vox_id;
flat in int face_id;

float fogDensity = 0.1;  // Adjust this parameter to control the density of the fog
float fogStartDistance = float(rendist-50);  // Adjust this parameter to control the distance at which the fog starts
float fogEndDistance = float(rendist+25);  // Adjust this parameter to control the distance at which the fog completely covers the object

vec3 applyFog(vec3 color, float distance) {
    float fogFactor = clamp((distance - fogStartDistance) / (fogEndDistance - fogStartDistance), 0.0, 1.0);
    vec3 fogColor = vec3(0.5, 0.5, 0.5);  // Gray color for fog
    return mix(color, fogColor, fogFactor);
}


void main(){
    vec2 tex = tx;
    tex.x = tx.x / 3.0 - min(face_id,2) / 3.0;
    vec3 color = texture(tx_0,vec3(tex,vox_id)).rgb*shader;
    float distance = length(camP - fragPos);
    color = applyFog(color,distance);
    fragColor = vec4(color,1.0);
}