"""Register painted references to complete rest-space surfaces.

Coordinates are fixed at authoring time and follow the skin, not the camera.
All textures remain opaque materials: missing source pixels use pigment fallback.
Original front/back and side atlases are never edited or used as alpha cutouts.
"""
import math

PALETTE={'Head and neck':'c08b5d','Eyes':'c08b5d','Mouth':'9f6347',
         'Hair':'50321f','Jacket':'47584d','Shirt':'bb8c42','Pants':'62533f',
         'Boots':'704825','Bag':'855023','Upper arms':'c08b5d',
         'Lower arms':'c08b5d','Hands':'c08b5d'}


def uv(pixel, size):
    return [round(pixel[0]/size[0], 6), round(1-pixel[1]/size[1], 6)]


def clamp(v, a, b):
    return max(a, min(b, v))


def paint_coordinates(item):
    group, name = item['group'], item['name']
    kind = 'solid'
    if group in ('Head and neck', 'Eyes', 'Mouth', 'Hair'):
        kind = 'portrait'
    elif group in ('Jacket', 'Shirt'):
        kind = 'garment'
    elif group == 'Pants':
        kind = 'pants'
    elif group == 'Boots' and not any(s in name.lower() for s in ('sole', 'lace', 'eyelet')):
        kind = 'boots'
    elif group == 'Bag' and name in ('Bag shell', 'Bag flap'):
        kind = 'bag'
    elif group in ('Upper arms', 'Lower arms', 'Hands'):
        kind = 'skin'
    elif group == 'Belt':
        kind = 'belt'
    result = {'paintKind': kind, 'paintFront': [], 'paintBack': [], 'paintSide': [], 'paintBlend': []}
    for offset in range(0, len(item['positions']), 3):
        x,y,z = item['positions'][offset:offset+3]
        nx,ny,nz = item['normals'][offset:offset+3]
        # Blend fixed projections according to the rest-surface normal. A vertex
        # never changes source image because a foot swings or camera orbits.
        f,b,s = max(0,-ny)**4, max(0,ny)**4, abs(nx)**4
        if f+b+s < .015:
            f=b=s=1/3
        total=f+b+s
        blend=[f/total,b/total,s/total]
        front=back=side=(0,0);size=(1774,887)
        if kind == 'portrait':
            z+=.055  # Paired with the complete portrait's collar-height fit.
            front=(260+x*300, 67+(1.791-z)*265)
            back=(252-x*330, 497+(1.791-z)*265)
            side=(270-y*250, 62+(1.791-z)*265)
            # Keep the facial drawing coherent across cheeks/nose. Surface
            # normals change quickly on a nose and used to blend a second eye
            # or jaw into the middle of the portrait. Side registration begins
            # at the temples, behind the main facial plane instead.
            ff=clamp((-.085-y)/.045,0,1)
            bb=clamp((y+.015)/.055,0,1)
            blend=[ff,bb,max(0,1-ff-bb)]
            if group=='Eyes':blend=[1,0,0]
            if name == 'Neck':
                front=(266+x*40,111);back=(251-x*40,533);side=(285,106)
            if name.startswith('Ear'):
                sign=1 if x>0 else -1
                front=((290 if sign>0 else 225)+(x-sign*.15)*230,78+(1.755-z)*260)
                back=((214 if sign>0 else 289)-(x-sign*.15)*230,505+(1.755-z)*240)
                side=(278-(y+.047)*230,73+(1.755-z)*250)
            if group == 'Hair':
                # Hair is textured from the hair region, never face/eyes.
                front=(clamp(front[0],218,299),clamp(front[1],20,43))
                back=(clamp(back[0],215,294),clamp(back[1],458,510))
                side=(clamp(side[0],254,323),clamp(side[1],24,43))
        elif kind == 'garment':
            size=(2172,724)
            front=(405+x*1320, 110+(1.55-z)*850)
            back=(1750-x*1320, 110+(1.55-z)*850)
            side=(1100-y*1080, 110+(1.55-z)*850)
            # Rolled cuffs have their own material coordinates in the source.
            if 'RolledCuff' in name:
                front=(230+(x%0.09)*500,455+(1.20-z)*200)
                back=(1510+(x%0.09)*500,450+(1.20-z)*200)
                side=(1040+(y%0.08)*500,460+(1.20-z)*200)
        elif kind == 'pants':
            # The satchel/hand hides one panel in the source drawings. Both
            # modeled legs reuse the unobscured cloth panel continuously from
            # waist to cuff, without crossing a painted hand/bag or switching
            # projection strips halfway down a thigh.
            front=(clamp(258+abs(x)*320,271,295),239+(.90-z)/.71*146)
            back=(clamp(252-abs(x)*320,214,238),650+(.90-z)/.71*160)
            t=clamp((.90-z)/.69,0,1)
            side=(270+56*t-y*200,240+140*t)
            # The side source is a striding pose with overlapping limbs. Keep
            # each complete trouser panel registered to the front/back cloth,
            # rather than painting a second limb's silhouette onto its side.
            blend=[max(0,-ny)+.12,max(0,ny)+.12,0]
        elif kind == 'boots':
            leg=1 if 'Left' in name else -1
            front=((300 if leg>0 else 213)+(x-leg*.10)*430,436-(z-.018)/.26*38)
            back=((200 if leg>0 else 305)-(x-leg*.10)*430,855-(z-.018)/.26*38)
            side=(707-y*300,435-(z-.018)/.26*41)
        elif kind == 'bag':
            # Use the unoccluded second side drawing, not a torso with baked bag.
            front=(638+(x+.244)/.163*59,267-(z-.769)/.194*60)
            back=front;side=front;blend=[0,0,1]
        elif kind == 'skin':
            sign=1 if x>=0 else -1
            sx=(320 if sign>0 else 191)
            front=(sx+(x-sign*.265)*180,140+(1.48-z)*225)
            back=(511-sx-(x-sign*.265)*180,575+(1.48-z)*225)
            side=(196+(y+.075)*100,205+(1.18-z)*180)
            if group=='Hands':
                front=(sx+(x-sign*.275)*170,267+(.94-z)*180)
                back=(511-sx-(x-sign*.275)*170,704+(.94-z)*180)
                side=(193+(y+.095)*120,247+(.94-z)*130)
        elif kind == 'belt':
            front=(260+x*180,222+(.94-z)*100)
            back=(252-x*180,651+(.94-z)*100)
            side=(282-y*100,223+(.94-z)*100)
        for key,point in [('paintFront',front),('paintBack',back),('paintSide',side)]:
            result[key].extend(uv(point,size))
        total=sum(blend)
        result['paintBlend'].extend(round(v/total,6) for v in blend)
    return result


def assign_blender_paint(objects, root):
    """Store actual UV layers and packed surface paintings in the authoring file.

    The browser uses the same registered coordinates. The .blend does not depend
    on that custom browser shader to retain its paintings.
    """
    import bpy
    sources={key:bpy.data.images.load(str(root/path),check_existing=True)
             for key,path in [('side','art/walking/maziss-side-atlas.png'),
                              ('depth','art/walking/maziss-depth-atlas.png'),
                              ('garment','art/walking/maziss-clean-garment-reference.png')]}
    for image in sources.values():
        image.colorspace_settings.name='sRGB';image.pack()
    for obj in objects:
        if obj.type!='MESH':continue
        positions=[];normals=[];matrix=obj.matrix_world
        for vertex in obj.data.vertices:
            positions.extend(matrix@vertex.co)
            normals.extend((matrix.to_3x3()@vertex.normal).normalized())
        group=obj.get('part_group','Body')
        info=paint_coordinates({'name':obj.name,'group':group,'positions':positions,'normals':normals})
        if info['paintKind']=='solid':continue
        for key in ('paintFront','paintBack','paintSide'):
            layer=obj.data.uv_layers.get(key) or obj.data.uv_layers.new(name=key)
            for loop in obj.data.loops:layer.data[loop.index].uv=info[key][loop.vertex_index*2:loop.vertex_index*2+2]
        attr=obj.data.color_attributes.get('PaintWeights') or obj.data.color_attributes.new(name='PaintWeights',type='FLOAT_COLOR',domain='CORNER')
        for loop in obj.data.loops:attr.data[loop.index].color=(*info['paintBlend'][loop.vertex_index*3:loop.vertex_index*3+3],1)
        mat=bpy.data.materials.new('Painted '+obj.name);mat.use_nodes=True
        fallback=PALETTE.get(group,'69503a');srgb=[int(fallback[i:i+2],16)/255 for i in (0,2,4)]
        linear=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in srgb]
        mat.diffuse_color=(*linear,1)
        nodes=mat.node_tree.nodes;links=mat.node_tree.links;nodes.clear()
        weights=nodes.new('ShaderNodeVertexColor');weights.layer_name='PaintWeights'
        split=nodes.new('ShaderNodeSeparateColor');links.new(weights.outputs['Color'],split.inputs['Color'])
        pigments=[]
        for i,key in enumerate(('paintFront','paintBack','paintSide')):
            mapping=nodes.new('ShaderNodeUVMap');mapping.uv_map=key
            image=nodes.new('ShaderNodeTexImage');image.extension='CLIP'
            source='garment' if info['paintKind']=='garment' else 'side' if i==2 else 'depth'
            image.image=sources[source];links.new(mapping.outputs['UV'],image.inputs['Vector'])
            mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(*linear,1)
            links.new(image.outputs['Alpha'],mix.inputs[0]);links.new(image.outputs['Color'],mix.inputs[2])
            weighted=nodes.new('ShaderNodeMixRGB');weighted.blend_type='MULTIPLY';weighted.inputs[0].default_value=1
            links.new(mix.outputs[0],weighted.inputs[1]);links.new(split.outputs[i],weighted.inputs[2]);pigments.append(weighted.outputs[0])
        add=nodes.new('ShaderNodeMixRGB');add.blend_type='ADD';add.inputs[0].default_value=1
        links.new(pigments[0],add.inputs[1]);links.new(pigments[1],add.inputs[2])
        final=nodes.new('ShaderNodeMixRGB');final.blend_type='ADD';final.inputs[0].default_value=1
        links.new(add.outputs[0],final.inputs[1]);links.new(pigments[2],final.inputs[2])
        emission=nodes.new('ShaderNodeEmission');links.new(final.outputs[0],emission.inputs['Color'])
        output=nodes.new('ShaderNodeOutputMaterial');links.new(emission.outputs[0],output.inputs['Surface'])
        obj.data.materials.clear();obj.data.materials.append(mat)
