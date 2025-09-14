import asyncio
import aiohttp
import base64
import re
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
    """处理获取的内容"""
    content = content.strip()
    
    # 检查是否是Base64编码
    if re.match(r'^[A-Za-z0-9+/=]+$', content):
        try:
            # 尝试解码Base64
            decoded = base64.b64decode(content).decode('utf-8')
            lines = decoded.split('\n')
            for line in lines:
                line = line.strip()
                if line and line not in results:
                    results.add(line)
            return
        except:
            pass  # 如果不是有效的Base64，继续处理原始内容
    
    # 处理文本内容
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and line not in results:
            results.add(line)

def split_into_multiple_txt_files(results: Set[str], max_lines_per_file=50000):
    """将结果集分割成多个TXT文件"""
    results_list = list(results)
    total_lines = len(results_list)
    num_files = (total_lines + max_lines_per_file - 1) // max_lines_per_file  # 向上取整
    
    print(f"总订阅数: {total_lines}, 分割为 {num_files} 个文件")
    
    output_files = []
    
    for i in range(num_files):
        start_idx = i * max_lines_per_file
        end_idx = min((i + 1) * max_lines_per_file, total_lines)
        
        filename = f"subscriptions_{i+1:03d}.txt"
        output_files.append(filename)
        
        with open(filename, 'w', encoding='utf-8') as f:
            for j in range(start_idx, end_idx):
                f.write(results_list[j] + '\n')
        
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        print(f"创建文件: {filename} (包含 {end_idx - start_idx} 行, {file_size:.2f} MB)")
    
    return output_files

def create_info_file(output_files: List[str]):
    """创建信息文件，说明文件内容"""
    info_content = f"""# 订阅文件信息

此目录包含 {len(output_files)} 个独立的订阅文件。

## 文件列表

"""
    
    total_lines = 0
    for filename in sorted(output_files):
        line_count = sum(1 for _ in open(filename, 'r', encoding='utf-8'))
        file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
        info_content += f"- `{filename}`: {line_count:,} 个订阅, {file_size:.2f} MB\n"
        total_lines += line_count
    
    info_content += f"""
## 总计
- 总文件数: {len(output_files)}
- 总订阅数: {total_lines:,}
- 生成时间: {os.popen('date').read().strip()}

## 使用说明
每个文件都是独立的，包含有效的订阅链接，可以直接使用。
无需合并，每个文件都可以单独导入到支持的客户端中。
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
    
    # 分割成多个TXT文件
    output_files = split_into_multiple_txt_files(results)
    
    # 创建信息文件
    create_info_file(output_files)

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
