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

vec3 turnLight(vec3 clr){
    vec3 normal = normalize(norm);
    // ambience
    vec3 amb = bulb.amb;
    //Beer–Lambert law for diffusion,further the light source more diffused light on object
    vec3 lightDir = normalize(bulb.pos - fragPos);
    float diff = max(0,dot(lightDir,normal));
    vec3 diffuse = diff * bulb.diff;
    //specular 
    vec3 direction = normalize(camP - fragPos);
    vec3 reflectDir = reflect(-lightDir,normal);
    float spec = pow(max(dot(direction,reflectDir),0),32);
    vec3 spec_int = spec * bulb.spe; //intensity
    return clr * (amb + diff + spec_int);
}

void main(){
    vec3 color = texture(tx_s,rtc_0).rgb;
    color = turnLight(color);
    fragCol = vec4(color,1.0);
}