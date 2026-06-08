import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ══════════════════════════════════════════════════════════════════
# 🛠️ સ્માર્ટ ટ્રેડિંગવ્યૂ સિમ્બોલ કન્વર્ટર (તમામ સર્ચ ઇશ્યૂ ફિક્સ)
# ══════════════════════════════════════════════════════════════════
def get_tradingview_symbol(symbol: str) -> str:
    if not symbol:
        return "TVC:NIFTY"
        
    # બધી ટેક્સ્ટને કેપિટલ કરો અને આજુબાજુની સ્પેસ કાઢી નાખો
    s = symbol.upper().strip()
    
    # જો પહેલેથી જ સાચો એક્સચેન્જ પ્રિફિક્સ (જેમ કે MCX: કે NSE:) લાગેલો હોય, તો તેને ડાયરેક્ટ મોકલો
    if any(s.startswith(p) for p in ["MCX:", "NSE:", "TVC:", "FX:", "FX_IDC:"]):
        return s

    # જો ઓપ્શન/ફ્યુચર્સનો આખો લાંબો સિમ્બોલ હોય, તો તેમાંથી હાઈફન કે સ્પેસ પહેલાનું મેઈન નામ લો
    base_symbol = re.split(r'[- ]', s)[0].strip()

    # પરફેક્ટ ટ્રેડિંગવ્યૂ સિમ્બોલ મેપિંગ ટેબલ
    tv_map = {
        "NIFTY"       : "TVC:NIFTY",
        "BANKNIFTY"   : "TVC:BANKNIFTY",
        "FINNIFTY"    : "TVC:FINNIFTY",
        "MIDCPNIFTY"  : "TVC:MIDCPNIFTY",
        "SENSEX"      : "TVC:SENSEX",
        "CRUDEOIL"    : "MCX:CRUDEOIL1!",
        "CRUDOIL"     : "MCX:CRUDEOIL1!",  # સ્પેલિંગ સેફ્ટી (E વગર)
        "NATURALGAS"  : "MCX:NATURALGAS1!",
        "GOLD"        : "MCX:GOLD1!",
        "SILVER"      : "MCX:SILVER1!",
        "COPPER"      : "MCX:COPPER1!",
        "ZINC"        : "MCX:ZINC1!",
        "USDINR"      : "FX_IDC:USDINR",   # કરન્સી ડાયરેક્ટ લાઈવ ચાર્ટ સોર્સ
    }
    
    # જો લિસ્ટમાં હોય તો ત્યાંથી લો, નહિતર RELIANCE કે SBI જેવા સ્ટોક્સ માટે આગળ ઓટોમેટિક "NSE:" લગાડો
    return tv_map.get(base_symbol, f"NSE:{base_symbol}")


# ══════════════════════════════════════════════════════════════════
# 🌐 વેબ પ્લેટફોર્મના બધા જ રૂટ્સ (Routes)
# ══════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    selected_symbol = request.args.get('symbol', 'NIFTY')
    chart_style = request.args.get('style', 'Candlesticks')
    timeframe = request.args.get('timeframe', '5')
    
    # બેકએન્ડ દ્વારા શુદ્ધ કરેલો ટ્રેડિંગવ્યૂ સિમ્બોલ મેળવો
    tv_symbol = get_tradingview_symbol(selected_symbol)
    
    dashboard_data = {
        "today_pnl": "2,695.00",
        "total_capital": "1,50,000",
        "open_positions": 0,
        "api_status": "Connected" if session.get('broker_connected') else "Disconnected...",
        "api_class": "setup-ready" if session.get('broker_connected') else "setup-pending",
        "raw_symbol": selected_symbol,
        "tv_symbol": tv_symbol,
        "timeframe": timeframe,
        "chart_style": chart_style
    }
    
    return render_template('dashboard.html', data=dashboard_data)


@app.route('/update_chart', methods=['POST'])
def update_chart():
    symbol = request.form.get('symbol', 'NIFTY')
    timeframe = request.form.get('timeframe', '5')
    style = request.form.get('style', 'Candlesticks')
    return redirect(url_for('index', symbol=symbol, timeframe=timeframe, style=style))


@app.route('/connect_broker', methods=['POST'])
def connect_broker():
    broker_name = request.form.get('broker')
    client_id = request.form.get('client_id')
    api_key = request.form.get('api_key')
    
    if client_id and api_key:
        session['broker_connected'] = True
        session['broker_name'] = broker_name
        return jsonify({"status": "success", "message": f"{broker_name} કનેક્ટ થઈ ગયું!"})
    
    return jsonify({"status": "error", "message": "વિગતો અધૂરી છે."}), 400


@app.route('/place_order', methods=['POST'])
def place_order():
    action = request.form.get('action')
    lots = request.form.get('lots', 1)
    mode = request.form.get('mode', 'DRY RUN')
    return jsonify({"status": "success", "message": f"{mode}: {action} ઓર્ડર સફળ રહ્યો."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
