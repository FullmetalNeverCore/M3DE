#version 330 core


layout (location = 0) out vec4 fragCol;

in vec2 rtc_0;
in vec3 norm; 
in vec3 fragPos;

vec2 u_res = vec2(1600,900);

uniform sampler2D tx_s;
uniform sampler2D noise;
uniform sampler2D backg;

//Confrolar tiling values 

const float PI = 3.14;
const float TAU = 2*PI;

uniform float time;


float fur(vec3 p,sampler2D tex){
    float s = 4.5;
    float u = s/TAU*atan(p.y/p.x);
    float v = sign(p.z) / TAU * acos((p.z*p.z*sqrt(s*s+1)+sqrt(1-p.z*p.z*s*s))/(p.z*p.z+1));
    vec2 uv = 2.0 *vec2(u,v);
    float fur = texture(tex,uv).r;
    return fur*0.06;
}

mat2 rotate2D(float x){
    float s = sin(x);
    float c = cos(x);
    return mat2(c,s,-s,c);
}

void just_rotate(inout vec3 z){
    z.xy *= rotate2D(sin(time*0.8)*0.25);
    z.yz *= rotate2D(sin(time*0.7)*0.2);
}


float map(vec3 p){
    float dist = length(vec2(length(p.xy)-0.6,p.z))-0.22;
    return dist * 0.7;

}


vec3 triPlanar(sampler2D tx,vec3 p,vec3 norm){
    norm = abs(norm);
    norm = pow(norm,vec3(15));
    norm /= norm.x + norm.y + norm.z;
    p = p * 0.5 + 0.5;
    return (texture(tx,p.xy)*norm.z+
            texture(tx,p.xz)*norm.y+
            texture(tx,p.yz)*norm.x).rgb;
}


vec3 getNormal(vec3 p){
    vec2 e = vec2(0.01,0.0);
    return normalize(vec3(map(p) - vec3(map(p - e.xyy),map(p-e.yxy),map(p-e.yxx))));
}

float rayMarch(vec3 ro, vec3 rd){
    float dist = 0.0;
    for (int i = 0;i<256;i++){
        vec3 p = ro + dist * rd;
        just_rotate(p);
        float hit = map(p);

        dist += hit;
        dist -= fur(0.5*p,noise);
        if(dist > 100.0 || abs(hit) < 0.0001) break;
    }
    return dist;
}

vec3 render(vec2 off){
    vec2 uv = (3.0 * (gl_FragCoord.xy+off) - u_res.xy)/u_res.y;
    vec3 col = vec3(0);

    //uv = step(0,uv);
    //col = vec3(uv,0);
    vec3 ro = vec3(0,0,-1.0);
    vec3 rd = normalize(vec3(uv,1.0));
    float dist = rayMarch(ro,rd);
    if(dist < 100.0){
        vec3 p = ro + dist * rd; 
        just_rotate(p);
        col += triPlanar(tx_s,p*1.0,getNormal(p));
    }
    else{
        float hpi = atan(uv.y,uv.x);
        float hro = length(uv)+0.2;
        vec2 back;
        back.x = 3.0 * hpi / PI;
        back.y = time * 0.5 + PI / hro;
        col += texture(backg,back).rgb;
    }
    return col;
}

//anti alising x4
vec3 AA(){
    vec4 i = vec4(0.125,-0.375,0.375,-0.375);
    vec3 aa = render(i.xz) + render(i.yw) + render(i.wx) + render(i.zy);
    return aa /= 4.0;

}

void main(){
    vec3 color = texture(tx_s,rtc_0).rgb;
    color = AA();
    fragCol = vec4(color,1.0);
}

