import asyncio
import aiohttp
import os
from typing import Set, List

async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore, results: Set[str]):
    """异步获取单个URL的内容"""
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=15)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content = await response.text()
                    process_content(content, results)
                    print(f"成功处理: {url}")
                else:
                    print(f"获取失败 {url}: 状态 {response.status}")
        except Exception as e:
            print(f"获取错误 {url}: {str(e)}")

def process_content(content: str, results: Set[str]):
    """处理获取的内容 - 跳过Base64解码，直接处理纯文本"""
    content = content.strip()
    
    # 直接处理文本内容，不尝试Base64解码
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and line not in results:
            # 检查是否是有效的订阅链接格式
            if is_valid_subscription_link(line):
                results.add(line)
            else:
                print(f"跳过无效链接: {line[:50]}...")  # 只显示前50个字符

def is_valid_subscription_link(line: str) -> bool:
    """检查是否是有效的订阅链接格式"""
    # 常见的订阅协议前缀
    subscription_prefixes = [
        "vmess://", "vless://", "trojan://", "ss://", 
        "ssr://", "http://", "https://", "socks://",
        "hysteria://", "hy2://", "tuic://"
    ]
    
    return any(line.startswith(prefix) for prefix in subscription_prefixes)

def split_by_size(results: Set[str], max_size_mb=90):
    """按文件大小分割结果集"""
    results_list = list(results)
    total_lines = len(results_list)
    
    print(f"总订阅数: {total_lines}, 开始按大小分割...")
    
    output_files = []
    current_file_index = 1
    current_size = 0
    current_file = None
    max_size_bytes = max_size_mb * 1024 * 1024  # 转换为字节
    
    for i, line in enumerate(results_list):
        line_size = len(line.encode('utf-8')) + 1  # +1 用于换行符
        
        # 如果当前文件不存在或添加这行会超过限制，则创建新文件
        if current_file is None or current_size + line_size > max_size_bytes:
            if current_file:
                current_file.close()
            
            filename = f"subscriptions_{current_file_index:03d}.txt"
            output_files.append(filename)
            current_file = open(filename, 'w', encoding='utf-8')
            print(f"创建文件: {filename}")
            current_file_index += 1
            current_size = 0
        
        # 写入行到当前文件
        current_file.write(line + '\n')
        current_size += line_size
        
        # 显示进度
        if (i + 1) % 1000 == 0 or (i + 1) == total_lines:
            print(f"处理进度: {i+1}/{total_lines} ({((i+1)/total_lines*100):.1f}%)")
    
    # 关闭最后一个文件
    if current_file:
        current_file.close()
    
    print(f"分割完成! 共创建 {len(output_files)} 个文件")
    return output_files

def create_info_file(output_files: List[str]):
    """创建信息文件，说明文件内容"""
    info_content = f"""# 订阅文件信息

此目录包含 {len(output_files)} 个独立的订阅文件。

## 文件列表

"""
    
    total_lines = 0
    total_size = 0
    for filename in sorted(output_files):
        line_count = sum(1 for _ in open(filename, 'r', encoding='utf-8'))
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        info_content += f"- `{filename}`: {line_count:,} 个订阅, {file_size:.2f} MB\n"
        total_lines += line_count
        total_size += file_size
    
    info_content += f"""
## 总计
- 总文件数: {len(output_files)}
- 总订阅数: {total_lines:,}
- 总大小: {total_size:.2f} MB
- 生成时间: {os.popen('date').read().strip()}

## 使用说明
每个文件都是独立的，包含有效的订阅链接，可以直接使用。
无需合并，每个文件都可以单独导入到支持的客户端中。

## 注意事项
所有订阅链接都以原始格式保存，未进行Base64解码。
只包含有效的订阅协议链接（vmess://, vless://, trojan://, ss://, ssr://, http://, https://, socks://, hysteria://, hy2://, tuic://）。
"""
    
    with open("SUBSCRIPTIONS_INFO.md", "w", encoding='utf-8') as f:
        f.write(info_content)
    
    print("已创建信息文件: SUBSCRIPTIONS_INFO.md")

async def main():
    """主函数，异步获取所有URL的内容"""
    # 从文件读取URL列表
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"发现 {len(urls)} 个URL需要处理")
    
    # 限制并发数，避免过多请求
    semaphore = asyncio.Semaphore(5)
    results = set()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_url(session, url, semaphore, results))
            tasks.append(task)
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
    
    print(f"完成! 共收集 {len(results)} 个唯一订阅")
    
    # 按大小分割成多个TXT文件
    output_files = split_by_size(results)
    
    # 创建信息文件
    create_info_file(output_files)

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
