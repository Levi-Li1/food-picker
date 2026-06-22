"""测试股票数据获取"""
from stock_terminal import get_index_data, get_stock_data

print("=" * 50)
print("  股票行情终端 - 数据测试")
print("=" * 50)

print("\n【大盘指数】")
indices = get_index_data()
for s in indices:
    try:
        change = float(s["price"]) - float(s["close"]) if s.get("close") and s["close"] != "0" else 0
        pct = (change / float(s["close"]) * 100) if s.get("close") and float(s["close"]) > 0 else 0
        print(f"  {s['name']:<10} {s['price']:>10}  {pct:+.2f}%")
    except:
        print(f"  {s['name']:<10} {s.get('price', '--')}")

print("\n【默认自选股】")
stocks = get_stock_data(["sh600519", "sh601318", "sz000858", "sh600036", "sz002594"])
for s in stocks:
    try:
        change = float(s["price"]) - float(s["close"]) if s.get("close") and s["close"] != "0" else 0
        pct = (change / float(s["close"]) * 100) if s.get("close") and float(s["close"]) > 0 else 0
        print(f"  {s['name']:<10} {s['price']:>10}  {pct:+.2f}%")
    except:
        print(f"  {s['name']:<10} {s.get('price', '--')}")

print("\n" + "=" * 50)
print("  测试完成！")
print("=" * 50)
