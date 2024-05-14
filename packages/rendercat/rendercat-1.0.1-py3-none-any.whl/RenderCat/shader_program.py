class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        # noinspection PyDictCreation
        self.shaders = {}
        self.shaders['default'] = self.ctx.program(vertex_shader='''
        #version 330 core
        
        layout (location = 0) in vec2 in_texcoord_0;
        layout (location = 1) in vec3 in_normal;
        layout (location = 2) in vec3 in_position;
        
        out vec2 uv_0;
        out vec3 normal;
        out vec3 fragPos;
        out vec4 shadowCoord;

        uniform mat4 m_proj;
        uniform mat4 m_view;
        uniform mat4 m_view_light;
        uniform mat4 m_model;
        
        mat4 m_shadow_bias = mat4(
            0.5, 0.0, 0.0, 0.0,
            0.0, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.5, 0.0,
            0.5, 0.5, 0.5, 1.0
        );
        
        void main(){
            uv_0 = in_texcoord_0;
            fragPos = vec3(m_model * vec4(in_position, 1.0));
            normal = mat3(transpose(inverse(m_model)))*normalize(in_normal);
            gl_Position = m_proj*m_view*m_model*vec4(in_position, 1.0);
        
            mat4 shadowMVP = m_proj * m_view_light * m_model;
            shadowCoord = m_shadow_bias * shadowMVP * vec4(in_position, 1.0);
            shadowCoord.z -= 0.0005;
        }
        ''', fragment_shader='''
        #version 330 core
        
        layout (location=0) out vec4 FragColor;
        
        in vec2 uv_0;
        in vec3 normal;
        in vec3 fragPos;
        in vec4 shadowCoord;
        uniform vec2 u_resolution;
        
        struct Light {
            vec3 position;
            vec3 Ia;
            vec3 Id;
            vec3 Is;
        };
        
        uniform Light light;
        uniform sampler2D u_texture_0;
        uniform vec3 camPos;
        uniform sampler2DShadow shadowMap;
        
        float lookup(float ox, float oy) {
            vec2 pixelOffset = 1 / u_resolution;
            return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                             oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
        }
        
        float getSoftShadowX4() {
            float shadow;
            float swidth = 1.5;  // shadow spread
            vec2 offset = mod(floor(gl_FragCoord.xy), 2.0) * swidth;
            shadow += lookup(-1.5 * swidth + offset.x, 1.5 * swidth - offset.y);
            shadow += lookup(-1.5 * swidth + offset.x, -0.5 * swidth - offset.y);
            shadow += lookup( 0.5 * swidth + offset.x, 1.5 * swidth - offset.y);
            shadow += lookup( 0.5 * swidth + offset.x, -0.5 * swidth - offset.y);
            return shadow / 4.0;
        }
        
        float getSoftShadowX16() {
            float shadow;
            float swidth = 1.0;
            float endp = swidth * 1.5;
            for (float y = -endp; y <= endp; y += swidth) {
                for (float x = -endp; x <= endp; x += swidth) {
                    shadow += lookup(x, y);
                }
            }
            return shadow / 16.0;
        }
        
        float getSoftShadowX64() {
            float shadow;
            float swidth = 0.6;
            float endp = swidth * 3.0 + swidth / 2.0;
            for (float y = -endp; y <= endp; y += swidth) {
                for (float x = -endp; x <= endp; x += swidth) {
                    shadow += lookup(x, y);
                }
            }
            return shadow / 64;
        }
        
        float getShadow() {
            float shadow = textureProj(shadowMap, shadowCoord);
            return shadow;
        }
        
        vec3 getLight(vec3 Color){
            vec3 Normal = normalize(normal);
        
            vec3 ambient = light.Ia;
        
            vec3 lightDir = normalize(light.position-fragPos);
            float diff = max(0, dot(lightDir, normal));
            vec3 diffuse = diff * light.Id;
        
            vec3 viewDir = normalize(camPos - fragPos);
            vec3 reflectDir = reflect(-lightDir, Normal);
            float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
            vec3 specular = spec * light.Is;
        
            float shadow = getSoftShadowX16();
        
            return Color * (ambient+(diffuse+specular) * shadow);
        }
        
        void main(){
            float gamma = 2.2;
            vec3 col = texture(u_texture_0, uv_0).rgb;
        
            col = getLight(col);
        
            col = pow(col, 1/vec3(gamma));
            FragColor = vec4(col, 1.0);
        }
        ''')
        self.shaders['shadow_map'] = self.ctx.program(vertex_shader='''
        #version 330 core
        
        layout (location = 2) in vec3 in_position;
        
        uniform mat4 m_proj;
        uniform mat4 m_view_light;
        uniform mat4 m_model;
        
        void main() {
            mat4 mvp = m_proj * m_view_light * m_model;
            gl_Position = mvp * vec4(in_position, 1.0);
        }
        ''', fragment_shader='''
        #version 330 core
        void main() {}
        ''')
        self.shaders['skybox'] = self.ctx.program(vertex_shader='''
        #version 330 core
        layout (location = 0) in vec3 in_position;
        
        out vec4 clipCoords;
        
        
        void main() {
            gl_Position = vec4(in_position, 1.0);
            clipCoords = gl_Position;
        }
        ''', fragment_shader='''
        #version 330 core
        out vec4 fragColor;
        
        in vec4 clipCoords;
        
        uniform samplerCube u_texture_skybox;
        uniform mat4 m_invProjView;
        
        
        void main() {
            vec4 worldCoords = m_invProjView * clipCoords;
            vec3 texCubeCoord = normalize(worldCoords.xyz / worldCoords.w);
            fragColor = texture(u_texture_skybox, texCubeCoord);
        }
        ''')
        self.shaders['overlay'] = self.ctx.program(
            vertex_shader='''
        #version 330 core
        
        layout (location = 0) in vec4 in_position;
        
        void main() {
            gl_Position = vec4(in_position.xy, -1.0, 1.0);
        }
        ''', fragment_shader='''
        #version 330 core
        
        out vec4 frag_color;
        
        uniform vec2 u_resolution;
        uniform sampler2D u_texture_0;
        
        
        void main() {
            vec2 uv = vec2(gl_FragCoord.xy / u_resolution);
            vec4 tex_col = texture(u_texture_0, uv);
            if (tex_col.xyz == vec3(0.392156862745098, 0.7843137254901961, 0.0588235294117647)) discard;
            frag_color = vec4(tex_col.xyz, 1.0);
        }
        '''
        )

    def get_prtogram(self, shader_name):
        with open(f'Shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'Shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.shaders.values()]
