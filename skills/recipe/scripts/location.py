"""
本模块主要用来获取当前地理位置

"""

import datetime
import os
import sys
import requests
from dotenv import load_dotenv


# ─── 编码修复 ───
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# 加载配置.env文件
load_dotenv()

def get_location_season() -> str:
    """

    获取当前季节

    Returns:
        str: 当前季节，例如：春季，夏季 ，秋季，冬季
    """
    # 获取当前月份
    month = datetime.datetime.now().month
    # 根据月份来输出季节
    if month in [3, 4, 5]:
        return "春季"
    elif month in [6, 7, 8]:
        return "夏季"
    elif month in [9, 10, 11]:
        return "秋季"
    elif month in [12, 1, 2]:
        return "冬季"
    else:
        return None
    
    

def get_loaction_city(ak:str)-> str:
    """
    
    通过百度地图 IP 定位接口获取当前位置的城市名称。

    Args:
        ak (str): 百度地图开放平台的访问密钥

    Returns:
        str:  获取到的城市名称，如果失败则返回 None
    """
    # 百度地图 IP 定位 API 请求地址
    url = "https://api.map.baidu.com/location/ip"
    # 请求参数
    # ip: 如果为空或省略，则默认为发起请求的客户端当前 IP
    # coor: 坐标类型，bd09ll 表示百度经纬度坐标
    params = {
        'ak': ak,
    }
    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)
        
        # 如果请求状态码不是 200，说明请求失败
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
        # 解析返回的 JSON 数据
        result = response.json()
        
        # 检查接口返回的状态码，0 表示成功
        if result.get('status') == 0:
            # 获取 content 下的 address_detail 中的 city 字段
            # 结构通常是: {'content': {'address_detail': {'city': '北京市'}}}
            city = result.get('content', {}).get('address_detail', {}).get('city')
            return city
        else:
            # 接口返回错误信息
            print(f"API 返回错误: {result.get('message')}")
            return None
            
    except requests.exceptions.RequestException as e:
        # 处理网络请求过程中的异常（如连接超时、DNS错误等）
        print(f"发生网络请求异常: {e}")
        return None
    except Exception as e:
        # 处理其他未知异常
        print(f"发生未知异常: {e}")
        return None

def main():  # 定义主函数 main
    # 获取环境变量中的百度地图 AK
    a_map_key = os.getenv("AMAP_KEY")
    if a_map_key is None:
        print("未找到环境变量 AMAP_KEY，请检查配置。")
        return
    # 调用 get_loaction_city 函数获取当前地理位置
    city = get_loaction_city(a_map_key)
    if city is None:
        print("获取城市失败。")
        return
    # 调用 get_location_season 函数获取当前季节
    season = get_location_season()
    if season is None:
        print("获取季节失败。")
        return
    # 打印结果
    print(f"当前城市是：{city}，当前季节是：{season}")
    


if __name__ == '__main__':
    main()