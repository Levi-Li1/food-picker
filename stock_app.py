"""
股票行情展示工具 v4.0
支持K线图展示
"""

import sys
import requests
import time
import json
import base64
from datetime import datetime, timedelta
from io import BytesIO
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QHeaderView, QTabWidget, QGroupBox, QFrame, QMessageBox,
    QProgressBar, QSplitter, QDialog, QTextBrowser, QScroller
)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MaxNLocator

# 新浪财经API
SINA_FINANCE_URL = "https://hq.sinajs.cn/list={codes}"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://finance.sina.com.cn/"
}

# K线数据API (新浪财经历史K线)
SINA_KLINE_URL = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"

# 颜色定义
COLOR_RISE = QColor(255, 68, 68)
COLOR_FALL = QColor(0, 200, 100)
COLOR_BG_MAIN = QColor(26, 32, 44)
COLOR_TEXT = QColor(255, 255, 255)


class KLineDataThread(QThread):
    """K线数据获取线程"""
    data_ready = pyqtSignal(list, str)
    error_occurred = pyqtSignal(str)

    def __init__(self, code, period="daily", count=60):
        super().__init__()
        self.code = code
        self.period = period
        self.count = count

    def run(self):
        try:
            # 获取股票名称
            name = self.get_stock_name()
            
            # 获取K线数据
            data = self.fetch_kline_data()
            self.data_ready.emit(data, name)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def get_stock_name(self):
        """获取股票名称"""
        try:
            url = SINA_FINANCE_URL.format(codes=self.code)
            resp = requests.get(url, headers=HEADERS, timeout=5)
            resp.encoding = 'gbk'
            if '=' in resp.text:
                parts = resp.text.split('=')[1].split(',')
                return parts[0].strip('"') if parts else self.code
        except:
            pass
        return self.code

    def fetch_kline_data(self):
        """获取K线数据"""
        market = "sh" if self.code.startswith("sh") else "sz"
        symbol = f"{market}{self.code[2:]}"
        
        params = {
            "symbol": symbol,
            "scale": self.get_scale(),
            "ma": "no",
            "datalen": self.count
        }
        
        resp = requests.get(SINA_KLINE_URL, params=params, headers=HEADERS, timeout=10)
        data = resp.json()
        return data if isinstance(data, list) else []

    def get_scale(self):
        """获取周期对应的scale"""
        scale_map = {
            "daily": 240,
            "weekly": 1200,
            "monthly": 7200,
            "5min": 5,
            "15min": 15,
            "60min": 60
        }
        return scale_map.get(self.period, 240)


class StockDataThread(QThread):
    """实时数据获取线程"""
    data_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, codes):
        super().__init__()
        self.codes = codes

    def run(self):
        try:
            stocks = self.fetch_data(self.codes)
            self.data_ready.emit(stocks)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def fetch_data(self, stock_codes):
        """获取股票数据"""
        if not stock_codes:
            return []
        
        codes_str = ",".join(stock_codes)
        url = SINA_FINANCE_URL.format(codes=codes_str)
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = 'gbk'
        
        stocks = []
        lines = resp.text.strip().split('\n')
        
        for i, line in enumerate(lines):
            if '=' not in line or i >= len(stock_codes):
                continue
            
            code_with_quote = line.split('=')[1].strip('";\n ')
            if not code_with_quote:
                continue
            
            parts = code_with_quote.split(',')
            if len(parts) >= 32:
                price = float(parts[3])
                close = float(parts[2])
                change = price - close
                pct = (change / close * 100) if close > 0 else 0
                
                stocks.append({
                    "code": stock_codes[i],
                    "name": parts[0],
                    "open": float(parts[1]),
                    "close": close,
                    "price": price,
                    "high": float(parts[4]),
                    "low": float(parts[5]),
                    "volume": int(parts[8]),
                    "amount": float(parts[9]),
                    "change": change,
                    "pct": pct,
                    "time": parts[31] + " " + parts[30] if len(parts) > 31 else ""
                })
        return stocks


class KLineDialog(QDialog):
    """K线图对话框"""
    
    def __init__(self, code, name="", parent=None):
        super().__init__(parent)
        self.code = code
        self.name = name
        self.kline_data = []
        self.current_period = "daily"
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle(f"K线图 - {self.name} ({self.code})")
        self.setGeometry(150, 150, 1000, 700)
        
        # 深色主题
        self.setStyleSheet("""
            QDialog { background-color: rgb(26, 32, 44); color: white; }
            QLabel { color: white; }
            QPushButton { 
                background-color: rgb(45, 55, 72); 
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: rgb(55, 65, 82); }
            QPushButton:pressed { background-color: rgb(65, 75, 92); }
            QPushButton:checked { background-color: rgb(0, 122, 204); }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        
        # 周期选择
        toolbar.addWidget(QLabel("周期:"))
        
        self.period_btns = {}
        periods = [("日K", "daily"), ("周K", "weekly"), ("月K", "monthly")]
        for text, period in periods:
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setChecked(period == "daily")
            btn.clicked.connect(lambda _, p=period: self.change_period(p))
            toolbar.addWidget(btn)
            self.period_btns[period] = btn
        
        toolbar.addStretch()
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.load_data)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # K线图画布
        self.figure = Figure(figsize=(10, 6), facecolor='#1a202c')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 信息栏
        self.info_label = QLabel("加载中...")
        self.info_label.setStyleSheet("padding: 5px; background: rgb(38, 46, 59); border-radius: 4px;")
        layout.addWidget(self.info_label)
        
        # 设置matplotlib中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    
    def change_period(self, period):
        """切换周期"""
        self.current_period = period
        for p, btn in self.period_btns.items():
            btn.setChecked(p == period)
        self.load_data()
    
    def load_data(self):
        """加载K线数据"""
        self.info_label.setText("正在加载K线数据...")
        
        self.thread = KLineDataThread(self.code, self.current_period)
        self.thread.data_ready.connect(self.plot_kline)
        self.thread.error_occurred.connect(self.show_error)
        self.thread.start()
    
    def plot_kline(self, data, name):
        """绘制K线图"""
        self.kline_data = data
        self.name = name
        
        if not data:
            self.info_label.setText("暂无数据")
            return
        
        self.figure.clear()
        
        # 设置背景色
        self.figure.patch.set_facecolor('#1a202c')
        
        # 创建子图
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e2530')
        
        # 解析数据
        dates = []
        opens = []
        highs = []
        lows = []
        closes = []
        volumes = []
        
        for item in data:
            try:
                dates.append(datetime.strptime(item['day'], '%Y-%m-%d'))
                opens.append(float(item['open']))
                highs.append(float(item['high']))
                lows.append(float(item['low']))
                closes.append(float(item['close']))
                volumes.append(int(item['volume']))
            except:
                continue
        
        if not dates:
            self.info_label.setText("数据解析失败")
            return
        
        # 绘制K线
        for i, (d, o, h, l, c) in enumerate(zip(dates, opens, highs, lows, closes)):
            if c >= o:  # 涨
                color = '#ff4444'
                body_bottom = o
                body_height = c - o
            else:  # 跌
                color = '#00c864'
                body_bottom = c
                body_height = o - c
            
            # 绘制上下影线
            ax.plot([d, d], [l, h], color=color, linewidth=1)
            
            # 绘制实体
            if body_height == 0:
                body_height = 0.001
            rect = Rectangle((mdates.date2num(d) - 0.3, body_bottom), 
                            0.6, body_height,
                            facecolor=color, edgecolor=color, linewidth=0.5)
            ax.add_patch(rect)
        
        # 设置x轴日期格式
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(MaxNLocator(10))
        
        # 隐藏边框
        for spine in ax.spines.values():
            spine.set_color('#333333')
        
        # 设置刻度颜色
        ax.tick_params(colors='gray', labelsize=9)
        
        # 添加网格
        ax.grid(True, alpha=0.2, color='#333333', linestyle='--')
        
        # 添加标题
        ax.set_title(f"{name} ({self.code}) K线图 - {self.current_period}", 
                    color='white', fontsize=12, pad=10)
        
        # 设置y轴标签
        ax.set_ylabel("价格", color='gray', fontsize=10)
        
        # 调整布局
        self.figure.tight_layout()
        self.canvas.draw()
        
        # 更新信息
        last = data[-1] if data else {}
        info_text = f"最新: {last.get('close', '--')} | 最高: {last.get('high', '--')} | 最低: {last.get('low', '--')} | 成交量: {int(last.get('volume', 0)):,}"
        self.info_label.setText(info_text)
    
    def show_error(self, msg):
        """显示错误"""
        self.info_label.setText(f"加载失败: {msg}")


class StockTableWidget(QTableWidget):
    """股票表格组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(["名称", "代码", "现价", "涨跌", "涨跌幅", "最高", "最低", "成交额"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setMinimumHeight(250)
        self.cellDoubleClicked.connect(self.on_cell_double_clicked)
    
    def on_cell_double_clicked(self, row, column):
        """双击单元格 - 显示K线"""
        code = self.item(row, 1)
        name = self.item(row, 0)
        if code and name:
            dialog = KLineDialog(code.text(), name.text(), self)
            dialog.exec_()


class StockApp(QMainWindow):
    """股票行情应用主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 默认自选股
        self.watchlist = ["sh600519", "sh601318", "sz000858", "sh600036", "sz002594"]
        
        # 大盘指数
        self.indices = ["sh000001", "sz399001", "sz399006", "sh000300", "sh000016", "sh000688"]
        
        self.init_ui()
        self.init_timers()
        self.load_data()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("股票行情终端 v4.0 - 新浪财经 | 双击查看K线")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: rgb(26, 32, 44); }
            QLabel { color: white; }
            QTabWidget::pane { border: 1px solid rgb(45, 55, 72); background: rgb(26, 32, 44); }
            QTabBar::tab { 
                background: rgb(38, 46, 59); 
                color: white;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected { background: rgb(0, 122, 204); }
            QPushButton { 
                background-color: rgb(45, 55, 72); 
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: rgb(55, 65, 82); }
            QLineEdit {
                background-color: rgb(38, 46, 59);
                color: white;
                border: 1px solid rgb(60, 70, 87);
                padding: 8px;
                border-radius: 4px;
            }
            QLineEdit:focus { border: 1px solid rgb(0, 122, 204); }
            QTableWidget { 
                background-color: rgb(26, 32, 44);
                color: white;
                gridline-color: rgb(45, 55, 72);
                border: none;
            }
            QTableWidget::item:alternate { background-color: rgb(38, 46, 59); }
            QHeaderView::section {
                background-color: rgb(45, 55, 72);
                color: white;
                padding: 8px;
                border: none;
            }
            QProgressBar {
                border: none;
                background-color: rgb(38, 46, 59);
                border-radius: 4px;
            }
            QProgressBar::chunk { background-color: rgb(0, 122, 204); }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # 顶部标题栏
        header = self.create_header()
        main_layout.addLayout(header)
        
        # 标签页
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_index_tab(), "📊 大盘指数")
        self.tabs.addTab(self.create_watchlist_tab(), "⭐ 自选股")
        self.tabs.addTab(self.create_hot_tab(), "🔥 热门股票")
        main_layout.addWidget(self.tabs)
        
        # 底部状态栏
        status = self.create_status_bar()
        main_layout.addLayout(status)
    
    def create_header(self):
        """创建标题栏"""
        header_layout = QHBoxLayout()
        
        title = QLabel("📈 股票行情终端")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入股票代码")
        self.search_input.setFixedWidth(200)
        self.search_input.returnPressed.connect(self.add_stock)
        header_layout.addWidget(self.search_input)
        
        # 添加按钮
        add_btn = QPushButton("添加自选")
        add_btn.clicked.connect(self.add_stock)
        header_layout.addWidget(add_btn)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_data)
        header_layout.addWidget(refresh_btn)
        
        return header_layout
    
    def create_index_tab(self):
        """大盘指数标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        hint = QLabel("💡 双击个股查看K线图")
        hint.setStyleSheet("color: gray; padding: 5px;")
        layout.addWidget(hint)
        
        self.index_table = StockTableWidget()
        layout.addWidget(self.index_table)
        
        return widget
    
    def create_watchlist_tab(self):
        """自选股标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        hint = QLabel("💡 双击个股查看K线图 | 双击表格行可删除")
        hint.setStyleSheet("color: gray; padding: 5px;")
        layout.addWidget(hint)
        
        self.watchlist_table = StockTableWidget()
        self.watchlist_table.cellDoubleClicked.connect(self.handle_watchlist_click)
        layout.addWidget(self.watchlist_table)
        
        return widget
    
    def handle_watchlist_click(self, row, column):
        """处理自选股表格点击"""
        # 如果需要特殊处理可以在这里添加
        pass
    
    def create_hot_tab(self):
        """热门股票标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        hint = QLabel("💡 双击个股查看K线图")
        hint.setStyleSheet("color: gray; padding: 5px;")
        layout.addWidget(hint)
        
        # 快捷按钮
        hot_layout = QHBoxLayout()
        
        sh_label = QLabel("沪市:")
        sh_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        hot_layout.addWidget(sh_label)
        
        sh_stocks = ["sh600519", "sh601318", "sh600036", "sh600276"]
        for code in sh_stocks:
            btn = QPushButton(code)
            btn.setFixedWidth(70)
            btn.clicked.connect(lambda _, c=code: self.add_stock_by_code(c))
            hot_layout.addWidget(btn)
        
        sz_label = QLabel("  深市:")
        sz_label.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
        hot_layout.addWidget(sz_label)
        
        sz_stocks = ["sz000858", "sz002594", "sz000333", "sz002415"]
        for code in sz_stocks:
            btn = QPushButton(code)
            btn.setFixedWidth(70)
            btn.clicked.connect(lambda _, c=code: self.add_stock_by_code(c))
            hot_layout.addWidget(btn)
        
        hot_layout.addStretch()
        layout.addLayout(hot_layout)
        
        self.hot_table = StockTableWidget()
        layout.addWidget(self.hot_table)
        
        return widget
    
    def create_status_bar(self):
        """创建状态栏"""
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("就绪")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        self.time_label = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        status_layout.addWidget(self.time_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        return status_layout
    
    def init_timers(self):
        """初始化定时器"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.load_data)
        self.refresh_timer.start(30000)  # 30秒
        
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
    
    def update_clock(self):
        self.time_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def load_data(self):
        """加载数据"""
        self.status_label.setText("正在获取数据...")
        self.progress_bar.setVisible(True)
        
        self.thread_index = StockDataThread(self.indices)
        self.thread_index.data_ready.connect(self.update_index_table)
        self.thread_index.start()
        
        self.thread_watch = StockDataThread(self.watchlist)
        self.thread_watch.data_ready.connect(self.update_watchlist_table)
        self.thread_watch.start()
        
        hot_codes = ["sh600519", "sh601318", "sh600036", "sh600276", "sh600887",
                     "sz000858", "sz002594", "sz000333", "sz002415", "sz000001"]
        self.thread_hot = StockDataThread(hot_codes)
        self.thread_hot.data_ready.connect(self.update_hot_table)
        self.thread_hot.start()
    
    def update_table(self, table, stocks):
        """更新表格"""
        table.setRowCount(len(stocks))
        
        for row, stock in enumerate(stocks):
            name = stock.get("name", "--")
            if len(name) > 6:
                name = name[:6]
            
            items_data = [
                (name, True),
                (stock.get("code", "--"), False),
                (f"{stock['price']:.2f}", False),
                (f"{stock.get('change', 0):+.2f}", False),
                (f"{stock.get('pct', 0):+.2f}%", True),
                (f"{stock.get('high', 0):.2f}", False),
                (f"{stock.get('low', 0):.2f}", False),
                (self.format_amount(stock.get('amount', 0)), False)
            ]
            
            for col, (text, is_key) in enumerate(items_data):
                item = QTableWidgetItem(text)
                if is_key:
                    item.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
                item.setForeground(COLOR_TEXT)
                table.setItem(row, col, item)
            
            # 设置涨跌颜色
            pct = stock.get('pct', 0)
            if pct > 0:
                color = COLOR_RISE
            elif pct < 0:
                color = COLOR_FALL
            else:
                color = QColor(128, 128, 128)
            
            for col in [3, 4]:  # 涨跌和涨跌幅列
                item = table.item(row, col)
                if item:
                    item.setForeground(color)
        
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"更新完成 | {datetime.now().strftime('%H:%M:%S')}")
    
    def format_amount(self, amount):
        """格式化成交额"""
        if amount >= 100000000:
            return f"{amount/100000000:.2f}亿"
        elif amount >= 10000:
            return f"{amount/10000:.2f}万"
        return f"{amount:.0f}"
    
    def update_index_table(self, stocks):
        self.update_table(self.index_table, stocks)
    
    def update_watchlist_table(self, stocks):
        self.update_table(self.watchlist_table, stocks)
    
    def update_hot_table(self, stocks):
        self.update_table(self.hot_table, stocks)
    
    def add_stock(self):
        """添加自选股"""
        code = self.search_input.text().strip().lower()
        if not code or not any(c.isdigit() for c in code):
            QMessageBox.warning(self, "提示", "请输入正确的股票代码")
            return
        
        if code not in self.watchlist:
            self.watchlist.append(code)
            self.search_input.clear()
            self.load_data()
            QMessageBox.information(self, "成功", f"已添加 {code}")
        else:
            QMessageBox.information(self, "提示", f"{code} 已在自选列表中")
    
    def add_stock_by_code(self, code):
        self.search_input.setText(code)
        self.add_stock()


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft YaHei", 10))
    window = StockApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
