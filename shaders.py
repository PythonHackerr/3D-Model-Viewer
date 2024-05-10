# Vertex Shader
vertex_shader = """
#version 330
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;
out vec2 TexCoord;
void main() {
    gl_Position = vec4(position, 1.0);
    TexCoord = texCoord;
}
"""

# Fragment Shader
fragment_shader = """
#version 330
in vec2 TexCoord;
out vec4 FragColor;
uniform sampler2D diffuseTexture;
uniform sampler2D specularTexture;

uniform vec3 light_direction;
uniform vec3 light_color;
uniform vec3 ambient_strength;

void main() {
    vec4 color_diffuse = texture(diffuseTexture, TexCoord);
    vec4 color_specular = texture(specularTexture, TexCoord);

    vec3 ambient = ambient_strength[0] * light_color;

    vec3 norm = normalize(vec3(0, 0, 1));

    vec3 diffuse = max(dot(norm, light_direction), 0.0) * light_color;

    vec3 result = (ambient + diffuse) * color_diffuse.rgb;

    vec4 final_color = vec4(result, color_diffuse.a) * color_specular;

    FragColor = final_color;
}
"""
