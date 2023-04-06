from PyQt5 import QtWidgets, QtGui, QtCore
from pycoingecko import CoinGeckoAPI


class TopCoins(QtWidgets.QWidget):
    def __init__(self):
        super(TopCoins, self).__init__()

        # Initialize CoinGeckoAPI client
        self.cg = CoinGeckoAPI()
        self.coins_data = []

        # Set window title and icon
        self.setWindowTitle("Top Coins by Volume to Market Cap Ratio")
        self.setWindowIcon(QtGui.QIcon("coin.png"))

        # Set custom font
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)

        # Create UI elements
        self.layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Loading top coins...")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFont(font)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Set dark mode theme
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197))
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Fetch data from CoinGecko API
        self.update_data()

    def update_data(self):
        self.coins_data.clear()

        # Get coin market data for all coins
        coins_data = self.cg.get_coins_markets(vs_currency='usd')

        # Filter only coins with a market cap of 50 million or above
        filtered_coins_data = [coin for coin in coins_data if coin['market_cap'] >= 50000000]

        # Sort by volume to market cap ratio in the last 24 hours
        sorted_coins_data = sorted(filtered_coins_data, key=lambda x: x['total_volume']/x['market_cap'], reverse=True)

        # Get top 10 coins
        top_coins_data = sorted_coins_data[:10]

        for coin in top_coins_data:
            name = coin['name']
            symbol = coin['symbol'].upper()
            ratio = coin['total_volume'] / coin['market_cap']

            self.coins_data.append("{} ({}, Volume to Market Cap Ratio: {:.6f})".format(name, symbol, ratio))

    def update_label(self, data):
        self.label.setText(data)


if __name__ == "__main__":
    import sys

    # Set application style
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set window and icon style
    icon = QtGui.QIcon("coin.png")
    app.setWindowIcon(icon)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197))
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

    app.setPalette(palette)

    # Set window dimensions and position
    window = TopCoins()
    window.setGeometry(500, 200, 400, 150)

    # Refresh data every 30 seconds
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: window.update_label('\n'.join(window.coins_data)))
    timer.timeout.connect(window.update_data)
    timer.start(30000)

    window.show()
    sys.exit(app.exec_())
