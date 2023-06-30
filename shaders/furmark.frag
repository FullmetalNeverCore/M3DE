#version 330 core


layout (location = 0) out vec4 fragCol;

in vec2 rtc_0;
in vec3 norm; 
in vec3 fragPos;

vec2 u_res = vec2(1600,900);

uniform sampler2D tx_s;




float map(vec3 p){
    float dist = length(p) - 0.6;
    return dist;

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
        float hit = map(p);

        dist += hit;

        if(dist > 100.0 || abs(hit) < 0.0001) break;
    }
    return dist;
}

vec3 render(){
    vec2 uv = (2.0 * (gl_FragCoord.xy) - u_res.xy)/u_res.y;
    vec3 col = vec3(0);

    //uv = step(0,uv);
    //col = vec3(uv,0);

    vec3 ro = vec3(0,0,-1.0);
    vec3 rd = normalize(vec3(uv,1.0));
    float dist = rayMarch(ro,rd);
    if(dist < 100.0){
        vec3 p = ro + dist * rd; 
        col += triPlanar(tx_s,p*2.0,getNormal(p));
    }

    return col;
}



void main(){
    vec3 color = texture(tx_s,rtc_0).rgb;
    color = render();
    fragCol = vec4(color,1.0);
}

