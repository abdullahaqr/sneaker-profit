from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/calculate_profit', methods=['POST'])
def calculate_profit():
    try:
        # Ensure JSON data is present
        if not request.is_json:
            return jsonify({"error": "Invalid input: JSON payload expected"}), 415  # Unsupported Media Type

        # Fetch JSON data from request
        data = request.json

        # Validate presence and type of required fields
        required_fields = ['retail_price', 'resale_price', 'shipping_cost', 'platform']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
            if not isinstance(data[field], (int, float)) and field != 'platform':
                return jsonify({"error": f"Invalid data type for {field}. Expected a numeric value."}), 400
        
        retail_price = float(data['retail_price'])
        resale_price = float(data['resale_price'])
        shipping_cost = float(data['shipping_cost'])
        platform = data['platform']

        # Validate the 'platform' field
        valid_platforms = ["StockX", "GOAT", "eBay"]
        # if platform not in valid_platforms and 'other_fee' not in data:
        # if any(platform for valid_plat in valid_platforms if platform != valid_plat) and ('other_fee' not in data):
        if (platform not in valid_platforms) and ('other_fee' not in data):
            return jsonify({"error": "Invalid platform or missing 'other_fee' for custom platforms"}), 400

        # Set platform fees
        print('Platform->>>', platform)
        if platform == "StockX":
            fee_percent = 9.5
            transaction_fee = 4
        elif platform == "GOAT":
            fee_percent = 9.5
            transaction_fee = 5
        elif platform == "eBay":
            fee_percent = 0 if resale_price >= 100 else float(data.get('other_fee', 0))
            transaction_fee = 0
        else:
            fee_percent = float(data.get('other_fee', 0))
            transaction_fee = 0

        # Calculate fees and profit
        platform_fee = (fee_percent / 100) * resale_price
        total_costs = retail_price + platform_fee + transaction_fee + shipping_cost
        profit = resale_price - total_costs
        roi = (profit / retail_price) * 100

        # Return results as JSON
        return jsonify({
            "estimated_profit": f"${profit:.2f}",
            "roi_percentage": f"{roi:.2f}%"
        }), 200  # OK status

    except ValueError as e:
        return jsonify({"error": "Invalid input: Unable to convert input to float values"}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing required field in JSON data: {str(e)}"}), 400
    except Exception as e:
        # Generic catch for unexpected errors
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
    # app.run()
