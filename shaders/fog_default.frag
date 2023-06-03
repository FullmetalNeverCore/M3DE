#version 330 core

layout (location = 0) out vec4 fragCol;

in vec2 rtc_0;
in vec3 norm; 
in vec3 fragPos;

uniform sampler2D tx_s;

struct Bulb{
    vec3 diff;
    vec3 pos;
    vec3 amb;
    vec3 spe;
};

uniform Bulb bulb;
uniform vec3 camP; 

float fogDensity = 0.1;  // Adjust this parameter to control the density of the fog
float fogStartDistance = 10.0;  // Adjust this parameter to control the distance at which the fog starts
float fogEndDistance = 50.0;  // Adjust this parameter to control the distance at which the fog completely covers the object

vec3 applyFog(vec3 color, float distance) {
    float fogFactor = clamp((distance - fogStartDistance) / (fogEndDistance - fogStartDistance), 0.0, 1.0);
    vec3 fogColor = vec3(0.5, 0.5, 0.5);  // Gray color for fog
    return mix(color, fogColor, fogFactor);
}

vec3 turnLight(vec3 clr){
    vec3 normal = normalize(norm);
    // ambience
    vec3 amb = bulb.amb;
    //Beer–Lambert law for diffusion, the further the light source, the more diffused light on the object
    vec3 lightDir = normalize(bulb.pos - fragPos);
    float diff = max(0,dot(lightDir,normal));
    vec3 diffuse = diff * bulb.diff;
    //specular 
    vec3 direction = normalize(camP - fragPos);
    vec3 reflectDir = reflect(-lightDir,normal);
    float spec = pow(max(dot(direction,reflectDir),0),32);
    vec3 spec_int = spec * bulb.spe; //intensity
    return clr * (amb + diffuse + spec_int);
}

void main(){
    vec3 color = texture(tx_s, rtc_0).rgb;
    color = turnLight(color);
    
    float distance = length(camP - fragPos);
    color = applyFog(color, distance);
    
    fragCol = vec4(color, 1.0);
}
