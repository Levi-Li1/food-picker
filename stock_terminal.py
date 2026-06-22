"""
股票行情展示终端 v2.0
数据源：新浪财经
"""

import requests
import json
import time
from datetime import datetime
import sys

# 新浪财经API
SINA_FINANCE_URL = "https://hq.sinajs.cn/list={codes}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://finance.sina.com.cn/"
}

def get_stock_data(stock_codes):
    """获取股票数据"""
    if not stock_codes:
        return []
    
    codes_str = ",".join(stock_codes)
    try:
        url = SINA_FINANCE_URL.format(codes=codes_str)
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = 'gbk'
        
        stocks = []
        lines = resp.text.strip().split('\n')
        
        for i, line in enumerate(lines):
            if '=' not in line:
                continue
            
            code_with_quote = line.split('=')[1].strip('";\n ')
            if not code_with_quote:
                stocks.append({"code": stock_codes[i], "name": "--", "error": True})
                continue
            
            parts = code_with_quote.split(',')
            if len(parts) >= 32:
                stocks.append({
                    "code": stock_codes[i],
                    "name": parts[0],
                    "open": parts[1],
                    "close": parts[2],
                    "price": parts[3],
                    "high": parts[4],
                    "low": parts[5],
                    "volume": parts[8],
                    "amount": parts[9],
                    "change": float(parts[3]) - float(parts[2]) if parts[2] != '0' else 0,
                })
            elif len(parts) >= 4:
                stocks.append({
                    "code": stock_codes[i],
                    "name": parts[0],
                    "price": parts[3] if len(parts) > 3 else "--",
                    "open": "--", "close": "--", "high": "--", "low": "--",
                    "volume": "--", "amount": "--", "change": 0,
                    "error": len(parts) < 10
                })
        return stocks
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def get_index_data():
    """获取主要指数"""
    indices = [
        "sh000001",  # 上证指数
        "sz399001",  # 深证成指
        "sz399006",  # 创业板指
        "sh000300",  # 沪深300
        "sh000016",  # 上证50
        "sh000688",  # 科创50
    ]
    return get_stock_data(indices)

def get_hot_stocks(market="sh", limit=10):
    """获取热门股票"""
    # 涨幅榜 - 简化版
    if market == "sh":
        return get_stock_data([
            "sh600519", "sh601318", "sh600036", "sh600276",
            "sh600887", "sh601166", "sh601328", "sh600030"
        ])
    else:
        return get_stock_data([
            "sz000858", "sz002594", "sz000333", "sz002415",
            "sz000001", "sz300750", "sz002460", "sz300059"
        ])

def format_number(num):
    """格式化数字"""
    if num == "--" or num is None:
        return "--"
    try:
        return f"{float(num):.2f}"
    except:
        return str(num)

def format_percent(stock):
    """计算涨跌幅"""
    try:
        if stock.get("close") and float(stock["close"]) > 0:
            change = float(stock["price"]) - float(stock["close"])
            pct = (change / float(stock["close"])) * 100
            return f"{change:+.2f}", f"{pct:+.2f}%"
    except:
        pass
    return "--", "--"

def format_volume(num):
    """格式化成交量"""
    if num == "--" or num is None:
        return "--"
    try:
        vol = float(num)
        if vol >= 100000000:
            return f"{vol/100000000:.2f}亿"
        elif vol >= 10000:
            return f"{vol/10000:.2f}万"
        return f"{vol:.0f}"
    except:
        return str(num)

def clear_screen():
    """清屏"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印表头"""
    print("=" * 80)
    print(f"  股票行情终端 v2.0  |  更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

def print_indices(indices):
    """打印指数"""
    print("\n【大盘指数】")
    print("-" * 70)
    print(f"{'名称':<12} {'代码':<12} {'现价':>10} {'涨跌':>10} {'涨跌幅':>10} {'成交量':>12}")
    print("-" * 70)
    
    for stock in indices:
        if stock.get("error"):
            print(f"{stock['code']:<12} 获取失败")
            continue
        
        change, pct = format_percent(stock)
        change_val = float(change) if change != "--" else 0
        
        # 颜色代码
        color = ""
        reset = ""
        if change_val > 0:
            color = "\033[92m"  # 绿色
            reset = "\033[0m"
        elif change_val < 0:
            color = "\033[91m"  # 红色
            reset = "\033[0m"
        
        vol = format_volume(stock.get("volume", "--"))
        name = stock["name"] if len(stock["name"]) <= 6 else stock["name"][:6]
        
        print(f"{name:<12} {stock['code']:<12} "
              f"{color}{format_number(stock['price']):>10}{reset} "
              f"{color}{change:>10}{reset} "
              f"{color}{pct:>10}{reset} "
              f"{vol:>12}")

def print_stocks(stocks, title="【自选股票】"):
    """打印股票列表"""
    print(f"\n{title}")
    print("-" * 90)
    print(f"{'名称':<10} {'代码':<12} {'现价':>10} {'涨跌':>10} {'涨跌幅':>10} {'最高':>10} {'最低':>10}")
    print("-" * 90)
    
    for stock in stocks:
        if stock.get("error"):
            print(f"{stock['code']:<10} 数据不可用")
            continue
        
        change, pct = format_percent(stock)
        change_val = float(change) if change != "--" else 0
        
        color = ""
        reset = ""
        if change_val > 0:
            color = "\033[92m"
            reset = "\033[0m"
        elif change_val < 0:
            color = "\033[91m"
            reset = "\033[0m"
        
        name = stock["name"] if len(stock["name"]) <= 6 else stock["name"][:6]
        
        print(f"{name:<10} {stock['code']:<12} "
              f"{color}{format_number(stock['price']):>10}{reset} "
              f"{color}{change:>10}{reset} "
              f"{color}{pct:>10}{reset} "
              f"{format_number(stock.get('high', '--')):>10} "
              f"{format_number(stock.get('low', '--')):>10}")

def print_footer():
    """打印页脚"""
    print("\n" + "=" * 80)
    print("  操作: R-刷新  Q-退出  A-添加  D-删除  H-帮助")
    print("=" * 80)

def print_help():
    """打印帮助"""
    print("\n【帮助信息】")
    print("-" * 50)
    print("  R: 刷新数据")
    print("  Q: 退出程序")
    print("  A: 添加自选股 (输入如: sh600519)")
    print("  D: 删除自选股")
    print("  H: 显示帮助")
    print("-" * 50)
    print("\n股票代码说明:")
    print("  sh=上海  sz=深圳")
    print("  如: sh600519(茅台) sz000858(五粮液)")
    input("按回车继续...")

def interactive_mode():
    """交互模式"""
    # 默认自选股
    watchlist = ["sh600519", "sh601318", "sz000858", "sh600036", "sz002594"]
    
    try:
        print_header()
        indices = get_index_data()
        print_indices(indices)
        
        stocks = get_stock_data(watchlist)
        print_stocks(stocks)
        print_footer()
        
        while True:
            try:
                cmd = input("\n请输入命令: ").strip().upper()
                
                if cmd == 'Q' or cmd == 'EXIT':
                    print("感谢使用，再见！")
                    break
                elif cmd == 'R' or cmd == 'REFRESH':
                    clear_screen()
                    print_header()
                    indices = get_index_data()
                    print_indices(indices)
                    stocks = get_stock_data(watchlist)
                    print_stocks(stocks)
                    print_footer()
                elif cmd == 'A':
                    code = input("请输入股票代码 (如: sh600519): ").strip().lower()
                    if code:
                        if code not in watchlist:
                            watchlist.append(code)
                            print(f"已添加 {code}")
                        else:
                            print(f"{code} 已在列表中")
                elif cmd == 'D':
                    code = input("请输入要删除的股票代码: ").strip().lower()
                    if code in watchlist:
                        watchlist.remove(code)
                        print(f"已删除 {code}")
                    else:
                        print(f"{code} 不在列表中")
                elif cmd == 'H' or cmd == 'HELP':
                    print_help()
                    clear_screen()
                    print_header()
                    indices = get_index_data()
                    print_indices(indices)
                    stocks = get_stock_data(watchlist)
                    print_stocks(stocks)
                    print_footer()
            except KeyboardInterrupt:
                print("\n\n感谢使用，再见！")
                break
    except Exception as e:
        print(f"程序错误: {e}")

def auto_refresh_mode(interval=30):
    """自动刷新模式"""
    print("自动刷新模式启动，按 Ctrl+C 退出...\n")
    try:
        while True:
            clear_screen()
            print_header()
            
            indices = get_index_data()
            print_indices(indices)
            
            sh_stocks = get_hot_stocks("sh")
            sz_stocks = get_hot_stocks("sz")
            
            print_stocks(sh_stocks, title="【沪市热门】")
            print_stocks(sz_stocks, title="【深市热门】")
            
            print_footer()
            print(f"\n下次刷新: {interval} 秒后 (按 Ctrl+C 退出)")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n已停止自动刷新")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("       欢迎使用 股票行情终端 v2.0")
    print("       数据来源: 新浪财经")
    print("=" * 50)
    print("\n请选择运行模式:")
    print("  1. 交互模式 (手动刷新)")
    print("  2. 自动刷新模式 (每30秒)")
    print("  3. 退出")
    
    try:
        choice = input("\n请输入选择 (1/2/3): ").strip()
        
        if choice == "1":
            interactive_mode()
        elif choice == "2":
            auto_refresh_mode()
        else:
            print("已退出")
    except KeyboardInterrupt:
        print("\n已退出")
