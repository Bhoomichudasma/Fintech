# Quick Start Guide - Testing All Features

## 🚀 Starting the Application

### Backend (Port 8000)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend (Port 5173)
```powershell
cd frontend
npm install
npm run dev
```

## 🧪 Testing Each Feature

### 1. **Single Stock Analysis**
- ✅ Select any stock from the left sidebar
- ✅ View interactive OHLC chart
- ✅ Toggle between 7D, 30D, 90D, 1Y timeframes
- ✅ Enable/disable MA7, MA30, Prediction overlays
- ✅ Check 52-week high/low, volatility cards
- ✅ Read "Why did this stock move?" section
- ✅ View Market Mood Index (Bullish/Bearish/Neutral)

### 2. **Stock Comparison (FIXED!)**
- ✅ Scroll to "Compare multiple stocks" section
- ✅ Select 2-8 stocks using the picker
- ✅ Watch the comparison table appear with metrics
- ✅ View correlation heatmap (color-coded)
- ✅ Check Top Gainers/Losers panel
- ✅ See side-by-side:
  - Average price
  - Volatility %
  - Momentum %
  - Health Score (0-100)
  - Risk Level (Low/Medium/High)

### 3. **AI Predictions**
- ✅ Click "Prediction" toggle on main chart
- ✅ See dashed yellow line for 7-day forecast
- ✅ View separate "AI 7-day outlook" chart
- ✅ Predictions based on linear regression

### 4. **Investment Simulator**
- ✅ Find "If you invested ₹10,000" card
- ✅ Shows growth chart over selected period
- ✅ Displays final value in rupees
- ✅ For custom amounts, use Portfolio Simulator

### 5. **Portfolio Simulator**
- ✅ Locate Portfolio Simulator section
- ✅ Add multiple stocks with symbols
- ✅ Set weights for each holding
- ✅ Customize initial investment amount
- ✅ Click "Run" to see portfolio performance
- ✅ View total return percentage
- ✅ See portfolio value chart

### 6. **Market Mood Index**
- ✅ Check the new Market Mood Index card
- ✅ See sentiment bar (Bearish ← → Bullish)
- ✅ View current mood: Bullish 🚀 / Bearish 📉 / Neutral ⏸️
- ✅ Read detailed breakdown:
  - Trend analysis (MA7 vs MA30)
  - Momentum strength
  - Health score
  - Bullish vs Bearish signal count

### 7. **"Why Did This Stock Move?"**
- ✅ Anomaly detection alerts
- ✅ Price spike notifications
- ✅ Volume surge warnings
- ✅ Related news headlines
- ✅ Combined technical + fundamental analysis

### 8. **News Integration**
- ✅ Latest news headlines displayed
- ✅ Source and timestamp shown
- ✅ Click through to full articles
- ✅ Correlated with price movements

## 🎯 Expected Behavior

### When Comparing Stocks:
1. Select AAPL and MSFT → See comparison table
2. Add GOOGL → Table updates with 3 stocks
3. Correlation matrix shows relationships
4. Top movers auto-sorts by momentum

### When Viewing Single Stock:
1. Select TSLA → All metrics update
2. Toggle MA7 → Purple line appears on chart
3. Toggle MA30 → Yellow line appears on chart
4. Toggle Prediction → Dashed forecast line appears
5. Change to 7D → Chart zooms to week view

### When Using Portfolio Simulator:
1. Add AAPL (weight: 1), MSFT (weight: 1)
2. Set initial: ₹10,000
3. Click "Run" → See portfolio chart
4. View total return percentage
5. Adjust weights → Re-run for different allocation

## 🐛 Troubleshooting

### If Comparison Not Working:
1. Ensure at least 2 stocks selected
2. Check browser console for errors
3. Verify backend is running on port 8000
4. Try refreshing the page

### If Charts Not Displaying:
1. Wait for data to load (spinner should disappear)
2. Check network tab for API responses
3. Verify Recharts library installed: `npm list recharts`
4. Try different time range (7D, 30D, etc.)

### If Predictions Missing:
1. Ensure stock has sufficient historical data
2. Check that prediction toggle is enabled
3. Look for predictions in API response
4. Verify linear regression service running

### If News Not Showing:
1. Check if NEWSAPI_KEY set in .env file
2. Without key, mock news will display
3. Verify internet connection
4. Check news_service.py fallback logic

## 📊 Data Validation

All metrics should show realistic values:
- **Volatility**: Typically 1-5% for most stocks
- **Momentum**: Can range from -50% to +100%+
- **Health Score**: 0-100 scale
- **52-week High/Low**: Should bracket current price
- **Correlation**: -1.0 to +1.0 range

## 🎨 UI Elements Checklist

### Colors (Neo-Brutalism Style):
- ✅ Accent color (green): #8ef5b9 for positive metrics
- ✅ Warning color (yellow): #f9cf58 for cautions
- ✅ Danger color (red): For negative metrics
- ✅ Solid colors, no gradient merges

### Interactive Elements:
- ✅ Hover states on buttons
- ✅ Active states for toggles
- ✅ Loading spinners during fetch
- ✅ Tooltips on charts
- ✅ Responsive grid layouts

## 📈 Performance Benchmarks

Expected load times:
- Initial page load: < 2 seconds
- Stock selection change: < 1 second
- Comparison update: < 1.5 seconds
- Portfolio simulation: < 2 seconds

## ✅ Success Criteria

You should see:
1. ✅ Working comparison with 2+ stocks
2. ✅ Correlation heatmap with color coding
3. ✅ Top gainers/losers properly sorted
4. ✅ Prediction lines on charts
5. ✅ Market Mood Index displaying sentiment
6. ✅ Investment simulator showing growth
7. ✅ Portfolio simulator with multiple stocks
8. ✅ News headlines integrated with analysis
9. ✅ All toggles functional (MA7, MA30, Prediction)
10. ✅ Time range filters working (7D, 30D, 90D, 1Y)

---

**Happy Testing!** 🚀


