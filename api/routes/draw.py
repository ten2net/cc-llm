import json
import secrets
import time
import base64
import requests
import hashlib
import json
import random

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from string import Template
from api.config import config
from api.routes.chat import create_chat_completion

from api.models import GENERATE_MDDEL
from api.routes.utils import check_requests, create_error_response, check_api_key
from api.utils.protocol import (
    ChatCompletionRequest,
    CompletionRequest,
    CompletionResponseStreamChoice,
    CompletionStreamResponse,
    UsageInfo,
)
from api.utils.protocol import CompletionResponse, CompletionResponseChoice
from gradio_client import Client
from loguru import logger

draw_router = APIRouter()

@draw_router.post("/draw")
async def create_draw(request: dict):
    prompt_origin = request['payload']['payload']['messagePlainContent']
    prompt = prompt_origin[prompt_origin.index(" ") + 1:]
    print(prompt)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "你是一位优秀的文字工作者，你擅长对文字进行总结并从中提炼出意境。你的任务是对用户输入的文本进行总结提炼后，用英文输出结果"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 1.0,
        "max_new_tokens": 50,
        "echo": False,
        "stream": False
    }
    
    # response = requests.post(url, headers=headers, json=data)
    response = await create_chat_completion(ChatCompletionRequest(**data),data)
    
    # get_test_url= f"http://{host}/test/{id}/"
    
    prompt_en = response.choices[0].message.content      
    logger.info(f'===8888===\n {prompt_en}')
        
    client = Client(config.FOOOCUS_BASE_URL, serialize=False)
    
    style_keys = ['官方 无风格', '官方 3D 模型', '官方 胶片', '官方 动画', '官方 电影', '官方 漫画书', '官方 手工粘土', '官方 数码艺术', '官方 增强', '官方 幻想艺术', '官方 等距轴测', '官方 线条艺术', '官方 低多边形', '官方 霓虹朋克', '官方 折纸', '官方 摄影', '官方 像素艺术', '官方 纹理', '广告 广告', '广告 汽车', '广告 企业', '广告 时尚编辑', '广告 食品摄影', '广告 奢侈品', '广告 房地产', '广告 零售', '艺术风格 抽象', '艺术风格 抽象表现主义', '艺术风格 装饰艺术', '艺术风格 新艺术', '艺术风格 建构主义', '艺术风格 立体派', '艺术风格 表现主义', '艺术风格 涂鸦', '艺术风格 超写实主义', '艺术风格 印象派', '艺术风格 点彩画', '艺术风格 流行艺术', '艺术风格 迷幻', '艺术风格 文艺复兴', '艺术风格 蒸汽朋克', '艺术风格 超现实主义', '艺术风格 印刷艺术', '艺术风格 水彩', '未来主义 生物机械', '未来主义 生物机械 赛博朋克', '未来主义 赛博朋克', '未来主义 赛博机器人', '未来主义 赛博朋克城市景观', '未来主义 未来主义', '未来主义 复古赛博朋克', '未来主义 复古未来主义', '未来主义 科幻小说', '未来主义 蒸汽波', '游戏 泡泡龙', '游戏 赛博朋克游戏', '游戏 格斗游戏', '游戏 Gta', '游戏 马里奥', '游戏 魔兽', '游戏 宠物小精灵', '游戏 复古街机', '游戏 复古游戏', '游戏 Rpg幻想游戏', '游戏 策略游戏', '游戏 街头霸王', '游戏 塞尔达', '杂项 建筑', '杂项 迪斯科', '杂项 梦境', '杂项 乌托邦', '杂项 童话', '杂项 哥特式', '杂项 垃圾摇滚', '杂项 恐怖', '杂项 卡哇伊', '杂项 魔幻', '杂项 黑色幽默', '杂项 漫画', '杂项 大都会', '杂项 极简主义', '杂项 单色', '杂项 航海', '杂项 空间', 'M杂项 染色玻璃', '杂项 科技时尚', '杂项 部落', '杂项 方格', '纸模 拼贴', '纸模 平面剪纸', '纸模 桐纸', '纸模 纸浆', '纸模 纸扎', '纸模 剪纸拼贴', '纸模 剪纸影盒', '纸模 叠剪纸', '纸模 厚层剪纸', '照片 异形', '照片 黑色', '照片 高清', '照片 长曝光', '照片 霓虹迷踪', '照片 剪影', '照片 倾斜摄影']
    
    style_keys_en =['Default (Slightly Cinematic)', 
                 'SAI 3D Model', 'SAI Analog Film', 
                 'SAI Anime动物', 'SAI Cinematic', 
                 'SAI Comic Book', 'SAI Craft Clay', 
                 'SAI Digital Art', 'SAI Enhance', 
                 'SAI Fantasy Art', 'SAI Isometric', 
                 'SAI Line Art', 'SAI Lowpoly', 'SAI Neonpunk', 
                 'SAI Origami', 'SAI Photographic', 'SAI Pixel Art', 
                 'SAI Texture', 'Ads Advertising', 'Ads Automotive', 
                 'Ads Corporate', 'Ads Fashion Editorial',
                 'Ads Food Photography', 'Ads Luxury', 
                 'Ads Real Estate', 'Ads Retail', 
                 'Artstyle Abstract', 'Artstyle Abstract Expressionism',
                 'Artstyle Art Deco', 'Artstyle Art Nouveau', 
                 'Artstyle Constructivist', 'Artstyle Cubist', 
                 'Artstyle Expressionist', 'Artstyle Graffiti', 
                 'Artstyle Hyperrealism', 'Artstyle Impressionist',
                 'Artstyle Pointillism', 'Artstyle Pop Art', 
                 'Artstyle Psychedelic', 'Artstyle Renaissance', 
                 'Artstyle Steampunk', 'Artstyle Surrealist', 
                 'Artstyle Typography', 'Artstyle Watercolor', 
                 'Futuristic Biomechanical', 'Futuristic Biomechanical Cyberpunk',
                 'Futuristic Cybernetic', 'Futuristic Cybernetic Robot', 
                 'Futuristic Cyberpunk Cityscape', 'Futuristic Futuristic',
                 'Futuristic Retro Cyberpunk', 'Futuristic Retro Futurism', 
                 'Futuristic Sci Fi', 'Futuristic Vaporwave', 
                 'Game Bubble Bobble', 'Game Cyberpunk Game', 
                 'Game Fighting Game', 'Game Gta', 'Game Mario', 
                 'Game Minecraft', 'Game Pokemon', 
                 'Game Retro Arcade', 'Game Retro Game', 
                 'Game Rpg Fantasy Game', 'Game Strategy Game',
                 'Game Streetfighter', 'Game Zelda', 
                 'Misc Architectural', 'Misc Disco', 
                 'Misc Dreamscape', 'Misc Dystopian', 
                 'Misc Fairy Tale', 'Misc Gothic', 
                 'Misc Grunge', 'Misc Horror', 
                 'Misc Kawaii', 'Misc Lovecraftian', 
                 'Misc Macabre', 'Misc Manga', 
                 'Misc Metropolis', 'Misc Minimalist', 
                 'Misc Monochrome', 'Misc Nautical', 
                 'Misc Space', 'Misc Stained Glass', 
                 'Misc Techwear Fashion', 'Misc Tribal', 
                 'Misc Zentangle', 'Papercraft Collage', 
                 'Papercraft Flat Papercut', 'Papercraft Kirigami', 
                 'Papercraft Paper Mache', 'Papercraft Paper Quilling', 
                 'Papercraft Papercut Collage', 'Papercraft Papercut Shadow Box', 
                 'Papercraft Stacked Papercut', 'Papercraft Thick Layered Papercut', 
                 'Photo Alien', 'Photo Film Noir', 'Photo Hdr', 'Photo Long Exposure',
                 'Photo Neon Noir', 'Photo Silhouette', 'Photo Tilt Shift', 
                 'Cinematic Diva', 'Abstract Expressionism', 
                 'Academia', 'Action Figure', 
                 'Adorable 3D Character', 'Adorable Kawaii', 
                 'Art Deco', 'Art Nouveau', 'Astral Aura', 
                 'Avant Garde', 'Baroque', 'Bauhaus Style Poster',
                 'Blueprint Schematic Drawing', 'Caricature', 
                 'Cel Shaded Art', 'Character Design Sheet', 
                 'Classicism Art', 'Color Field Painting', 
                 'Colored Pencil Art', 'Conceptual Art', 
                 'Constructivism', 'Cubism', 'Dadaism',
                 'Dark Fantasy', 'Dark Moody Atmosphere', 
                 'Dmt Art Style', 'Doodle Art', 
                 'Double Exposure', 'Dripping Paint Splatter Art', 
                 'Expressionism', 'Faded Polaroid Photo', 
                 'Fauvism', 'Flat 2d Art', 'Fortnite Art Style', 
                 'Futurism', 'Glitchcore', 'Glo Fi', 
                 'Googie Art Style', 'Graffiti Art', 
                 'Harlem Renaissance Art', 'High Fashion', 
                 'Idyllic', 'Impressionism', 
                 'Infographic Drawing', 'Ink Dripping Drawing', 
                 'Japanese Ink Drawing', 'Knolling Photography', 
                 'Light Cheery Atmosphere', 'Logo Design', 
                 'Luxurious Elegance', 'Macro Photography', 
                 'Mandola Art', 'Marker Drawing', 'Medievalism', 
                 'Minimalism', 'Neo Baroque', 'Neo Byzantine',
                 'Neo Futurism', 'Neo Impressionism', 'Neo Rococo', 
                 'Neoclassicism', 'Op Art', 
                 'Ornate And Intricate', 'Pencil Sketch Drawing', 
                 'Pop Art 2', 'Rococo', 'Silhouette Art', 'Simple Vector Art', 'Sketchup', 'Steampunk 2', 'Surrealism', 'Suprematism', 'Terragen', 'Tranquil Relaxing Atmosphere', 'Sticker Designs', 'Vibrant Rim Light', 'Volumetric Lighting', 'Watercolor 2', 'Whimsical And Playful']
    # 随机选择2个条目
    random_styles = random.choices(style_keys, k=1)
    result = client.predict(
            prompt_en,	# str in 'parameter_8' Textbox component
            "",	# str in '负向提示词' Textbox component
            # ["Cinematic Diva"], #random_styles, #  ["Fooocus V2","SAI 3D Model"],	# List[str] in '图片风格' Checkboxgroup component
            random_styles, #  ["Fooocus V2","SAI 3D Model"],	# List[str] in '图片风格' Checkboxgroup component
            # ["广告 房地产"], #  ["Fooocus V2","SAI 3D Model"],	# List[str] in '图片风格' Checkboxgroup component
            "Speed",	# str in '性能' Radio component
            "1024×960",	# str in '宽高比' Radio component
            1,	# int | float (numeric value between 1 and 32) in '图像数量' Slider component
            random.randint(0, 100),	# int | float in '种子' Number component
            0,	# int | float (numeric value between 0.0 and 30.0) in '采样清晰度' Slider component
            "sd_xl_base_1.0_0.9vae.safetensors",	# str (Option from: ['sd_xl_refiner_1.0_0.9vae.safetensors', 'sd_xl_base_1.0_0.9vae.safetensors']) in 'SDXL 基础模型' Dropdown component
            "sd_xl_refiner_1.0_0.9vae.safetensors",	# str (Option from: ['None', 'sd_xl_refiner_1.0_0.9vae.safetensors', 'sd_xl_base_1.0_0.9vae.safetensors']) in 'SDXL 增强模型' Dropdown component
            "None",	# str (Option from: ['None', '中国水墨画-Chinese_Ink_Painting_style.safetensors', '彩铅-Colored lead_v1.0.safetensors', '卡通证件照_v1.0.safetensors', '神秘光符-GlowingRunesAIv4-000005.safetensors', '女性机甲-XM机械纪元_v1.0.safetensors', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 1' Dropdown component
            -2,	# int | float (numeric value between -2 and 2) in '权重' Slider component
            "None",	# str (Option from: ['None', '中国水墨画-Chinese_Ink_Painting_style.safetensors', '彩铅-Colored lead_v1.0.safetensors', '卡通证件照_v1.0.safetensors', '神秘光符-GlowingRunesAIv4-000005.safetensors', '女性机甲-XM机械纪元_v1.0.safetensors', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 2' Dropdown component
            -2,	# int | float (numeric value between -2 and 2) in '权重' Slider component
            "None",	# str (Option from: ['None', '中国水墨画-Chinese_Ink_Painting_style.safetensors', '彩铅-Colored lead_v1.0.safetensors', '卡通证件照_v1.0.safetensors', '神秘光符-GlowingRunesAIv4-000005.safetensors', '女性机甲-XM机械纪元_v1.0.safetensors', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 3' Dropdown component
            -2,	# int | float (numeric value between -2 and 2) in '权重' Slider component
            "None",	# str (Option from: ['None', '中国水墨画-Chinese_Ink_Painting_style.safetensors', '彩铅-Colored lead_v1.0.safetensors', '卡通证件照_v1.0.safetensors', '神秘光符-GlowingRunesAIv4-000005.safetensors', '女性机甲-XM机械纪元_v1.0.safetensors', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 4' Dropdown component
            -2,	# int | float (numeric value between -2 and 2) in '权重' Slider component
            "None",	# str (Option from: ['None', '中国水墨画-Chinese_Ink_Painting_style.safetensors', '彩铅-Colored lead_v1.0.safetensors', '卡通证件照_v1.0.safetensors', '神秘光符-GlowingRunesAIv4-000005.safetensors', '女性机甲-XM机械纪元_v1.0.safetensors', 'sd_xl_offset_example-lora_1.0.safetensors']) in 'SDXL LoRA 5' Dropdown component
            -2,	# int | float (numeric value between -2 and 2) in '权重' Slider component
            fn_index=4
    )

    mdCode = [
    f"![{prompt}]({config.FOOOCUS_BASE_URL + '/file=' + item['name']})"
    for item in result[3]['value']
    ]
    # 构建请求的URL和数据
    template = Template("[md] $mdCode [/md]")
    files ='\n'.join(mdCode)
    content = template.substitute(mdCode=files)    
    
    # mdFilePath = "result.md"
    # with open(mdFilePath, "w") as file:
    #     file.write(files)
    
    groupId = request['payload']['payload']['groupId']
    converseId = request['payload']['payload']['converseId']
    messageId = request['payload']['payload']['messageId']
    messageAuthor = request['payload']['payload']['messageAuthor']
    messageSnippet = request['payload']['payload']['messageSnippet']
    userId = request['payload']['userId']
    
   
    url = config.CCTALKS_BASE_URL+'/api/openapi/bot/login'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'appId': config.CCTALKS_BOT_APPID,
        'token': hashlib.md5((config.CCTALKS_BOT_APPID + config.CCTALKS_BOT_SECRET).encode('utf-8')).hexdigest()
    }
    
    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        json_data = response.json()
        jwt_token = json_data['data']['jwt']
        
        url = config.CCTALKS_BASE_URL+"/api/chat/message/sendMessage"
        headers = {
            "Content-Type": "application/json",
            "X-Token": jwt_token
        }
        body = {
            "converseId": converseId,
            "groupId": groupId,
            "content": content, # result[3]['value'][0]['name'],
            "plain": content,
            "meta": {
                "mentions": [messageAuthor],
                "reply": {
                    "_id": messageId,
                    "author": messageAuthor,
                    "content": messageSnippet + " 风格: " + ', '.join(random_styles)
                }
            }
        }

        response = requests.post(url, headers=headers, json=body)        
        
    else:
        print('Request failed with status code:', response.status_code)  
    return files  
    # logger.info(f"consume time  = {(time.time() - start_time)}s, response = {str(choices)}")
 


