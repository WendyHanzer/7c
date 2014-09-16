#version 330
//uniform bool hasTexture;
//varying vec2 tex_coords;
uniform sampler1D tex;
in float colorPos;

void main(void) {
    vec4 color = texture1D(tex, colorPos);

    gl_FragColor = color;
}
