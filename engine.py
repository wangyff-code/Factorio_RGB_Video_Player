
import json
import zlib
import base64
import numpy as np
from PIL import Image,ImageEnhance
from io import BytesIO
import imageio.v3 as iio
import av
import itertools
# 红线1 绿线2 电线5



def create_small_lamp(entity_number, x, y, signal_name):
    return {
                    "entity_number": entity_number,
                    "name": "small-lamp",
                    "position": {
                        "x": x,
                        "y": y
                    },
                    "control_behavior": {
                        "use_colors": True,
                        "rgb_signal": {
                            "name": signal_name
                        },
                        "color_mode": 2
                    },
                    "always_on": True
                }

def create_medium_electric_pole(entity_number, x, y):
    return{
                "entity_number": entity_number,
                "name": "medium-electric-pole",
                "position": {
                    "x": x,
                    "y": y
                }
            }

def create_constant_combinator(entity_number, x, y,constant_list):
    return{
                "entity_number": entity_number,
                "name": "constant-combinator",
                "position": {
                    "x": x,
                    "y": y
                },
                "control_behavior": {
                    "sections": {
                        "sections": [
                            {
                                "index": 1,
                                "filters": constant_list
                            }
                        ]
                    }
                }
            }


def create_constant_list(id,name,value):
    return{
        "index": id,
        "name": name,
        "quality": "normal",
        "comparator": "=",
        "count": value
    }



def create_decider_combinator(id,x,y,frane_num):
    return{
                "entity_number": id,
                "name": "decider-combinator",
                "position": {
                    "x": x,
                    "y": y
                },
                "direction": 8,
                "control_behavior": {
                    "decider_conditions": {
                        "conditions": [
                            {
                                "first_signal": {
                                    "type": "virtual",
                                    "name": "signal-F"
                                },
                                "constant": frane_num,
                                "comparator": "="
                            }
                        ],
                        "outputs": [
                            {
                                "signal": {
                                    "type": "virtual",
                                    "name": "signal-everything"
                                }
                            }
                        ]
                    }
                }
            }


def create_decider_combinator_f(id,x,y,max_count):
    return {
                "entity_number": id,
                "name": "decider-combinator",
                "position": {
                    "x": x,
                    "y": y
                },
                "direction": 4,
                "control_behavior": {
                    "decider_conditions": {
                        "conditions": [
                            {
                                "first_signal": {
                                    "type": "virtual",
                                    "name": "signal-F"
                                },
                                "constant": max_count
                            }
                        ],
                        "outputs": [
                            {
                                "signal": {
                                    "type": "virtual",
                                    "name": "signal-F"
                                }
                            }
                        ]
                    }
                }
            }

def create_arithmetic_combinator(id,x,y,operation,constant):
    return {
                "entity_number": id,
                "name": "arithmetic-combinator",
                "position": {
                    "x": x,
                    "y": y
                },
                "direction": 4,
                "control_behavior": {
                    "arithmetic_conditions": {
                        "first_signal": {
                            "type": "virtual",
                            "name": "signal-F"
                        },
                        "second_constant": constant,
                        "operation": operation,
                        "output_signal": {
                            "type": "virtual",
                            "name": "signal-F"
                        }
                    }
                }
            }





name_list=['wooden-chest', 'iron-chest', 'steel-chest', 'storage-tank', 'transport-belt', 'fast-transport-belt', 'express-transport-belt', 'underground-belt', 'fast-underground-belt', 'express-underground-belt', 'splitter', 'fast-splitter', 'express-splitter', 'burner-inserter', 'inserter', 'long-handed-inserter', 'fast-inserter', 'bulk-inserter', 'small-electric-pole', 'medium-electric-pole', 'big-electric-pole', 'substation', 'pipe', 'pipe-to-ground', 'pump', 'rail', 'train-stop', 'rail-signal', 'rail-chain-signal', 'locomotive', 'cargo-wagon', 'fluid-wagon', 'artillery-wagon', 'car', 'tank', 'spidertron', 'logistic-robot', 'construction-robot', 'active-provider-chest', 'passive-provider-chest', 'storage-chest', 'buffer-chest', 'requester-chest', 'roboport', 'small-lamp', 'arithmetic-combinator', 'decider-combinator', 'selector-combinator', 'power-switch', 'programmable-speaker', 'constant-combinator', 'display-panel', 'stone-brick', 'concrete', 'hazard-concrete', 'refined-concrete', 'refined-hazard-concrete', 'landfill', 'cliff-explosives', 'repair-pack', 'blueprint', 'upgrade-planner', 'deconstruction-planner', 'blueprint-book', 'boiler', 'steam-engine', 'solar-panel', 'accumulator', 'nuclear-reactor', 'heat-pipe', 'heat-exchanger', 'steam-turbine', 'burner-mining-drill', 'electric-mining-drill', 'offshore-pump', 'pumpjack', 'stone-furnace', 'steel-furnace', 'electric-furnace', 'assembling-machine-1', 'assembling-machine-2', 'assembling-machine-3', 'oil-refinery', 'chemical-plant', 'centrifuge', 'lab', 'beacon', 'speed-module', 'speed-module-2', 'speed-module-3', 'efficiency-module', 'efficiency-module-2', 'efficiency-module-3', 'productivity-module', 'productivity-module-2', 'productivity-module-3', 'rocket-silo', 'cargo-landing-pad', 'satellite', 'wood', 'coal', 'stone', 'iron-ore', 'copper-ore', 'uranium-ore', 'raw-fish', 'iron-plate', 'steel-plate', 'copper-plate', 'solid-fuel', 'plastic-bar', 'sulfur', 'battery', 'explosives', 'water-barrel', 'crude-oil-barrel', 'petroleum-gas-barrel', 'light-oil-barrel', 'heavy-oil-barrel', 'lubricant-barrel', 'sulfuric-acid-barrel', 'iron-gear-wheel', 'iron-stick', 'copper-cable', 'barrel', 'electronic-circuit', 'advanced-circuit', 'processing-unit', 'engine-unit', 'electric-engine-unit', 'flying-robot-frame', 'low-density-structure', 'rocket-fuel', 'rocket-part', 'gate', 'uranium-235', 'uranium-238', 'uranium-fuel-cell', 'depleted-uranium-fuel-cell', 'radar', 'land-mine', 'nuclear-fuel', 'automation-science-pack', 'logistic-science-pack', 'military-science-pack', 'chemical-science-pack', 'production-science-pack', 'utility-science-pack', 'space-science-pack', 'pistol', 'submachine-gun', 'shotgun', 'combat-shotgun', 'rocket-launcher', 'flamethrower', 'firearm-magazine', 'piercing-rounds-magazine', 'uranium-rounds-magazine', 'shotgun-shell', 'piercing-shotgun-shell', 'cannon-shell', 'explosive-cannon-shell', 'uranium-cannon-shell', 'explosive-uranium-cannon-shell', 'artillery-shell', 'rocket', 'explosive-rocket', 'atomic-bomb', 'flamethrower-ammo', 'grenade', 'cluster-grenade', 'poison-capsule', 'slowdown-capsule', 'light-armor', 'heavy-armor', 'modular-armor', 'power-armor', 'power-armor-mk2', 'solar-panel-equipment', 'fission-reactor-equipment', 'battery-equipment', 'battery-mk2-equipment', 'belt-immunity-equipment', 'exoskeleton-equipment', 'personal-roboport-equipment', 'personal-roboport-mk2-equipment', 'night-vision-equipment', 'energy-shield-equipment', 'energy-shield-mk2-equipment', 'personal-laser-defense-equipment', 'discharge-defense-equipment', 'stone-wall']


def encode_zlib_b64_json(json_data):

    json_str = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
    
    # 3. 将字符串转换为 UTF-8 字节流
    json_bytes = json_str.encode('utf-8')
    
    # 4. 使用 zlib 压缩
    compressed_bytes = zlib.compress(json_bytes)
    
    # 5. Base64 编码并转换为字符串
    b64_bytes = base64.b64encode(compressed_bytes)
    b64_str = b64_bytes.decode('utf-8')
    
    # 6. 在开头加上 '0'
    final_str = '0' + b64_str
    return final_str



def get_preview_base64(video_path, frame_idx):
    """
    抽取指定帧，按比例缩放至高度 100，返回 Base64 字符串供前端预览
    """
    try:
        # 使用 imageio 直接读取指定的一帧 (pyav 会直接返回 RGB 格式)
        frame = iio.imread(video_path, index=int(frame_idx), plugin="pyav")
        
        # 如果你在 engine.py 中发现颜色反了（比如变蓝了），可以加上这句:
        # frame = frame[:, :, ::-1] 
        
        img = Image.fromarray(frame)
        
        # 计算缩放尺寸：固定高度 100，宽度等比例计算
        w, h = img.size
        new_h = 100
        new_w = int(w * (new_h / h))
        
        # 缩放图片 (LANCZOS 采样保证缩放清晰度)
        # 兼容性提示：如果 Pillow 版本较老报错，可将 Image.Resampling.LANCZOS 改为 Image.LANCZOS
        img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # 将图片保存到内存中，并转为 Base64
        buffered = BytesIO()
        img_resized.save(buffered, format="JPEG", quality=85)
        img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {"success": True, "image": f"data:image/jpeg;base64,{img_b64}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def read_video(video_path,start_frame,end_frame,frame_interval):
    video_list = []
    with iio.imopen(video_path, "r", plugin="pyav") as file:
        for idx in range(start_frame, end_frame + 1):
            frame = file.read(index=idx)
            if idx % frame_interval == 0:
                corrected_frame = frame[:, :, ::-1]
                video_list.append(Image.fromarray(corrected_frame))
    return video_list

def read_video_iterator(video_path, start_frame, end_frame, frame_interval):
    # with 语句会在迭代器结束或中途中断时自动安全地关闭文件
    with iio.imopen(video_path, "r", plugin="pyav") as file:
        for idx in range(start_frame, end_frame + 1):
            # 优化：先判断是否满足间隔，满足再去读帧，极大提升速度
            if idx % frame_interval == 0:
                frame = file.read(index=idx)
                corrected_frame = frame[:, :, ::-1]
                # 使用 yield 返回单帧，而不是塞进 list
                yield Image.fromarray(corrected_frame)

class gen_item_class():
    def __init__(self):
        fac_dir = {
        "blueprint": {
            "icons": [
                {
                    "signal": {
                        "name": "steel-chest"
                    },
                    "index": 1
                }
            ],
            "entities": [
    
            ],
            "item": "blueprint",
            "version": 562949958402048
        }
        }
        self.entity_number = 0
        self.entities_list = []
        self.wire_list = []

    def add_small_lamp(self,x,y,index):
        self.entity_number += 1
        self.entities_list.append(create_small_lamp(self.entity_number,x,y,name_list[index]))
        return self.entity_number
    
    def add_medium_electric_pole(self,x,y):
        self.entity_number += 1
        self.entities_list.append(create_medium_electric_pole(self.entity_number,x,y))
        return self.entity_number

    def add_constant_combinator(self,x,y,constant_list):
        self.entity_number += 1
        self.entities_list.append(create_constant_combinator(self.entity_number,x,y,constant_list))
        return self.entity_number 

    def add_decider_combinator(self,x,y,frane_num): 
        self.entity_number += 1
        self.entities_list.append(create_decider_combinator(self.entity_number,x,y,frane_num))
        return self.entity_number 
    
    def add_decider_combinator_f(self,x,y,max_count): 
        self.entity_number += 1
        self.entities_list.append(create_decider_combinator_f(self.entity_number,x,y,max_count))
        return self.entity_number 

    def add_arithmetic_combinator(self,x,y,operation,constant):
        self.entity_number += 1
        self.entities_list.append(create_arithmetic_combinator(self.entity_number,x,y,operation,constant))
        return self.entity_number 


    def add_wire_list(self,nod1,port1,nod2,port2):
        self.wire_list.append([nod1,port1,nod2,port2])

    def pack(self):
        fac_dir = {
        "blueprint": {
            "icons": [
                {
                    "signal": {
                        "name": "small-lamp"
                    },
                    "index": 1
                }
            ],
            "entities": [
    
            ],
            "item": "blueprint",
            "version": 562949958402048
        }
        }
        fac_dir['blueprint']["entities"] = self.entities_list
        fac_dir['blueprint']["wires"] = self.wire_list
        return encode_zlib_b64_json(fac_dir)



def gen_screen(gen_item, x_offset, y_offset,line_type):
    lap_num = 0
    id_list = []
    electric_list = []
    lap_ele_list = []
    item_map = np.zeros((14,14),dtype=np.int32)-1
    
    # 完美覆盖 14x14 屏幕的 4 个中型电线杆相对坐标
    pole_coords = [(3, 3), (10, 3), (3, 10), (10, 10)]
    
    for i in range(14):
        # 蛇形走线
        if i % 2 == 0:
            y_range = range(0, 14) 
        else:
            y_range = range(13, -1, -1)
            
        for k in y_range:
            real_x = i + x_offset
            real_y = k + y_offset
            
            # 只有在这 4 个指定坐标才放置电线杆
            if (i, k) in pole_coords:
                # 记录电线杆ID（如果在 gen_item 中有返回值的话）
                electric_list.append(gen_item.add_medium_electric_pole(real_x, real_y))
                lap_ele_list.append(curr_id)
            else:
                curr_id = gen_item.add_small_lamp(real_x, real_y, lap_num)
                item_map[i][k] = lap_num
                id_list.append(curr_id)
                lap_num += 1
                
    # 连线逻辑完全不用改！
    # 因为是用 id_list 相邻连线，遇到电线杆没放灯泡时，
    # id_list 没增加，电线会自动跨过那个“坏点”连接下一个灯泡，完美！
    for index in range(len(id_list) - 1):
        curr_lamp = id_list[index]
        next_lamp = id_list[index + 1]
        
        gen_item.add_wire_list(curr_lamp, line_type, next_lamp, line_type)

    gen_item.add_wire_list(electric_list[0], 5, electric_list[1], 5)
    gen_item.add_wire_list(electric_list[1], 5, electric_list[2], 5)
    gen_item.add_wire_list(electric_list[2], 5, electric_list[3], 5)
    gen_item.add_wire_list(electric_list[3], 5, electric_list[0], 5)

    gen_item.add_wire_list(electric_list[0], 1, electric_list[1], 1)
    gen_item.add_wire_list(electric_list[0], 2, electric_list[1], 2)

    
    gen_item.add_wire_list(electric_list[2], 1, electric_list[3], 1)
    gen_item.add_wire_list(electric_list[2], 2, electric_list[3], 2)

    return item_map,electric_list,lap_ele_list



def gen_frame_constent(item_map,img):
    id = 1
    sig_list = []
    for i in range(0,14):
        for k in range(0,14):
            if(item_map[k][i] >= 0):
                color_index = item_map[k][i] 
                sig_list.append(create_constant_list(id,name_list[color_index],int(img[i][k])))
                id += 1

    return sig_list

def combine_14x14_patch(patch_array):
    """
    负责转换一小片的 14x14 矩阵
    :param patch_array: 形状为 (14, 14, 3) 的小碎片
    :return: 形状为 (14, 14) 的合并后矩阵
    """
    # 必须转为 uint32 防止溢出
    p32 = patch_array.astype(np.uint32)
    R = p32[:, :, 0]
    G = p32[:, :, 1]
    B = p32[:, :, 2]
    
    # 你的合并公式
    return R + G * 256 + B * 65536

def image_to_MN_patches(img, M, N):
    """
    M: 对应矩阵的行数 (高度方向有 M 个块)
    N: 对应矩阵的列数 (宽度方向有 N 个块)
    """
    
    # 1. 缩放图片
    # 注意：PIL 的 resize 接收的参数是 (宽, 高)
    # 所以宽是 14*N，高是 14*M
    target_width = 14 * N
    target_height = 14 * M
    # Image.Transpose.ROTATE_90 表示逆时针旋转 90 度
    # Image.Transpose.ROTATE_270 表示顺时针旋转 90 度
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Contrast(img_resized)
    img_resized = enhancer.enhance(1.5)
    # 转为 NumPy 数组，形状将是 (14*M, 14*N, 3)
    img_array = np.array(img_resized)
    
    # 2. 准备 M * N 的矩阵（这里用两层列表来装）
    grid_matrix = []
    
    for i in range(M):
        row_patches = []
        for j in range(N):
            # 3. 裁剪出 14x14 的图片碎片
            # i 控制行(y轴)，j 控制列(x轴)
            y_start, y_end = i * 14, (i + 1) * 14
            x_start, x_end = j * 14, (j + 1) * 14
            
            patch = img_array[y_start:y_end, x_start:x_end, :]  # 形状为 (14, 14, 3)
            
            # 4. 用函数处理这一小片
            combined_patch = combine_14x14_patch(patch)
            
            # 塞入行列表中
            row_patches.append(combined_patch)
            
        # 塞入总矩阵中
        grid_matrix.append(row_patches)
        
    # 为了方便后续使用，将 Python 嵌套列表转换为 NumPy 四维矩阵
    # 最终形状为 (M, N, 14, 14)
    return np.array(grid_matrix)

def get_video_info(video_path):
    """
    轻量级、极速、高准确率的视频信息获取。
    通过直接拆解视频包（demux）来数帧，跳过画面解码（decode），速度极快。
    """
    try:
        # 打开视频容器
        with av.open(video_path) as container:
            # 获取第一个视频流
            video_stream = container.streams.video[0]
            
            # 1. 获取帧率 (通常 average_rate 是一个分数对象，转为 float)
            fps = 24.0
            if video_stream.average_rate and video_stream.average_rate > 0:
                fps = float(video_stream.average_rate)
            elif video_stream.base_rate and video_stream.base_rate > 0:
                fps = float(video_stream.base_rate)
            
            # 2. 极速数帧法：只遍历数据包(Packet)，不解码成图像(Frame)
            total_frames = 0
            
            # demux() 是“解复用”，它只会把视频流中的压缩数据块（如H264块）剥离出来
            # 因为没有进行将 H264 还原成 RGB 像素矩阵的操作，所以耗时极短
            for packet in container.demux(video_stream):
                # 过滤掉偶尔出现的空数据包，正常的 packet 代表一帧
                if packet.dts is not None and packet.size > 0:
                    total_frames += 1
                    
        return {"success": True, "fps": round(fps, 2), "total_frames": total_frames}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def gen_video_blueprint(name,fps,start_frame,end_frame,frame_interval,progress_callback=None):

    video_stream  = read_video_iterator(name,start_frame,end_frame,frame_interval)
    img =  next(video_stream)

    clip_wide_num = int((img.width/img.height)*5)

    # === 新增：计算剩余要处理的总帧数 ===
    total_yields = sum(1 for x in range(start_frame, end_frame + 1) if x % frame_interval == 0)
    total_frames_expected = max(1, total_yields - 1) # 减去刚才 next() 消耗掉的第一帧

    gen_item = gen_item_class()

    row_list = []
    fram_sig_id_list = []

    new_fps = fps/frame_interval
    div_num = int(24/new_fps)
    max_count = end_frame - start_frame

    div_id = gen_item.add_arithmetic_combinator(0,-2,'/',div_num)
    frame_limit_id = gen_item.add_decider_combinator_f(0,-4,max_count)
    gen_f_id = gen_item.add_arithmetic_combinator(0,-6,'+',1)
    gen_item.add_wire_list(gen_f_id,3,frame_limit_id,1)
    gen_item.add_wire_list(frame_limit_id,3,gen_f_id,1)
    gen_item.add_wire_list(gen_f_id,3,div_id,1)
    frame_list = []

    if progress_callback:
        progress_callback(5, "正在初始化屏幕及基础线路...")
    # ==========================================
    # 准备缓存字典，用于在跨帧循环时保存状态
    # ==========================================
    disp_ctr_ports = {}
    item_maps = {}
    # line_ids_map 结构: {i: {k: [id2_list]}}
    line_ids_map = {i: {k: [] for k in range(5)} for i in range(clip_wide_num)}
    ele_line1_map = {i: [] for i in range(clip_wide_num)}
    ele_line2_map = {i: [] for i in range(clip_wide_num)}

    # ==========================================
    # 第一步：只与 i 相关的静态屏幕生成 (原循环的上半部分)
    # ==========================================
    for i in range(0, clip_wide_num):
        disp_ctr_port = []
        
        # 你的原代码: 生成屏幕和内部连线
        item_map,electric_list0,lap_ele_list = gen_screen(gen_item,14*i,14*0,2)
        disp_ctr_port.append(lap_ele_list[1])
        disp_ctr_port.append(electric_list0[1])
        disp_ctr_port.append(electric_list0[2])
        
        item_map,electric_list1,lap_ele_list = gen_screen(gen_item,14*i,14*1,2)
        gen_item.add_wire_list(electric_list0[0],1,electric_list1[1],1)
        gen_item.add_wire_list(electric_list0[0],2,electric_list1[1],2)
        gen_item.add_wire_list(electric_list0[0],5,electric_list1[1],5)
        gen_item.add_wire_list(electric_list0[3],1,electric_list1[2],1)
        gen_item.add_wire_list(electric_list0[3],2,electric_list1[2],2)
        gen_item.add_wire_list(electric_list0[3],5,electric_list1[2],5)
        gen_item.add_wire_list(electric_list1[1],2,lap_ele_list[1],2)
        electric_list0 = electric_list1

        item_map,electric_list1,lap_ele_list = gen_screen(gen_item,14*i,14*2,2)
        gen_item.add_wire_list(electric_list0[0],1,electric_list1[1],1)
        gen_item.add_wire_list(electric_list0[0],2,electric_list1[1],2)
        gen_item.add_wire_list(electric_list0[0],5,electric_list1[1],5)
        gen_item.add_wire_list(electric_list1[3],2,lap_ele_list[3],2)
        gen_item.add_wire_list(electric_list0[3],1,electric_list1[2],1)
        gen_item.add_wire_list(electric_list0[3],2,electric_list1[2],2)
        gen_item.add_wire_list(electric_list0[3],5,electric_list1[2],5)
        electric_list0 = electric_list1

        item_map,electric_list1,lap_ele_list  = gen_screen(gen_item,14*i,14*3,1)
        gen_item.add_wire_list(electric_list0[0],1,electric_list1[1],1)
        gen_item.add_wire_list(electric_list0[0],2,electric_list1[1],2)
        gen_item.add_wire_list(electric_list0[0],5,electric_list1[1],5)
        gen_item.add_wire_list(electric_list0[3],1,electric_list1[2],1)
        gen_item.add_wire_list(electric_list0[3],2,electric_list1[2],2)
        gen_item.add_wire_list(electric_list0[3],5,electric_list1[2],5)
        gen_item.add_wire_list(electric_list1[1],1,lap_ele_list[1],1)
        electric_list0 = electric_list1

        item_map,electric_list1,lap_ele_list  = gen_screen(gen_item,14*i,14*4,1)
        gen_item.add_wire_list(electric_list0[0],1,electric_list1[1],1)
        gen_item.add_wire_list(electric_list0[0],2,electric_list1[1],2)
        gen_item.add_wire_list(electric_list0[0],5,electric_list1[1],5)
        gen_item.add_wire_list(electric_list0[3],1,electric_list1[2],1)
        gen_item.add_wire_list(electric_list0[3],2,electric_list1[2],2)
        gen_item.add_wire_list(electric_list0[3],5,electric_list1[2],5)
        gen_item.add_wire_list(electric_list1[3],1,lap_ele_list[3],1)
        
        # 缓存该 i 下的 disp_ctr_port 和最终的 item_map 供后面使用
        disp_ctr_ports[i] = disp_ctr_port
        item_maps[i] = item_map

    # ==========================================
    # 第二步：按帧处理 (frame_num 循环在最外层！)
    # ==========================================
    for frame_num, frame in enumerate(video_stream):
        # === 新增：汇报百分比 (从 5% 增长到 90%) ===
        if progress_callback:
            percent = 5 + int((frame_num / total_frames_expected) * 85)
            progress_callback(percent, f"正在生成视频帧数据... ({frame_num + 1}/{total_frames_expected})")
        # 【性能优化核心】：一帧图片只解析一次！
        grid_matrix = image_to_MN_patches(frame, 5, clip_wide_num)
        
        for i in range(0, clip_wide_num):
            item_map = item_maps[i]
            disp_ctr_port = disp_ctr_ports[i]
            
            for k in range(0, 5):
                patch_array = grid_matrix[k][i]
                sig_list = gen_frame_constent(item_map, patch_array)
                id1 = gen_item.add_constant_combinator(i*14+3+k, -1-frame_num*3-2, sig_list)
                id2 = gen_item.add_decider_combinator(i*14+3+k, -1-frame_num*3, frame_num)
                gen_item.add_wire_list(id1, 2, id2, 2)
                
                if frame_num % 2 == 0 and k == 0:
                    ele_line1_map[i].append(gen_item.add_medium_electric_pole(i*14+2, -1-frame_num*3))
                if frame_num % 2 == 0 and k == 4:
                    ele_line2_map[i].append(gen_item.add_medium_electric_pole(i*14+4+k, -1-frame_num*3))
                
                # 将 id2 收集起来，等所有帧处理完再连线
                line_ids_map[i][k].append(id2)
                
                if frame_num == 0:
                    fram_sig_id_list.append(id2)
                    if k == 0:
                        gen_item.add_wire_list(id2, 4, disp_ctr_port[0], 2)
                    elif k == 1:
                        gen_item.add_wire_list(id2, 4, disp_ctr_port[1], 2)
                    elif k == 2:
                        gen_item.add_wire_list(id2, 4, disp_ctr_port[2], 2)
                    elif k == 3:
                        gen_item.add_wire_list(id2, 3, disp_ctr_port[1], 1)
                    elif k == 4:
                        gen_item.add_wire_list(id2, 3, disp_ctr_port[2], 1)
    if progress_callback:
        progress_callback(95, "正在进行信号与电网跨帧收尾连线...")
    # ==========================================
    # 第三步：跨帧连线 (原循环的收尾部分)
    # ==========================================
    for i in range(0, clip_wide_num):
        # 处理信号线连线
        for k in range(0, 5):
            line_id = line_ids_map[i][k]
            for line in range(0, len(line_id)-1):
                gen_item.add_wire_list(line_id[line], 1, line_id[line+1], 1)
                if k < 3:
                    gen_item.add_wire_list(line_id[line], 4, line_id[line+1], 4)
                else:
                    gen_item.add_wire_list(line_id[line], 3, line_id[line+1], 3)
    
        # 处理电线杆连线
        ele_line1 = ele_line1_map[i]
        ele_line2 = ele_line2_map[i]
        
        for line in range(0, len(ele_line1)-1):
            gen_item.add_wire_list(ele_line1[line], 5, ele_line1[line+1], 5)
        for line in range(0, len(ele_line2)-1):
            gen_item.add_wire_list(ele_line2[line], 5, ele_line2[line+1], 5)
    
        disp_ctr_port = disp_ctr_ports[i]
        if ele_line1 and ele_line2:
            gen_item.add_wire_list(ele_line1[0], 5, disp_ctr_port[1], 5) 
            gen_item.add_wire_list(ele_line2[0], 5, disp_ctr_port[1], 5)  
            row_list.append(ele_line1[0])   
            row_list.append(ele_line2[0])

    for line in range(0,len(row_list)-1):
        gen_item.add_wire_list(row_list[line],5,row_list[line+1],5)


    for line in range(0,len(fram_sig_id_list)-1):
        gen_item.add_wire_list(fram_sig_id_list[line],1,fram_sig_id_list[line+1],1)
        if line == 0:
            gen_item.add_wire_list(div_id,3,fram_sig_id_list[0],1)
    if progress_callback:
        progress_callback(100, "生成完毕，正在编码 JSON 数据...")
    return gen_item.pack()

if __name__ == "__main__":
    name = r'D:/A_step/blue/p/猫和老鼠 - S01E85 - 室内溜冰场.mkv'
    b = gen_video_blueprint(name,24,0,400,4)
    f = open('o.txt','w')
    f.write(b)
    f.close()