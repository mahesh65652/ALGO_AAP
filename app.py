import os
import re
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)  # સેઝન મેનેજમેન્ટ માટે સેફ્ટી કી

# ------------------------------------------------------------------
# 🛠️ સ્માર્ટ ટ્રેડિંગવ્યૂ સિમ્બોલ મેપિંગ ફંક્શન (બધી જ એરર્સ ફિક્સ)
# ------------------------------------------------------------------
def get_tradingview_symbol(symbol: str) -> str:
    if not symbol:
        return "TVC:NIFTY"
        
    # ૧. બધી ટેક્સ્ટને કેપિટલ કરો અને આજુબાજુની વધારાની સ્પેસ કાઢી નાખો
    s = symbol.upper().strip()
    
    # ૨. જો યુઝરે પહેલેથી જ સાચો એક્સચેન્જ પ્રિફિક્સ લગાડેલો હોય, તો તેને ડાયરેક્ટ રિટર્ન કરો
    if s.startswith("MCX:") or s.startswith("NSE:") or s.startswith("TVC:") or s.startswith("FX:") or s.startswith("FX_IDC:"):
        return s

    # ૩. જો ઓપ્શન/ફ્યુચર્સનો લાંબો સિમ્બોલ હોય (જેમ કે CRUDEOIL-19-SEP-25-CE), તો તેમાંથી મેઈન નામ અલગ કરો
    # આ હાઈફન (-) અથવા સ્પેસ પછીનું બધું કાઢી નાખશે જેથી આપણને ફક્ત મેઈન સ્ક્રિપ્ટનું નામ મળે
    base_symbol = re.split(r'[- ]', s)[0].strip()

    # ૪. પરફેક્ટ ટ્રેડિંગવ્યૂ ઇન્ડેક્સ, કોમોડિટી અને કરન્સી મેપિંગ ડિક્શનરી
    tv_map = {
        "NIFTY"       : "TVC:NIFTY",
        "BANKNIFTY"   : "TVC:BANKNIFTY",
        "FINNIFTY"    : "TVC:FINNIFTY",
        "MIDCPNIFTY"  : "TVC:MIDCPNIFTY",
        "SENSEX"      : "TVC:SENSEX",
        "CRUDEOIL"    : "MCX:CRUDEOIL1!",
        "CRUDOIL"     : "MCX:CRUDEOIL1!",  # સ્પેલિંગ મિસ્ટેક સેફ્ટી (E વગર)
        "NATURALGAS"  : "MCX:NATURALGAS1!",
        "GOLD"        : "MCX:GOLD1!",
        "SILVER"      : "MCX:SILVER1!",
        "COPPER"      : "MCX:COPPER1!",
        "ZINC"        : "MCX:ZINC1!",
        "USDINR"      : "FX_IDC:USDINR",   # લાઈવ કરન્સી રેટ માટે બેસ્ટ ટ્રેડિંગવ્યૂ સોર્સ
    }
    
    # ૫. જો મેપિંગમાં નામ મળી જાય તો તે રિટર્ન કરો, નહિતર ઇક્વિટી સ્ટોક્સ માટે ડિફોલ્ટ NSE પ્રિફિક્સ લગાડો
    return tv_map.get(base_symbol, f"NSE:{base_symbol}")


# ------------------------------------------------------------------
# 🌐 વેબ પ્લેટફોર્મના રૂટ્સ (Routes)
# ------------------------------------------------------------------

@app.route('/')
def index():
    # ડિફોલ્ટ ચાર્ટ તરીકે NIFTY સેટ રાખીએ છીએ
    selected_symbol = request.args.get('symbol', 'NIFTY')
    chart_style = request.args.get('style', 'Candlesticks')
    timeframe = request.args.get('timeframe', '5')
    
    # આપણા સ્માર્ટ ફંક્શન દ્વારા ટ્રેડિંગવ્યૂ માટેનો શુદ્ધ સિમ્બોલ મેળવો
    tv_symbol = get_tradingview_symbol(selected_symbol)
    
    # ડેશબોર્ડ ડેટા (ડેમો સ્ટેટ્સ જે સ્ક્રીનશોટમાં છે તે મુજબ)
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
    """ જ્યારે યુઝર સર્ચ બોક્સમાં કંઈ લખીને એન્ટર મારે ત્યારે આ હિટ થશે """
    symbol = request.form.get('symbol', 'NIFTY')
    timeframe = request.form.get('timeframe', '5')
    style = request.form.get('style', 'Candlesticks')
    
    # ચાર્ટ અપડેટ સાથે પેજ રીલોડ કરો
    return redirect(url_for('index', symbol=symbol, timeframe=timeframe, style=style))


@app.route('/connect_broker', methods=['POST'])
def connect_broker():
    """ બ્રોકર કન્ફિગરેશન (Angel One, વગેરે) કનેક્ટ કરવા માટે """
    broker_name = request.form.get('broker')
    client_id = request.form.get('client_id')
    api_key = request.form.get('api_key')
    totp = request.form.get('totp')
    
    # અહીં તમારો બ્રોકર કનેક્શનનો અસલી લોજિક આવશે
    if client_id and api_key:
        session['broker_connected'] = True
        session['broker_name'] = broker_name
        return jsonify({"status": "success", "message": f"{broker_name} સાથે કનેક્શન સફળ રહ્યું!"})
    
    return jsonify({"status": "error", "message": "કૃપા કરીને બધી વિગતો સાચી ભરો."}), 400


@app.route('/place_order', methods=['POST'])
def place_order():
    """ ઓર્ડર કંટ્રોલ સેન્ટર પરથી બાય/સેલ કરવા માટે """
    action = request.form.get('action') # BUY, SELL, WAIT
    strike_price = request.form.get('strike_price')
    expiry = request.form.get('expiry')
    lots = request.form.get('lots', 1)
    sl = request.form.get('sl')
    target = request.form.get('target')
    mode = request.form.get('mode', 'DRY RUN')
    
    # ઓર્ડર પ્લેસ કરવાનો લોજિક અહીં આવશે
    return jsonify({
        "status": "success", 
        "message": f"{mode} મોડમાં ઓર્ડર સબમિટ થયો: {action} | Lots: {lots} | SL: {sl} | Tgt: {target}"
    })


# ------------------------------------------------------------------
# 🚀 એપ્લિકેશન સ્ટાર્ટ કરો
# ------------------------------------------------------------------
if __name__ == '__main__':
    # ડેવલપમેન્ટ વખતે લાઈવ ચેન્જ જોવા debug=True રાખેલ છે
    app.run(host='0.0.0.0', port=5000, debug=True)
